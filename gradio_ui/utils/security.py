"""Security hardening utilities for autoMate"""

import logging
import secrets
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class SecurityManager:
    """Manage security policies and enforcement"""

    def __init__(self):
        """Initialize security manager"""
        self.failed_attempts: Dict[str, List[datetime]] = {}
        self.blocked_ips: Dict[str, datetime] = {}
        self.rate_limits: Dict[str, int] = {}

        # Security settings
        self.max_login_attempts = 5
        self.lockout_duration = 15 * 60  # 15 minutes
        self.password_min_length = 12
        self.api_key_min_length = 20

    def check_rate_limit(self, key: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
        """
        Check if request is within rate limit.

        Args:
            key: Rate limit key (IP, user, API key)
            max_requests: Max requests per window
            window_seconds: Time window in seconds

        Returns:
            True if within limit
        """
        if key not in self.rate_limits:
            self.rate_limits[key] = 0

        self.rate_limits[key] += 1

        if self.rate_limits[key] > max_requests:
            logger.warning(f"Rate limit exceeded for: {key}")
            return False

        return True

    def validate_input_safety(self, text: str, max_length: int = 10000) -> bool:
        """
        Validate input for security issues.

        Args:
            text: Input text to validate
            max_length: Maximum allowed length

        Returns:
            True if input is safe
        """
        if not isinstance(text, str):
            return False

        # Check length
        if len(text) > max_length:
            logger.warning("Input exceeds maximum length")
            return False

        # Check for null bytes
        if "\x00" in text:
            logger.warning("Null bytes detected in input")
            return False

        # Check for malicious patterns
        dangerous_patterns = [
            r"<script[^>]*>",  # Script tags
            r"onclick=",  # Inline event handlers
            r"onerror=",
            r"eval\(",  # eval calls
            r"__import__",  # Python import
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"Dangerous pattern detected: {pattern}")
                return False

        return True

    def hash_api_key(self, api_key: str) -> str:
        """
        Hash API key for storage.

        Args:
            api_key: API key to hash

        Returns:
            Hashed API key
        """
        return hashlib.sha256(api_key.encode()).hexdigest()

    def mask_api_key(self, api_key: str, visible_chars: int = 4) -> str:
        """
        Create masked version of API key for display.

        Args:
            api_key: API key to mask
            visible_chars: Number of visible characters at end

        Returns:
            Masked API key
        """
        if len(api_key) <= visible_chars:
            return "*" * len(api_key)

        hidden_length = len(api_key) - visible_chars
        return "*" * hidden_length + api_key[-visible_chars:]

    def sanitize_log_message(self, message: str) -> str:
        """
        Sanitize log messages to remove sensitive data.

        Args:
            message: Log message to sanitize

        Returns:
            Sanitized message
        """
        # Mask API keys (pattern: sk-... or similar)
        message = re.sub(r"sk-[a-zA-Z0-9]{40,}", "sk-***", message)

        # Mask email addresses
        message = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "***@***.***", message)

        # Mask passwords
        message = re.sub(r"password['\"]?\s*[:=]\s*['\"]?[^'\"]+['\"]?", 'password="***"', message)

        # Mask tokens
        message = re.sub(r"token['\"]?\s*[:=]\s*['\"]?[^'\"]+['\"]?", 'token="***"', message)

        return message

    def validate_api_key_format(self, api_key: str) -> bool:
        """
        Validate API key format.

        Args:
            api_key: API key to validate

        Returns:
            True if valid format
        """
        if not isinstance(api_key, str):
            return False

        # Check length
        if len(api_key) < self.api_key_min_length:
            return False

        # Check for alphanumeric and common separators
        if not re.match(r"^[a-zA-Z0-9\-_]*$", api_key):
            return False

        return True


class EncryptionManager:
    """Manage encryption for sensitive data"""

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate a secure random token.

        Args:
            length: Token length

        Returns:
            Secure token
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple:
        """
        Hash password with salt.

        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)

        Returns:
            (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)

        # Use PBKDF2 for secure hashing
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000,  # iterations
        )

        return hashlib.sha256(hashed).hexdigest(), salt

    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """
        Verify password against hash.

        Args:
            password: Password to verify
            hashed: Hashed password
            salt: Salt used in hashing

        Returns:
            True if password matches
        """
        test_hashed, _ = EncryptionManager.hash_password(password, salt)
        return test_hashed == hashed


class AccessControl:
    """Manage access control and permissions"""

    def __init__(self):
        """Initialize access control"""
        self.permissions: Dict[str, List[str]] = {}
        self.roles: Dict[str, List[str]] = {}

    def add_permission(self, role: str, permission: str) -> None:
        """
        Add permission to role.

        Args:
            role: Role name
            permission: Permission name
        """
        if role not in self.roles:
            self.roles[role] = []

        if permission not in self.roles[role]:
            self.roles[role].append(permission)

    def has_permission(self, role: str, permission: str) -> bool:
        """
        Check if role has permission.

        Args:
            role: Role name
            permission: Permission name

        Returns:
            True if role has permission
        """
        if role not in self.roles:
            return False

        return permission in self.roles[role]

    def revoke_permission(self, role: str, permission: str) -> None:
        """
        Revoke permission from role.

        Args:
            role: Role name
            permission: Permission name
        """
        if role in self.roles and permission in self.roles[role]:
            self.roles[role].remove(permission)

    def create_role(self, role: str, permissions: List[str] = None) -> None:
        """
        Create new role with permissions.

        Args:
            role: Role name
            permissions: List of permissions
        """
        self.roles[role] = permissions or []


# Global security manager instance
_security_manager: Optional[SecurityManager] = None


def get_security_manager() -> SecurityManager:
    """Get global security manager instance"""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager
