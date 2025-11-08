"""Utility modules for autoMate"""

from gradio_ui.utils.error_handler import (
    RetryConfig,
    AutoMateException,
    APIException,
    ToolException,
    VisionException,
    TimeoutException,
    retry_with_backoff,
    with_timeout,
    CircuitBreaker,
    RateLimiter,
    create_error_context,
)

from gradio_ui.utils.logger import setup_logging, logger, create_task_logger

from gradio_ui.utils.monitoring import (
    MetricPoint,
    TaskMetrics,
    PerformanceMonitor,
    TaskMonitor,
    get_performance_monitor,
    get_task_monitor,
)

from gradio_ui.utils.validation import (
    Validator,
    InputSanitizer,
    ValidationError,
)

from gradio_ui.utils.persistence import (
    TaskRecord,
    TaskDatabase,
    TaskHistory,
    get_task_history,
)

__all__ = [
    # Error handling
    "RetryConfig",
    "AutoMateException",
    "APIException",
    "ToolException",
    "VisionException",
    "TimeoutException",
    "retry_with_backoff",
    "with_timeout",
    "CircuitBreaker",
    "RateLimiter",
    "create_error_context",
    # Logging
    "setup_logging",
    "logger",
    "create_task_logger",
    # Monitoring
    "MetricPoint",
    "TaskMetrics",
    "PerformanceMonitor",
    "TaskMonitor",
    "get_performance_monitor",
    "get_task_monitor",
    # Validation
    "Validator",
    "InputSanitizer",
    "ValidationError",
    # Persistence
    "TaskRecord",
    "TaskDatabase",
    "TaskHistory",
    "get_task_history",
]
