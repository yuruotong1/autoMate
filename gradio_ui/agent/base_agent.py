"""Base agent class with error handling and retry logic"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from gradio_ui.utils.error_handler import (
    retry_with_backoff,
    with_timeout,
    RetryConfig,
    APIException,
    create_error_context,
)
from gradio_ui.utils.logger import agent_logger

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents with error handling and retry logic"""

    def __init__(self, model_config: Dict[str, Any], api_key: str, base_url: Optional[str] = None):
        """
        Initialize base agent.

        Args:
            model_config: Model configuration
            api_key: API key for LLM provider
            base_url: Optional custom base URL for API

        Raises:
            ValueError: If required configuration is missing
        """
        if not model_config:
            raise ValueError("model_config is required")
        if not api_key:
            raise ValueError("api_key is required")

        self.model_config = model_config
        self.api_key = api_key
        self.base_url = base_url
        self.SYSTEM_PROMPT = ""

        # Setup retry configuration
        self.retry_config = RetryConfig(
            max_retries=3,
            initial_delay=1.0,
            max_delay=30.0,
        )

        # Rate limiter for API calls
        from gradio_ui.utils.error_handler import RateLimiter
        self.rate_limiter = RateLimiter(max_calls=10, time_window=60)

        logger.debug(f"Initialized {self.__class__.__name__} with model: {model_config.get('model')}")

    @retry_with_backoff(exceptions=(APIException,))
    @with_timeout(timeout_seconds=30)
    async def analyze(self, **kwargs) -> Dict[str, Any]:
        """
        Analyze input and return results.
        Must be implemented by subclasses.

        Returns:
            Dictionary with analysis results
        """
        raise NotImplementedError("Subclasses must implement analyze()")

    async def _call_llm(
        self,
        messages: List[Dict[str, Any]],
        schema: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> str:
        """
        Call LLM with messages and optional schema.

        Args:
            messages: List of message dictionaries
            schema: Optional JSON schema for structured output
            **kwargs: Additional parameters for LLM call

        Returns:
            LLM response as string

        Raises:
            APIException: If API call fails
        """
        try:
            # Check rate limit
            await self.rate_limiter.await_if_needed()

            provider = self.model_config.get("provider", "openai")
            model = self.model_config.get("model", "gpt-4o")

            logger.debug(f"Calling {provider} API with model {model}")

            if provider == "anthropic":
                return await self._call_anthropic(messages, schema, **kwargs)
            elif provider in ["openai", "yeka", "openai-next"]:
                return await self._call_openai(messages, schema, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {provider}")

        except Exception as e:
            error_context = create_error_context(e, {"model": model, "provider": provider})
            agent_logger.error(f"LLM call failed: {error_context}")
            raise APIException(str(e), retryable=True)

    async def _call_anthropic(
        self,
        messages: List[Dict[str, Any]],
        schema: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> str:
        """
        Call Anthropic Claude API.

        Args:
            messages: Message list
            schema: Optional JSON schema
            **kwargs: Additional parameters

        Returns:
            Response string
        """
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key, base_url=self.base_url)

            request_kwargs = {
                "model": self.model_config.get("model", "claude-3-5-sonnet-20241022"),
                "max_tokens": self.model_config.get("max_tokens", 4096),
                "temperature": self.model_config.get("temperature", 0.7),
                "messages": messages,
            }

            if schema:
                request_kwargs["response_format"] = {"type": "json_schema", "json_schema": schema}

            response = client.messages.create(**request_kwargs)
            return response.content[0].text

        except Exception as e:
            agent_logger.error(f"Anthropic API call failed: {str(e)}")
            raise APIException(str(e), retryable=True)

    async def _call_openai(
        self,
        messages: List[Dict[str, Any]],
        schema: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> str:
        """
        Call OpenAI-compatible API.

        Args:
            messages: Message list
            schema: Optional JSON schema
            **kwargs: Additional parameters

        Returns:
            Response string
        """
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url or "https://api.openai.com/v1",
            )

            request_kwargs = {
                "model": self.model_config.get("model", "gpt-4o"),
                "max_tokens": self.model_config.get("max_tokens", 4096),
                "temperature": self.model_config.get("temperature", 0.7),
                "messages": messages,
            }

            if schema:
                request_kwargs["response_format"] = {"type": "json_schema", "json_schema": schema}

            response = client.chat.completions.create(**request_kwargs)
            return response.choices[0].message.content

        except Exception as e:
            agent_logger.error(f"OpenAI API call failed: {str(e)}")
            raise APIException(str(e), retryable=True)

    def _format_prompt(self, **kwargs) -> str:
        """
        Format input parameters into prompt text.

        Args:
            **kwargs: Input parameters

        Returns:
            Formatted prompt string
        """
        raise NotImplementedError("Subclasses must implement _format_prompt()")

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured output.

        Args:
            response: LLM response string

        Returns:
            Parsed response dictionary
        """
        raise NotImplementedError("Subclasses must implement _parse_response()")

