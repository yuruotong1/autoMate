"""Caching and performance optimization utilities"""

import time
import logging
from typing import Dict, Any, Optional, Callable, TypeVar, List
from datetime import datetime, timedelta
from functools import wraps
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class CacheEntry:
    """Cache entry with metadata"""

    key: str
    value: Any
    timestamp: datetime
    ttl_seconds: Optional[int] = None
    hit_count: int = 0
    access_time: Optional[datetime] = None

    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if self.ttl_seconds is None:
            return False

        elapsed = (datetime.now() - self.timestamp).total_seconds()
        return elapsed > self.ttl_seconds

    def record_hit(self) -> None:
        """Record cache hit"""
        self.hit_count += 1
        self.access_time = datetime.now()


class MemoryCache:
    """In-memory cache with TTL support"""

    def __init__(self, max_size: int = 1000):
        """
        Initialize memory cache.

        Args:
            max_size: Maximum number of entries
        """
        self.max_size = max_size
        self._cache: Dict[str, CacheEntry] = {}
        self.total_hits = 0
        self.total_misses = 0

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if key not in self._cache:
            self.total_misses += 1
            return None

        entry = self._cache[key]

        if entry.is_expired():
            del self._cache[key]
            self.total_misses += 1
            return None

        entry.record_hit()
        self.total_hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds
        """
        # Evict oldest entry if at capacity
        if len(self._cache) >= self.max_size:
            oldest_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].timestamp,
            )
            del self._cache[oldest_key]

        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            timestamp=datetime.now(),
            ttl_seconds=ttl_seconds,
        )

    def clear(self) -> None:
        """Clear cache"""
        self._cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.total_hits + self.total_misses

        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self.total_hits,
            "misses": self.total_misses,
            "hit_rate": self.total_hits / total_requests if total_requests > 0 else 0,
        }


class DiskCache:
    """Disk-based cache with serialization"""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize disk cache.

        Args:
            cache_dir: Cache directory path
        """
        self.cache_dir = cache_dir or Path.home() / ".automate" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key"""
        # Hash key to create safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str, ttl_seconds: Optional[int] = None) -> Optional[Any]:
        """
        Get value from disk cache.

        Args:
            key: Cache key
            ttl_seconds: Maximum age in seconds

        Returns:
            Cached value or None
        """
        try:
            cache_path = self._get_cache_path(key)

            if not cache_path.exists():
                return None

            # Check TTL
            if ttl_seconds:
                file_age = time.time() - cache_path.stat().st_mtime
                if file_age > ttl_seconds:
                    cache_path.unlink()
                    return None

            with open(cache_path, "r") as f:
                data = json.load(f)

            logger.debug(f"Cache hit: {key}")
            return data.get("value")

        except Exception as e:
            logger.error(f"Failed to read cache: {str(e)}")
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Set value in disk cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        try:
            cache_path = self._get_cache_path(key)

            with open(cache_path, "w") as f:
                json.dump(
                    {"key": key, "value": value, "timestamp": datetime.now().isoformat()},
                    f,
                )

            logger.debug(f"Cache set: {key}")

        except Exception as e:
            logger.error(f"Failed to write cache: {str(e)}")

    def clear(self) -> None:
        """Clear all cache files"""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except Exception as e:
                logger.error(f"Failed to delete cache file: {str(e)}")


class CacheDecorator:
    """Decorator for caching function results"""

    def __init__(self, ttl_seconds: int = 300, cache: Optional[MemoryCache] = None):
        """
        Initialize cache decorator.

        Args:
            ttl_seconds: Time to live for cached results
            cache: Cache instance to use
        """
        self.ttl_seconds = ttl_seconds
        self.cache = cache or MemoryCache()

    def __call__(self, func: Callable) -> Callable:
        """
        Decorate function for caching.

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Check cache
            cached_value = self.cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Using cached result for {func.__name__}")
                return cached_value

            # Call function
            result = func(*args, **kwargs)

            # Cache result
            self.cache.set(cache_key, result, self.ttl_seconds)

            return result

        return wrapper


# Global cache instances
_memory_cache = MemoryCache()
_disk_cache = DiskCache()


def get_memory_cache() -> MemoryCache:
    """Get global memory cache instance"""
    return _memory_cache


def get_disk_cache() -> DiskCache:
    """Get global disk cache instance"""
    return _disk_cache


def cache_result(ttl_seconds: int = 300):
    """
    Decorator to cache function results.

    Args:
        ttl_seconds: Time to live for cached results

    Returns:
        Decorator function
    """
    return CacheDecorator(ttl_seconds=ttl_seconds, cache=_memory_cache)


class PrefetchCache:
    """Prefetch cache for predictive loading"""

    def __init__(self, cache: MemoryCache):
        """
        Initialize prefetch cache.

        Args:
            cache: Cache instance
        """
        self.cache = cache
        self.prefetch_queue: List[tuple] = []

    def add_prefetch(self, key: str, fetch_func: Callable, ttl_seconds: Optional[int] = None) -> None:
        """
        Add item to prefetch queue.

        Args:
            key: Cache key
            fetch_func: Function to fetch value
            ttl_seconds: TTL for cached value
        """
        self.prefetch_queue.append((key, fetch_func, ttl_seconds))

    def execute_prefetch(self) -> None:
        """Execute all prefetch operations"""
        for key, fetch_func, ttl_seconds in self.prefetch_queue:
            try:
                value = fetch_func()
                self.cache.set(key, value, ttl_seconds)
                logger.debug(f"Prefetched: {key}")
            except Exception as e:
                logger.warning(f"Prefetch failed for {key}: {str(e)}")

        self.prefetch_queue.clear()
