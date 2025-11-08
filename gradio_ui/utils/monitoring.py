"""Monitoring and metrics collection for autoMate"""

import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """Single metric data point"""

    timestamp: str
    value: float
    unit: str


@dataclass
class TaskMetrics:
    """Metrics for a task execution"""

    task_id: str
    task_description: str
    start_time: str
    end_time: Optional[str] = None
    duration_seconds: float = 0.0
    status: str = "running"  # running, completed, failed
    total_actions: int = 0
    vision_calls: int = 0
    llm_calls: int = 0
    tool_executions: int = 0
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def mark_complete(self, status: str = "completed"):
        """Mark task as complete"""
        self.end_time = datetime.now().isoformat()
        self.status = status
        self.duration_seconds = (
            datetime.fromisoformat(self.end_time) - datetime.fromisoformat(self.start_time)
        ).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class PerformanceMonitor:
    """Monitor performance metrics"""

    def __init__(self, name: str = "automate"):
        """
        Initialize performance monitor.

        Args:
            name: Monitor name
        """
        self.name = name
        self.metrics: Dict[str, List[MetricPoint]] = {}
        self.start_times: Dict[str, float] = {}

    def start_timer(self, operation: str) -> None:
        """
        Start timing an operation.

        Args:
            operation: Operation name
        """
        self.start_times[operation] = time.time()
        logger.debug(f"Started timing: {operation}")

    def end_timer(self, operation: str, unit: str = "ms") -> float:
        """
        End timing an operation.

        Args:
            operation: Operation name
            unit: Time unit (ms, s)

        Returns:
            Elapsed time in specified unit
        """
        if operation not in self.start_times:
            logger.warning(f"No start time found for: {operation}")
            return 0.0

        elapsed = time.time() - self.start_times[operation]

        # Convert to specified unit
        if unit == "ms":
            elapsed = elapsed * 1000

        # Record metric
        self.record_metric(operation, elapsed, unit)

        del self.start_times[operation]
        logger.debug(f"Ended timing: {operation} - {elapsed:.2f}{unit}")

        return elapsed

    def record_metric(self, metric_name: str, value: float, unit: str = "") -> None:
        """
        Record a metric value.

        Args:
            metric_name: Metric name
            value: Metric value
            unit: Unit of measurement
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []

        point = MetricPoint(
            timestamp=datetime.now().isoformat(),
            value=value,
            unit=unit,
        )
        self.metrics[metric_name].append(point)

    def get_metric_stats(self, metric_name: str) -> Dict[str, float]:
        """
        Get statistics for a metric.

        Args:
            metric_name: Metric name

        Returns:
            Dictionary with min, max, avg, count
        """
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return {}

        values = [p.value for p in self.metrics[metric_name]]

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "total": sum(values),
        }

    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all metrics.

        Returns:
            Dictionary of all metrics and their statistics
        """
        result = {}
        for metric_name in self.metrics:
            result[metric_name] = self.get_metric_stats(metric_name)
        return result

    def clear_metrics(self) -> None:
        """Clear all recorded metrics"""
        self.metrics = {}
        self.start_times = {}


class TaskMonitor:
    """Monitor task execution"""

    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize task monitor.

        Args:
            log_dir: Directory to save task logs
        """
        self.log_dir = log_dir or Path.home() / ".automate" / "tasks"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.current_task: Optional[TaskMetrics] = None
        self.task_history: List[TaskMetrics] = []

    def start_task(self, task_id: str, description: str) -> TaskMetrics:
        """
        Start monitoring a task.

        Args:
            task_id: Task identifier
            description: Task description

        Returns:
            TaskMetrics object
        """
        self.current_task = TaskMetrics(
            task_id=task_id,
            task_description=description,
            start_time=datetime.now().isoformat(),
        )
        logger.info(f"Task started: {task_id} - {description}")
        return self.current_task

    def end_task(self, status: str = "completed") -> Optional[TaskMetrics]:
        """
        End monitoring current task.

        Args:
            status: Task status (completed, failed, cancelled)

        Returns:
            Completed TaskMetrics object
        """
        if not self.current_task:
            logger.warning("No current task to end")
            return None

        self.current_task.mark_complete(status)
        self.task_history.append(self.current_task)

        # Save task log
        self._save_task_log(self.current_task)

        logger.info(
            f"Task ended: {self.current_task.task_id} - "
            f"Status: {status}, Duration: {self.current_task.duration_seconds:.2f}s"
        )

        current = self.current_task
        self.current_task = None
        return current

    def record_action(self) -> None:
        """Record an action in current task"""
        if self.current_task:
            self.current_task.total_actions += 1

    def record_vision_call(self) -> None:
        """Record vision agent call"""
        if self.current_task:
            self.current_task.vision_calls += 1

    def record_llm_call(self) -> None:
        """Record LLM API call"""
        if self.current_task:
            self.current_task.llm_calls += 1

    def record_tool_execution(self) -> None:
        """Record tool execution"""
        if self.current_task:
            self.current_task.tool_executions += 1

    def record_error(self, error_message: str) -> None:
        """Record an error during task"""
        if self.current_task:
            self.current_task.errors.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "message": error_message,
                }
            )

    def record_metric(self, key: str, value: Any) -> None:
        """Record a custom metric"""
        if self.current_task:
            self.current_task.metrics[key] = value

    def _save_task_log(self, task: TaskMetrics) -> None:
        """Save task log to file"""
        log_file = self.log_dir / f"task_{task.task_id}.json"

        try:
            with open(log_file, "w") as f:
                json.dump(task.to_dict(), f, indent=2)
            logger.debug(f"Task log saved: {log_file}")
        except Exception as e:
            logger.error(f"Failed to save task log: {str(e)}")

    def get_task_history(self, hours: int = 24) -> List[TaskMetrics]:
        """
        Get task history from past N hours.

        Args:
            hours: Number of hours to look back

        Returns:
            List of TaskMetrics
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)

        return [
            task
            for task in self.task_history
            if datetime.fromisoformat(task.start_time) > cutoff_time
        ]

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.task_history:
            return {}

        completed = [t for t in self.task_history if t.status == "completed"]
        failed = [t for t in self.task_history if t.status == "failed"]

        if not completed:
            return {
                "total_tasks": len(self.task_history),
                "completed": 0,
                "failed": len(failed),
                "success_rate": 0.0,
            }

        durations = [t.duration_seconds for t in completed]
        total_actions = sum(t.total_actions for t in completed)

        return {
            "total_tasks": len(self.task_history),
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": len(completed) / len(self.task_history),
            "avg_duration": sum(durations) / len(durations),
            "total_actions": total_actions,
            "avg_actions_per_task": total_actions / len(completed) if completed else 0,
            "total_vision_calls": sum(t.vision_calls for t in completed),
            "total_llm_calls": sum(t.llm_calls for t in completed),
        }


# Global monitor instances
_perf_monitor = PerformanceMonitor()
_task_monitor = TaskMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor"""
    return _perf_monitor


def get_task_monitor() -> TaskMonitor:
    """Get global task monitor"""
    return _task_monitor
