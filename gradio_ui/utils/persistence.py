"""Task persistence and history management"""

import json
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
import threading

logger = logging.getLogger(__name__)


@dataclass
class TaskRecord:
    """Task execution record"""

    task_id: str
    description: str
    input_params: Dict[str, Any]
    output_result: Optional[Dict[str, Any]]
    status: str  # pending, running, completed, failed
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    duration_seconds: float
    error_message: Optional[str]
    action_log: List[Dict[str, Any]]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class TaskDatabase:
    """SQLite-based task database"""

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize task database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or Path.home() / ".automate" / "tasks.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Thread-local storage for connections
        self._local = threading.local()

        # Initialize database
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection"""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self.db_path))
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _init_db(self) -> None:
        """Initialize database schema"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                input_params TEXT NOT NULL,
                output_result TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                duration_seconds REAL DEFAULT 0,
                error_message TEXT,
                action_log TEXT,
                metadata TEXT,
                created_index TEXT NOT NULL
            )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_created_at
            ON tasks(created_at DESC)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_status
            ON tasks(status)
        """
        )

        conn.commit()
        logger.debug(f"Database initialized: {self.db_path}")

    def save_task(self, record: TaskRecord) -> None:
        """
        Save task record.

        Args:
            record: TaskRecord to save
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO tasks
                (id, description, input_params, output_result, status, created_at,
                 started_at, completed_at, duration_seconds, error_message, action_log,
                 metadata, created_index)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    record.task_id,
                    record.description,
                    json.dumps(record.input_params),
                    json.dumps(record.output_result) if record.output_result else None,
                    record.status,
                    record.created_at,
                    record.started_at,
                    record.completed_at,
                    record.duration_seconds,
                    record.error_message,
                    json.dumps(record.action_log),
                    json.dumps(record.metadata),
                    record.created_at,
                ),
            )

            conn.commit()
            logger.debug(f"Task saved: {record.task_id}")

        except Exception as e:
            logger.error(f"Failed to save task: {str(e)}")

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        """
        Get task record.

        Args:
            task_id: Task ID

        Returns:
            TaskRecord or None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return TaskRecord(
                task_id=row["id"],
                description=row["description"],
                input_params=json.loads(row["input_params"]),
                output_result=json.loads(row["output_result"]) if row["output_result"] else None,
                status=row["status"],
                created_at=row["created_at"],
                started_at=row["started_at"],
                completed_at=row["completed_at"],
                duration_seconds=row["duration_seconds"],
                error_message=row["error_message"],
                action_log=json.loads(row["action_log"]),
                metadata=json.loads(row["metadata"]),
            )

        except Exception as e:
            logger.error(f"Failed to get task: {str(e)}")
            return None

    def list_tasks(
        self, status: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[TaskRecord]:
        """
        List tasks.

        Args:
            status: Filter by status
            limit: Maximum results
            offset: Offset

        Returns:
            List of TaskRecords
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if status:
                cursor.execute(
                    """
                    SELECT * FROM tasks
                    WHERE status = ?
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                """,
                    (status, limit, offset),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM tasks
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                """,
                    (limit, offset),
                )

            tasks = []
            for row in cursor.fetchall():
                tasks.append(
                    TaskRecord(
                        task_id=row["id"],
                        description=row["description"],
                        input_params=json.loads(row["input_params"]),
                        output_result=json.loads(row["output_result"]),
                        status=row["status"],
                        created_at=row["created_at"],
                        started_at=row["started_at"],
                        completed_at=row["completed_at"],
                        duration_seconds=row["duration_seconds"],
                        error_message=row["error_message"],
                        action_log=json.loads(row["action_log"]),
                        metadata=json.loads(row["metadata"]),
                    )
                )

            return tasks

        except Exception as e:
            logger.error(f"Failed to list tasks: {str(e)}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get task statistics.

        Returns:
            Statistics dictionary
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Get status counts
            cursor.execute(
                """
                SELECT status, COUNT(*) as count
                FROM tasks
                GROUP BY status
            """
            )

            status_counts = {row[0]: row[1] for row in cursor.fetchall()}

            # Get average duration
            cursor.execute(
                """
                SELECT AVG(duration_seconds) as avg_duration
                FROM tasks
                WHERE status = 'completed'
            """
            )

            avg_duration = cursor.fetchone()[0] or 0.0

            return {
                "total_tasks": sum(status_counts.values()),
                "status_counts": status_counts,
                "average_duration": avg_duration,
                "success_rate": status_counts.get("completed", 0) / sum(status_counts.values())
                if status_counts
                else 0,
            }

        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}

    def delete_old_tasks(self, days: int = 30) -> int:
        """
        Delete tasks older than specified days.

        Args:
            days: Days to keep

        Returns:
            Number of deleted tasks
        """
        try:
            from datetime import datetime, timedelta

            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM tasks WHERE created_at < ?", (cutoff_date,))
            conn.commit()

            deleted_count = cursor.rowcount
            logger.info(f"Deleted {deleted_count} tasks older than {days} days")

            return deleted_count

        except Exception as e:
            logger.error(f"Failed to delete old tasks: {str(e)}")
            return 0

    def close(self) -> None:
        """Close database connection"""
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None


class TaskHistory:
    """Manage task history and caching"""

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize task history.

        Args:
            db_path: Database path
        """
        self.db = TaskDatabase(db_path)
        self._memory_cache: Dict[str, TaskRecord] = {}

    def save_task(self, record: TaskRecord) -> None:
        """Save task to database and cache"""
        self.db.save_task(record)
        self._memory_cache[record.task_id] = record

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        """Get task from cache or database"""
        if task_id in self._memory_cache:
            return self._memory_cache[task_id]

        record = self.db.get_task(task_id)
        if record:
            self._memory_cache[task_id] = record

        return record

    def list_recent_tasks(self, count: int = 10) -> List[TaskRecord]:
        """Get recent tasks"""
        return self.db.list_tasks(limit=count)

    def get_stats(self) -> Dict[str, Any]:
        """Get history statistics"""
        return self.db.get_statistics()

    def clear_cache(self) -> None:
        """Clear in-memory cache"""
        self._memory_cache.clear()

    def cleanup_old_tasks(self, days: int = 30) -> int:
        """Clean up old tasks"""
        count = self.db.delete_old_tasks(days)
        self.clear_cache()
        return count


# Global task history instance
_task_history: Optional[TaskHistory] = None


def get_task_history() -> TaskHistory:
    """Get global task history instance"""
    global _task_history
    if _task_history is None:
        _task_history = TaskHistory()
    return _task_history
