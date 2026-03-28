"""
OpenAI-compatible LLM client for autoMate.

Works with any OpenAI-compatible API endpoint, including:
  - OpenAI (gpt-4o, gpt-4.1, o3, etc.)
  - Azure OpenAI
  - Anthropic Claude (via OpenAI-compatible proxy, e.g. OpenRouter)
  - Google Gemini (via OpenAI-compatible endpoint)
  - DeepSeek, Qwen, GLM, etc.
  - OpenRouter (https://openrouter.ai/api/v1)
  - Groq (https://api.groq.com/openai/v1)
  - Ollama (http://localhost:11434/v1)
  - Any other OpenAI-compatible provider
"""

import json
import os
import re
from typing import Type

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Global configuration (updated by configure() at runtime)
# ---------------------------------------------------------------------------
_base_url: str = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
_api_key: str = os.environ.get("OPENAI_API_KEY", "")
_model: str = os.environ.get("OPENAI_MODEL", "gpt-4o")


def configure(base_url: str, api_key: str, model: str) -> None:
    """Configure the global LLM client settings at runtime."""
    global _base_url, _api_key, _model
    _base_url = base_url or _base_url
    _api_key = api_key or _api_key
    _model = model or _model


def _get_client():
    from openai import OpenAI
    return OpenAI(base_url=_base_url, api_key=_api_key)


# ---------------------------------------------------------------------------
# Main entry point (drop-in replacement for xbrain.core.chat.run)
# ---------------------------------------------------------------------------

def run(messages: list, user_prompt: str, response_format: Type[BaseModel]) -> str:
    """
    Call the LLM with structured output.

    Compatible with any OpenAI-compatible API.  Falls back gracefully:
      1. Native structured-output  (client.beta.chat.completions.parse)
      2. JSON-mode                 (response_format={"type":"json_object"})
      3. Plain text + JSON extract (last resort)

    Side effect: appends the assistant response to `messages` in-place,
    mirroring the original xbrain behaviour so the rest of the codebase
    continues to work unchanged.

    Returns: JSON string of the LLM response.
    """
    client = _get_client()
    api_messages = [{"role": "system", "content": user_prompt}] + messages

    response_text = _call_with_structured_output(client, _model, api_messages, response_format)

    # Append assistant reply to the caller's message list (in-place side effect)
    messages.append({"role": "assistant", "content": response_text})

    return response_text


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _call_with_structured_output(
    client,
    model: str,
    messages: list,
    response_format: Type[BaseModel],
) -> str:
    """Try progressively less strict output strategies until one succeeds."""

    # ── Strategy 1: native structured output ──────────────────────────────
    try:
        resp = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_format,
        )
        content = resp.choices[0].message.content
        if content:
            return content
        parsed = resp.choices[0].message.parsed
        if parsed is not None:
            return parsed.model_dump_json()
    except Exception as e:
        print(f"[LLMClient] Structured output unavailable ({e}); trying JSON mode")

    # ── Strategy 2: json_object mode with schema hint ─────────────────────
    try:
        schema = response_format.model_json_schema()
        schema_hint = (
            "\n\nIMPORTANT: You MUST respond with valid JSON that exactly matches "
            f"this schema:\n{json.dumps(schema, ensure_ascii=False, indent=2)}"
        )
        json_messages = _inject_schema_hint(messages, schema_hint)
        resp = client.chat.completions.create(
            model=model,
            messages=json_messages,
            response_format={"type": "json_object"},
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"[LLMClient] JSON mode unavailable ({e}); trying plain text fallback")

    # ── Strategy 3: plain text, extract JSON manually ─────────────────────
    schema = response_format.model_json_schema()
    schema_hint = (
        "\n\nIMPORTANT: Respond ONLY with valid JSON matching this schema "
        f"(no markdown, no extra text):\n{json.dumps(schema, ensure_ascii=False)}"
    )
    plain_messages = _inject_schema_hint(messages, schema_hint)
    resp = client.chat.completions.create(model=model, messages=plain_messages)
    return _extract_json(resp.choices[0].message.content)


def _inject_schema_hint(messages: list, hint: str) -> list:
    """Append the JSON-schema hint to the system message (non-destructive copy)."""
    result = []
    injected = False
    for msg in messages:
        if not injected and msg.get("role") == "system":
            result.append({**msg, "content": msg["content"] + hint})
            injected = True
        else:
            result.append(msg)
    if not injected:
        result.append({"role": "system", "content": hint})
    return result


def _extract_json(text: str) -> str:
    """Extract a JSON object from text that may contain markdown fences."""
    # Remove ```json ... ``` fences
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    # Find the outermost { ... } block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text
