"""Input validation and type checking utilities"""

import re
import logging
from typing import Any, Optional, Dict, List, Union, Type
from pathlib import Path

logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """Validation error"""

    pass


class Validator:
    """Input validator"""

    @staticmethod
    def validate_string(value: Any, min_length: int = 0, max_length: Optional[int] = None) -> str:
        """
        Validate string input.

        Args:
            value: Value to validate
            min_length: Minimum length
            max_length: Maximum length

        Returns:
            Validated string

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise ValidationError(f"Expected string, got {type(value).__name__}")

        if len(value) < min_length:
            raise ValidationError(f"String must be at least {min_length} characters")

        if max_length and len(value) > max_length:
            raise ValidationError(f"String must not exceed {max_length} characters")

        return value

    @staticmethod
    def validate_integer(
        value: Any, min_value: Optional[int] = None, max_value: Optional[int] = None
    ) -> int:
        """
        Validate integer input.

        Args:
            value: Value to validate
            min_value: Minimum value
            max_value: Maximum value

        Returns:
            Validated integer

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, int):
            raise ValidationError(f"Expected integer, got {type(value).__name__}")

        if min_value is not None and value < min_value:
            raise ValidationError(f"Value must be at least {min_value}")

        if max_value is not None and value > max_value:
            raise ValidationError(f"Value must not exceed {max_value}")

        return value

    @staticmethod
    def validate_float(
        value: Any, min_value: Optional[float] = None, max_value: Optional[float] = None
    ) -> float:
        """
        Validate float input.

        Args:
            value: Value to validate
            min_value: Minimum value
            max_value: Maximum value

        Returns:
            Validated float

        Raises:
            ValidationError: If validation fails
        """
        try:
            val = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Expected float, got {type(value).__name__}")

        if min_value is not None and val < min_value:
            raise ValidationError(f"Value must be at least {min_value}")

        if max_value is not None and val > max_value:
            raise ValidationError(f"Value must not exceed {max_value}")

        return val

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate email address.

        Args:
            email: Email to validate

        Returns:
            Validated email

        Raises:
            ValidationError: If email is invalid
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, email):
            raise ValidationError(f"Invalid email address: {email}")

        return email

    @staticmethod
    def validate_url(url: str) -> str:
        """
        Validate URL.

        Args:
            url: URL to validate

        Returns:
            Validated URL

        Raises:
            ValidationError: If URL is invalid
        """
        pattern = r"^https?://[^\s/$.?#].[^\s]*$"

        if not re.match(pattern, url, re.IGNORECASE):
            raise ValidationError(f"Invalid URL: {url}")

        return url

    @staticmethod
    def validate_dict(
        value: Any, required_keys: Optional[List[str]] = None, allowed_keys: Optional[List[str]] = None
    ) -> Dict:
        """
        Validate dictionary.

        Args:
            value: Dictionary to validate
            required_keys: Required keys
            allowed_keys: Allowed keys

        Returns:
            Validated dictionary

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, dict):
            raise ValidationError(f"Expected dictionary, got {type(value).__name__}")

        if required_keys:
            missing = set(required_keys) - set(value.keys())
            if missing:
                raise ValidationError(f"Missing required keys: {missing}")

        if allowed_keys:
            extra = set(value.keys()) - set(allowed_keys)
            if extra:
                raise ValidationError(f"Unexpected keys: {extra}")

        return value

    @staticmethod
    def validate_list(value: Any, item_type: Optional[Type] = None, min_length: int = 0) -> List:
        """
        Validate list.

        Args:
            value: List to validate
            item_type: Expected type of items
            min_length: Minimum length

        Returns:
            Validated list

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, list):
            raise ValidationError(f"Expected list, got {type(value).__name__}")

        if len(value) < min_length:
            raise ValidationError(f"List must have at least {min_length} items")

        if item_type:
            for i, item in enumerate(value):
                if not isinstance(item, item_type):
                    raise ValidationError(
                        f"Item {i} is {type(item).__name__}, expected {item_type.__name__}"
                    )

        return value

    @staticmethod
    def validate_coordinates(coords: tuple) -> tuple:
        """
        Validate screen coordinates.

        Args:
            coords: Coordinates tuple (x, y) or (x, y, w, h)

        Returns:
            Validated coordinates

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(coords, (tuple, list)):
            raise ValidationError(f"Coordinates must be tuple or list, got {type(coords).__name__}")

        if len(coords) not in [2, 4]:
            raise ValidationError("Coordinates must be (x, y) or (x, y, w, h)")

        for i, val in enumerate(coords):
            if not isinstance(val, (int, float)):
                raise ValidationError(f"Coordinate {i} must be numeric")

            if val < 0:
                raise ValidationError(f"Coordinate {i} must be non-negative")

        return tuple(coords)

    @staticmethod
    def validate_api_key(key: str) -> str:
        """
        Validate API key format.

        Args:
            key: API key to validate

        Returns:
            Validated API key

        Raises:
            ValidationError: If key is invalid
        """
        if not isinstance(key, str):
            raise ValidationError("API key must be string")

        if len(key) < 20:
            raise ValidationError("API key appears to be invalid (too short)")

        return key

    @staticmethod
    def validate_model_config(config: Dict) -> Dict:
        """
        Validate model configuration.

        Args:
            config: Configuration dictionary

        Returns:
            Validated configuration

        Raises:
            ValidationError: If configuration is invalid
        """
        required = {"provider", "model"}
        Validator.validate_dict(config, required_keys=list(required))

        provider = config.get("provider")
        if provider not in ["openai", "anthropic", "yeka", "openai-next"]:
            raise ValidationError(f"Invalid provider: {provider}")

        model = config.get("model")
        if not isinstance(model, str) or len(model) < 1:
            raise ValidationError("Model must be non-empty string")

        temperature = config.get("temperature")
        if temperature is not None:
            Validator.validate_float(temperature, min_value=0.0, max_value=2.0)

        max_tokens = config.get("max_tokens")
        if max_tokens is not None:
            Validator.validate_integer(max_tokens, min_value=1, max_value=100000)

        return config


class InputSanitizer:
    """Sanitize user input"""

    @staticmethod
    def sanitize_string(text: str, max_length: int = 10000) -> str:
        """
        Sanitize string input.

        Args:
            text: Text to sanitize
            max_length: Maximum length

        Returns:
            Sanitized string
        """
        if not isinstance(text, str):
            text = str(text)

        # Limit length
        text = text[:max_length]

        # Remove control characters
        text = "".join(ch for ch in text if ord(ch) >= 32 or ch in "\n\t\r")

        return text.strip()

    @staticmethod
    def sanitize_path(path: str) -> Path:
        """
        Sanitize file path.

        Args:
            path: Path string to sanitize

        Returns:
            Sanitized Path object

        Raises:
            ValidationError: If path is invalid
        """
        try:
            path_obj = Path(path).resolve()

            # Check for path traversal attempts
            if ".." in str(path):
                raise ValidationError("Path traversal detected")

            return path_obj
        except Exception as e:
            raise ValidationError(f"Invalid path: {str(e)}")

    @staticmethod
    def sanitize_dict(data: Dict, max_depth: int = 5) -> Dict:
        """
        Sanitize dictionary recursively.

        Args:
            data: Dictionary to sanitize
            max_depth: Maximum nesting depth

        Returns:
            Sanitized dictionary
        """
        if max_depth <= 0:
            logger.warning("Max depth exceeded in dictionary sanitization")
            return {}

        sanitized = {}
        for key, value in data.items():
            if isinstance(key, str):
                key = InputSanitizer.sanitize_string(key, max_length=100)

            if isinstance(value, dict):
                value = InputSanitizer.sanitize_dict(value, max_depth=max_depth - 1)
            elif isinstance(value, str):
                value = InputSanitizer.sanitize_string(value)
            elif isinstance(value, (list, tuple)):
                value = [
                    InputSanitizer.sanitize_string(v) if isinstance(v, str) else v for v in value
                ]

            sanitized[key] = value

        return sanitized
