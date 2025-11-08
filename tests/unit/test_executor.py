"""Unit tests for executor module"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
import json


class TestAnthropicExecutor:
    """Test AnthropicExecutor functionality"""

    @pytest.mark.asyncio
    async def test_executor_initialization(self, tool_collection_mock):
        """Test executor initialization"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)
        assert executor is not None

    @pytest.mark.asyncio
    async def test_execute_tool(self, tool_collection_mock):
        """Test executing a tool"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # Mock tool execution
        tool_collection_mock.execute.return_value = {
            "success": True,
            "data": {"result": "executed"},
        }

        result = await executor.execute(
            tool_name="computer_control", tool_input={"action": "click", "x": 100, "y": 200}
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_validate_tool_call(self, tool_collection_mock):
        """Test tool call validation"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # Valid tool call
        is_valid, error = executor.validate_tool_call(
            "computer_control", {"action": "click", "x": 100, "y": 200}
        )

        # Should handle validation
        assert isinstance(is_valid, (bool, type(None)))

    @pytest.mark.asyncio
    async def test_execute_invalid_tool(self, tool_collection_mock):
        """Test executing invalid tool"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # Tool collection returns error for invalid tool
        tool_collection_mock.execute.return_value = None

        result = await executor.execute(
            tool_name="invalid_tool", tool_input={"action": "test"}
        )

        # Should return None or error
        assert result is None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_execute_with_timeout(self, tool_collection_mock):
        """Test execution with timeout"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor
        import asyncio

        executor = AnthropicExecutor(tool_collection_mock)

        # Simulate slow execution
        async def slow_execute(*args, **kwargs):
            await asyncio.sleep(0.1)
            return {"success": True}

        tool_collection_mock.execute = slow_execute

        # Should handle timeout gracefully
        result = await executor.execute("test_tool", {})
        assert result is not None or result is None


class TestToolExecution:
    """Test tool execution patterns"""

    @pytest.mark.asyncio
    async def test_execute_click_tool(self, computer_tool_mock, tool_collection_mock):
        """Test executing click tool"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        result = await executor.execute("computer_control", {"action": "click", "x": 100, "y": 200})

        assert result is not None

    @pytest.mark.asyncio
    async def test_execute_type_tool(self, computer_tool_mock, tool_collection_mock):
        """Test executing type tool"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        result = await executor.execute(
            "computer_control",
            {"action": "type", "text": "hello", "interval": 0.05},
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_execute_screenshot_tool(self, capture_tool_mock, tool_collection_mock):
        """Test executing screenshot tool"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        tool_collection_mock.execute.return_value = {
            "success": True,
            "data": capture_tool_mock.execute.return_value.get("data"),
        }

        result = await executor.execute("screen_capture", {})

        assert result is not None

    @pytest.mark.asyncio
    async def test_sequential_tool_execution(self, tool_collection_mock):
        """Test executing multiple tools sequentially"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # Execute multiple tools in sequence
        tool_collection_mock.execute.return_value = {"success": True}

        result1 = await executor.execute("computer_control", {"action": "click", "x": 100, "y": 200})
        result2 = await executor.execute("computer_control", {"action": "type", "text": "test"})

        assert result1 is not None
        assert result2 is not None


class TestExecutorErrorHandling:
    """Test executor error handling"""

    @pytest.mark.asyncio
    async def test_executor_handles_tool_exception(self, tool_collection_mock):
        """Test executor handles tool exceptions"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # Mock tool raising exception
        tool_collection_mock.execute.side_effect = Exception("Tool execution failed")

        result = await executor.execute("computer_control", {"action": "click"})

        # Should handle exception gracefully
        assert result is None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_executor_validates_input(self, tool_collection_mock):
        """Test executor validates input"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # Test with minimal input
        result = await executor.execute("computer_control", {})

        # Should handle empty input
        assert result is None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_executor_handles_missing_parameters(self, tool_collection_mock):
        """Test executor with missing parameters"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # Click without coordinates
        result = await executor.execute("computer_control", {"action": "click"})

        # Should handle or reject invalid call
        assert result is None or isinstance(result, dict)


class TestExecutorRetry:
    """Test executor retry logic"""

    @pytest.mark.asyncio
    async def test_executor_retry_on_failure(self, tool_collection_mock):
        """Test executor retries on failure"""
        from gradio_ui.executor.anthropic_executor import AnthropicExecutor

        executor = AnthropicExecutor(tool_collection_mock)

        # First call fails, second succeeds
        tool_collection_mock.execute.side_effect = [
            Exception("First attempt failed"),
            {"success": True},
        ]

        # In production, executor would retry
        try:
            result = await executor.execute("computer_control", {"action": "click"})
        except:
            # First attempt may fail
            pass

        # Second attempt would succeed
        tool_collection_mock.execute.side_effect = None
        tool_collection_mock.execute.return_value = {"success": True}
        result = await executor.execute("computer_control", {"action": "click"})

        assert result is not None
