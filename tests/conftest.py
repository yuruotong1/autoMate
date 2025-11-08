"""Pytest configuration and fixtures"""

import pytest
import numpy as np
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import os


@pytest.fixture
def mock_api_key():
    """Mock API key fixture"""
    return "sk-test-mock-key"


@pytest.fixture
def mock_model_config():
    """Mock model configuration"""
    return {
        "provider": "openai",
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 4096,
    }


@pytest.fixture
def mock_anthropic_config():
    """Mock Anthropic configuration"""
    return {
        "provider": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7,
        "max_tokens": 4096,
    }


@pytest.fixture
def mock_screenshot():
    """Create a mock screenshot as numpy array"""
    # Create a simple RGB image (100x100x3)
    return np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)


@pytest.fixture
def mock_ui_element():
    """Create a mock UI element"""
    return {
        "id": "elem_0",
        "bbox": (10, 10, 50, 30),
        "x": 10,
        "y": 10,
        "width": 50,
        "height": 30,
        "text": "Login",
        "type": "button",
        "caption": "A login button",
        "confidence": 0.95,
    }


@pytest.fixture
def mock_tool_result():
    """Create a mock tool result"""
    return {
        "success": True,
        "data": {"message": "Operation successful"},
        "error": None,
        "timestamp": datetime.now().isoformat(),
    }


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client"""
    client = MagicMock()
    client.messages.create.return_value = MagicMock(
        content=[MagicMock(text='{"result": "success"}')]
    )
    return client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    client = MagicMock()
    client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"result": "success"}'))]
    )
    return client


@pytest.fixture
def mock_yolo_model():
    """Mock YOLO model"""
    model = MagicMock()
    detection = MagicMock()
    detection.boxes.xyxy = np.array([[10, 10, 60, 40]])
    detection.boxes.cls = np.array([0])
    detection.boxes.conf = np.array([0.95])
    model.predict.return_value = [detection]
    return model


@pytest.fixture
def mock_easyocr_reader():
    """Mock EasyOCR reader"""
    reader = MagicMock()
    reader.readtext.return_value = [
        ([(10, 10), (60, 10), (60, 40), (10, 40)], "Login", 0.98)
    ]
    return reader


@pytest.fixture
def mock_florence_model():
    """Mock Florence-2 model"""
    model = MagicMock()
    model.return_value = {"<CAPTION>": "A login button"}
    return model


@pytest.fixture
def capture_tool_mock():
    """Mock screen capture tool"""
    tool = MagicMock()
    tool.name = "screen_capture"
    tool.execute.return_value = {
        "success": True,
        "data": {
            "image": np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8),
            "size": (100, 100),
            "cursor_position": (50, 50),
        },
        "error": None,
    }
    return tool


@pytest.fixture
def computer_tool_mock():
    """Mock computer control tool"""
    tool = MagicMock()
    tool.name = "computer_control"
    tool.execute.return_value = {"success": True, "data": {}, "error": None}
    return tool


@pytest.fixture
def tool_collection_mock():
    """Mock tool collection"""
    collection = MagicMock()
    collection.execute.return_value = {"success": True, "data": {}, "error": None}
    return collection


# Pytest markers for test organization
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "requires_gpu: Tests requiring GPU")
    config.addinivalue_line("markers", "requires_api: Tests requiring API keys")


# Environment setup for tests
@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment"""
    # Set test API key if not present
    if "ANTHROPIC_API_KEY" not in os.environ:
        os.environ["ANTHROPIC_API_KEY"] = "sk-test-key"
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "sk-test-key"

    yield

    # Cleanup after test
    pass
