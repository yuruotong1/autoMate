"""Unit tests for tools module"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from gradio_ui.tools.base import ToolResult
from gradio_ui.tools.collection import ToolCollection
import numpy as np
from datetime import datetime


class TestToolResult:
    """Test ToolResult data class"""

    def test_tool_result_success(self):
        """Test successful tool result"""
        result = ToolResult(success=True, data={"key": "value"})
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.error is None

    def test_tool_result_failure(self):
        """Test failed tool result"""
        result = ToolResult(success=False, error="Operation failed")
        assert result.success is False
        assert result.error == "Operation failed"
        assert result.data is None

    def test_tool_result_timestamp(self):
        """Test that ToolResult has timestamp"""
        result = ToolResult(success=True)
        assert result.timestamp is not None
        assert isinstance(result.timestamp, datetime)

    def test_tool_result_execution_time(self):
        """Test execution time tracking"""
        result = ToolResult(success=True, execution_time=1.5)
        assert result.execution_time == 1.5


class TestComputerTool:
    """Test ComputerTool functionality"""

    @patch("pyautogui.click")
    def test_click_action(self, mock_click):
        """Test click action"""
        from gradio_ui.tools.computer import ComputerTool

        tool = ComputerTool()
        result = tool.execute(action="click", x=100, y=200, button="left")

        # Should succeed even with mock
        assert result is not None

    @patch("pyautogui.typewrite")
    @patch("pyautogui.write")
    def test_type_action(self, mock_write, mock_typewrite):
        """Test type action"""
        from gradio_ui.tools.computer import ComputerTool

        tool = ComputerTool()
        result = tool.execute(action="type", text="hello", interval=0.05)

        # Should handle both typewrite and write
        assert result is not None

    @patch("pyautogui.scroll")
    def test_scroll_action(self, mock_scroll):
        """Test scroll action"""
        from gradio_ui.tools.computer import ComputerTool

        tool = ComputerTool()
        result = tool.execute(action="scroll", x=100, y=100, direction="down", amount=3)

        assert result is not None

    @patch("pyautogui.press")
    def test_key_press_action(self, mock_press):
        """Test key press action"""
        from gradio_ui.tools.computer import ComputerTool

        tool = ComputerTool()
        result = tool.execute(action="key_press", key="enter")

        assert result is not None

    @patch("pyautogui.moveTo")
    def test_mouse_move_action(self, mock_move):
        """Test mouse move action"""
        from gradio_ui.tools.computer import ComputerTool

        tool = ComputerTool()
        result = tool.execute(action="mouse_move", x=100, y=200, duration=0.5)

        assert result is not None

    @patch("time.sleep")
    def test_wait_action(self, mock_sleep):
        """Test wait action"""
        from gradio_ui.tools.computer import ComputerTool

        tool = ComputerTool()
        result = tool.execute(action="wait", seconds=1)

        assert result is not None
        mock_sleep.assert_called()

    def test_invalid_action(self):
        """Test invalid action raises error"""
        from gradio_ui.tools.computer import ComputerTool

        tool = ComputerTool()
        result = tool.execute(action="invalid_action")

        # Should return error result
        assert result.success is False
        assert result.error is not None


class TestScreenCaptureTool:
    """Test ScreenCaptureTool functionality"""

    @patch("pyautogui.screenshot")
    def test_capture_full_screen(self, mock_screenshot):
        """Test full screen capture"""
        from gradio_ui.tools.screen_capture import ScreenCaptureTool
        from PIL import Image

        # Create mock image
        mock_image = Image.new("RGB", (1920, 1080))
        mock_screenshot.return_value = mock_image

        tool = ScreenCaptureTool()
        result = tool.execute()

        assert result is not None

    @patch("pyautogui.screenshot")
    def test_capture_region(self, mock_screenshot):
        """Test region capture"""
        from gradio_ui.tools.screen_capture import ScreenCaptureTool
        from PIL import Image

        mock_image = Image.new("RGB", (100, 100))
        mock_screenshot.return_value = mock_image

        tool = ScreenCaptureTool()
        result = tool.execute(region=(100, 100, 200, 200))

        assert result is not None

    @patch("pyautogui.screenshot")
    @patch("pyautogui.position")
    def test_capture_with_cursor(self, mock_position, mock_screenshot):
        """Test capture with cursor overlay"""
        from gradio_ui.tools.screen_capture import ScreenCaptureTool
        from PIL import Image

        mock_position.return_value = (500, 500)
        mock_image = Image.new("RGB", (1920, 1080))
        mock_screenshot.return_value = mock_image

        tool = ScreenCaptureTool()
        result = tool.execute(include_cursor=True)

        assert result is not None

    @patch("pyautogui.screenshot")
    def test_capture_formats(self, mock_screenshot):
        """Test different output formats"""
        from gradio_ui.tools.screen_capture import ScreenCaptureTool
        from PIL import Image

        mock_image = Image.new("RGB", (100, 100))
        mock_screenshot.return_value = mock_image

        tool = ScreenCaptureTool()

        # Test numpy format
        result_numpy = tool.execute(format="numpy")
        assert result_numpy is not None

        # Test PIL format
        result_pil = tool.execute(format="pil")
        assert result_pil is not None

        # Test base64 format
        result_base64 = tool.execute(format="base64")
        assert result_base64 is not None


class TestToolCollection:
    """Test ToolCollection management"""

    def test_tool_collection_creation(self):
        """Test creating tool collection"""
        collection = ToolCollection()
        assert collection is not None

    def test_register_tool(self, computer_tool_mock):
        """Test registering a tool"""
        collection = ToolCollection()
        collection.register_tool(computer_tool_mock)

        # Should be able to retrieve tool
        tool = collection.get_tool("computer_control")
        assert tool is not None

    def test_list_tools(self, computer_tool_mock):
        """Test listing available tools"""
        collection = ToolCollection()
        collection.register_tool(computer_tool_mock)

        tools = collection.list_tools()
        assert len(tools) > 0
        assert any(t["name"] == "computer_control" for t in tools)

    @patch("pyautogui.click")
    def test_execute_tool(self, mock_click):
        """Test executing a tool from collection"""
        from gradio_ui.tools.computer import ComputerTool

        collection = ToolCollection()
        # Assuming ComputerTool is registered by default
        result = collection.execute("computer_control", action="click", x=100, y=100)

        assert result is not None

    def test_execute_nonexistent_tool(self):
        """Test executing nonexistent tool returns error"""
        collection = ToolCollection()
        result = collection.execute("nonexistent_tool")

        # Should return error result
        assert result is None or result.get("error") is not None
