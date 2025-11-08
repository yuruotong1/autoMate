"""Error handling and retry utilities for autoMate"""

import asyncio
import logging
from typing import Callable, Any, Optional, Type, Tuple, List
from functools import wraps
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry behavior"""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ):
        """
        Initialize retry configuration.

        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay between retries
            exponential_base: Base for exponential backoff
            jitter: Whether to add random jitter to delay
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """
        Calculate delay for retry attempt.

        Args:
            attempt: Attempt number (0-indexed)

        Returns:
            Delay in seconds
        """
        delay = self.initial_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            import random

            delay = delay * (0.5 + random.random())

        return delay


class AutoMateException(Exception):
    """Base exception for autoMate"""

    pass


class APIException(AutoMateException):
    """Exception from API calls"""

    def __init__(self, message: str, status_code: Optional[int] = None, retryable: bool = False):
        """
        Initialize API exception.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
            retryable: Whether the error is retryable
        """
        super().__init__(message)
        self.status_code = status_code
        self.retryable = retryable
        self.timestamp = datetime.now()


class ToolException(AutoMateException):
    """Exception from tool execution"""

    def __init__(self, message: str, tool_name: str, retryable: bool = True):
        """
        Initialize tool exception.

        Args:
            message: Error message
            tool_name: Name of tool that failed
            retryable: Whether the error is retryable
        """
        super().__init__(message)
        self.tool_name = tool_name
        self.retryable = retryable
        self.timestamp = datetime.now()


class VisionException(AutoMateException):
    """Exception from vision processing"""

    pass


class TimeoutException(AutoMateException):
    """Exception for operation timeouts"""

    pass


def retry_with_backoff(
    retry_config: Optional[RetryConfig] = None,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None,
):
    """
    Decorator for retrying async functions with exponential backoff.

    Args:
        retry_config: Retry configuration
        exceptions: Tuple of exceptions to catch and retry
        on_retry: Callback function called on each retry

    Returns:
        Decorated function
    """
    if retry_config is None:
        retry_config = RetryConfig()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(retry_config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < retry_config.max_retries:
                        delay = retry_config.get_delay(attempt)

                        if on_retry:
                            on_retry(attempt + 1, e)

                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {retry_config.max_retries + 1} attempts failed for {func.__name__}"
                        )

            raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(retry_config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < retry_config.max_retries:
                        delay = retry_config.get_delay(attempt)

                        if on_retry:
                            on_retry(attempt + 1, e)

                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {retry_config.max_retries + 1} attempts failed for {func.__name__}"
                        )

            raise last_exception

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def with_timeout(timeout_seconds: float):
    """
    Decorator to add timeout to async function.

    Args:
        timeout_seconds: Timeout in seconds

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout_seconds)
            except asyncio.TimeoutError:
                raise TimeoutException(f"{func.__name__} exceeded timeout of {timeout_seconds}s")

        return wrapper

    return decorator


class CircuitBreaker:
    """Circuit breaker pattern for failure handling"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Type[Exception] = Exception,
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures to trigger break
            recovery_timeout: Seconds before attempting recovery
            expected_exception: Exception type to catch
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.is_open = False

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If circuit is open or function fails
        """
        if self.is_open:
            if self._should_attempt_reset():
                self.is_open = False
                self.failure_count = 0
                logger.info("Circuit breaker attempting recovery")
            else:
                raise AutoMateException("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            return result
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.is_open = True
                logger.error(f"Circuit breaker opened after {self.failure_count} failures")

            raise e

    async def acall(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute async function with circuit breaker protection.

        Args:
            func: Async function to call
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        if self.is_open:
            if self._should_attempt_reset():
                self.is_open = False
                self.failure_count = 0
                logger.info("Circuit breaker attempting recovery")
            else:
                raise AutoMateException("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            self.failure_count = 0
            return result
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.is_open = True
                logger.error(f"Circuit breaker opened after {self.failure_count} failures")

            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery"""
        if self.last_failure_time is None:
            return True

        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout


class RateLimiter:
    """Rate limiter for API calls"""

    def __init__(self, max_calls: int = 10, time_window: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum calls per time window
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.call_times: List[datetime] = []

    def is_allowed(self) -> bool:
        """
        Check if call is allowed.

        Returns:
            True if call is within rate limit
        """
        now = datetime.now()

        # Remove old calls outside the time window
        self.call_times = [
            ct for ct in self.call_times if (now - ct).total_seconds() < self.time_window
        ]

        if len(self.call_times) < self.max_calls:
            self.call_times.append(now)
            return True

        return False

    def wait_if_needed(self) -> float:
        """
        Wait if necessary to respect rate limit.

        Returns:
            Time waited in seconds
        """
        if self.is_allowed():
            return 0.0

        # Calculate wait time
        oldest_call = self.call_times[0]
        elapsed = (datetime.now() - oldest_call).total_seconds()
        wait_time = self.time_window - elapsed

        if wait_time > 0:
            logger.info(f"Rate limited, waiting {wait_time:.2f}s")
            time.sleep(wait_time)

        return wait_time

    async def await_if_needed(self) -> float:
        """
        Async wait if necessary to respect rate limit.

        Returns:
            Time waited in seconds
        """
        if self.is_allowed():
            return 0.0

        oldest_call = self.call_times[0]
        elapsed = (datetime.now() - oldest_call).total_seconds()
        wait_time = self.time_window - elapsed

        if wait_time > 0:
            logger.info(f"Rate limited, waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)

        return wait_time


def create_error_context(
    error: Exception, context: Optional[dict] = None
) -> dict:
    """
    Create detailed error context for logging.

    Args:
        error: Exception that occurred
        context: Additional context information

    Returns:
        Error context dictionary
    """
    error_context = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.now().isoformat(),
        "traceback": None,
    }

    if context:
        error_context.update(context)

    import traceback

    error_context["traceback"] = traceback.format_exc()

    return error_context
