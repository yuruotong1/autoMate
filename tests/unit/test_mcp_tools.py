"""
Unit tests for MCP server tools.
"""

import platform
import pytest
from unittest.mock import patch, MagicMock


class TestClickTool:
    """Tests for click tool."""

    @pytest.fixture
    def setup_mocks(self):
        with patch("mcp_server.pyautogui") as mock:
            yield mock

    def test_click_default_left(self, setup_mocks):
        """Click with default button is left click."""
        from mcp_server import click
        result = click(x=100, y=200)
        setup_mocks.click.assert_called_once_with(100, 200, button="left")
        assert result == "Clicked (100, 200) [left]"

    def test_click_right_button(self, setup_mocks):
        """Click with right button."""
        from mcp_server import click
        result = click(x=50, y=150, button="right")
        setup_mocks.click.assert_called_once_with(50, 150, button="right")
        assert result == "Clicked (50, 150) [right]"

    def test_click_middle_button(self, setup_mocks):
        """Click with middle button."""
        from mcp_server import click
        result = click(x=300, y=400, button="middle")
        setup_mocks.click.assert_called_once_with(300, 400, button="middle")


class TestDoubleClickTool:
    """Tests for double_click tool."""

    @pytest.fixture
    def setup_mocks(self):
        with patch("mcp_server.pyautogui") as mock:
            yield mock

    def test_double_click(self, setup_mocks):
        """Double-click works correctly."""
        from mcp_server import double_click
        result = double_click(x=100, y=200)
        setup_mocks.doubleClick.assert_called_once_with(100, 200)
        assert result == "Double-clicked (100, 200)"


class TestMouseMoveTool:
    """Tests for mouse_move tool."""

    @pytest.fixture
    def setup_mocks(self):
        with patch("mcp_server.pyautogui") as mock:
            yield mock

    def test_mouse_move(self, setup_mocks):
        """Mouse move works correctly."""
        from mcp_server import mouse_move
        result = mouse_move(x=500, y=600)
        setup_mocks.moveTo.assert_called_once_with(500, 600)
        assert result == "Cursor moved to (500, 600)"


class TestDragTool:
    """Tests for drag tool."""

    @pytest.fixture
    def setup_mocks(self):
        with patch("mcp_server.pyautogui") as mock:
            yield mock

    def test_drag_default_duration(self, setup_mocks):
        """Drag with default duration."""
        from mcp_server import drag
        result = drag(start_x=100, start_y=100, end_x=200, end_y=200)
        setup_mocks.moveTo.assert_called_once_with(100, 100)
        setup_mocks.drag.assert_called_once_with(100, 100, duration=0.5)
        assert result == "Dragged (100,100) → (200,200)"

    def test_drag_custom_duration(self, setup_mocks):
        """Drag with custom duration."""
        from mcp_server import drag
        result = drag(start_x=0, start_y=0, end_x=100, end_y=100, duration=1.0)
        setup_mocks.drag.assert_called_once_with(100, 100, duration=1.0)


class TestScrollTool:
    """Tests for scroll tool."""

    @pytest.fixture
    def setup_mocks(self):
        with patch("mcp_server.pyautogui") as mock:
            yield mock

    def test_scroll_down_default(self, setup_mocks):
        """Scroll down with default amount."""
        from mcp_server import scroll
        result = scroll(direction="down")
        setup_mocks.scroll.assert_called_once_with(-3)
        assert result == "Scrolled down ×3"

    def test_scroll_up_default(self, setup_mocks):
        """Scroll up with default amount."""
        from mcp_server import scroll
        result = scroll(direction="up")
        setup_mocks.scroll.assert_called_once_with(3)
        assert result == "Scrolled up ×3"

    def test_scroll_custom_amount(self, setup_mocks):
        """Scroll with custom amount."""
        from mcp_server import scroll
        result = scroll(direction="down", amount=5)
        setup_mocks.scroll.assert_called_once_with(-5)
        assert result == "Scrolled down ×5"


class TestPressKeyTool:
    """Tests for press_key tool."""

    @pytest.fixture
    def setup_mocks(self):
        with patch("mcp_server.pyautogui") as mock:
            yield mock

    def test_press_single_key(self, setup_mocks):
        """Press single key."""
        from mcp_server import press_key
        result = press_key(keys="enter")
        setup_mocks.press.assert_called_once_with("enter")
        assert result == "Pressed [enter]"

    def test_press_key_combo(self, setup_mocks):
        """Press key combination."""
        from mcp_server import press_key
        result = press_key(keys="ctrl+c")
        setup_mocks.hotkey.assert_called_once_with("ctrl", "c")
        assert result == "Pressed [ctrl+c]"

    def test_press_triple_combo(self, setup_mocks):
        """Press triple key combination."""
        from mcp_server import press_key
        result = press_key(keys="ctrl+shift+s")
        setup_mocks.hotkey.assert_called_once_with("ctrl", "shift", "s")
        assert result == "Pressed [ctrl+shift+s]"


class TestTypeTextTool:
    """Tests for type_text tool."""

    @pytest.fixture
    def setup_mocks(self):
        with patch("mcp_server.pyperclip") as mock_clipboard:
            with patch("mcp_server.pyautogui") as mock_pyautogui:
                mock_clipboard.paste.return_value = "old_content"
                yield {"clipboard": mock_clipboard, "pyautogui": mock_pyautogui}

    def test_type_text_basic(self, setup_mocks):
        """Type basic text."""
        from mcp_server import type_text
        result = type_text(text="Hello")

        # First call: paste() to save old content
        # Second call: copy() with new text
        # Third call: copy() to restore old content
        calls = setup_mocks["clipboard"].copy.call_args_list
        assert len(calls) >= 2
        assert calls[0][0][0] == "Hello"  # First copy is the new text

        # Check hotkey - command on Mac, ctrl on others
        expected_modifier = "command" if platform.system() == "Darwin" else "ctrl"
        setup_mocks["pyautogui"].hotkey.assert_called_with(expected_modifier, "v")

        assert "Typed 5 characters" in result

    def test_type_text_unicode(self, setup_mocks):
        """Type Unicode text (including Chinese)."""
        from mcp_server import type_text
        result = type_text(text="你好世界")

        calls = setup_mocks["clipboard"].copy.call_args_list
        assert calls[0][0][0] == "你好世界"
        assert "Typed 4 characters" in result

    def test_type_text_preserves_clipboard(self, setup_mocks):
        """Type text preserves original clipboard content."""
        from mcp_server import type_text
        type_text(text="new text")
        # Last call should restore original clipboard
        setup_mocks["clipboard"].copy.assert_called_with("old_content")


class TestScreenInfoTools:
    """Tests for screen information tools."""

    def test_get_screen_size(self):
        """Get screen size returns correct format."""
        from mcp_server import get_screen_size
        with patch("mcp_server.pyautogui") as mock:
            mock.size.return_value = (1920, 1080)
            result = get_screen_size()
            assert result == "1920x1080"

    def test_get_cursor_position(self):
        """Get cursor position returns correct format."""
        from mcp_server import get_cursor_position
        with patch("mcp_server.pyautogui") as mock:
            mock.position.return_value = (100, 200)
            result = get_cursor_position()
            assert result == "(100, 200)"


class TestScreenshotTool:
    """Tests for screenshot tool."""

    def test_screenshot_full_screen(self):
        """Screenshot captures full screen."""
        from mcp_server import screenshot

        # Create a mock for the screenshot return value
        mock_img = MagicMock()
        mock_img.save = MagicMock()

        with patch("mcp_server.pyautogui") as mock:
            mock.screenshot.return_value = mock_img

            result = screenshot()

            mock.screenshot.assert_called_once()
            mock_img.save.assert_called_once()
            assert result.startswith("data:image/png;base64,")

    def test_screenshot_with_region(self):
        """Screenshot captures specific region."""
        from mcp_server import screenshot

        mock_img = MagicMock()
        mock_img.save = MagicMock()

        with patch("mcp_server.pyautogui") as mock:
            mock.screenshot.return_value = mock_img

            result = screenshot(region=[0, 0, 800, 600])

            mock.screenshot.assert_called_once_with(region=(0, 0, 800, 600))
            assert result.startswith("data:image/png;base64,")


class TestScriptManagementTools:
    """Tests for script management tools."""

    def test_list_scripts_empty(self, tmp_path):
        """List scripts returns message when empty."""
        from mcp_server import list_scripts

        with patch("mcp_server.SCRIPTS_DIR", tmp_path / "scripts"):
            result = list_scripts()
            assert "No saved scripts" in result

    def test_list_scripts_with_files(self, tmp_path):
        """List scripts shows all saved scripts."""
        from mcp_server import list_scripts

        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "script1.md").write_text("---\nname: script1\ndescription: First\n---")
        (scripts_dir / "script2.md").write_text("---\nname: script2\ndescription: Second\n---")

        with patch("mcp_server.SCRIPTS_DIR", scripts_dir):
            result = list_scripts()

        assert "2 script(s)" in result
        assert "script1" in result
        assert "script2" in result

    def test_run_script_not_found(self, tmp_path):
        """Run script returns error for missing script."""
        from mcp_server import run_script

        with patch("mcp_server.SCRIPTS_DIR", tmp_path / "scripts"):
            result = run_script(name="nonexistent")

        assert "not found" in result

    def test_save_script(self, tmp_path):
        """Save script writes file correctly."""
        from mcp_server import save_script

        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()

        with patch("mcp_server.SCRIPTS_DIR", scripts_dir):
            result = save_script(
                name="test_script",
                description="Test description",
                steps="1. Do something [key:enter]"
            )

        assert "Saved script" in result
        assert (scripts_dir / "test_script.md").exists()

    def test_show_script(self, tmp_path):
        """Show script returns content."""
        from mcp_server import show_script

        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        content = "---\nname: test\n---\n\n## Steps\n\n1. Step one"
        (scripts_dir / "test.md").write_text(content)

        with patch("mcp_server.SCRIPTS_DIR", scripts_dir):
            result = show_script(name="test")

        assert "Step one" in result

    def test_delete_script(self, tmp_path):
        """Delete script removes file."""
        from mcp_server import delete_script

        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "test.md").write_text("content")

        with patch("mcp_server.SCRIPTS_DIR", scripts_dir):
            result = delete_script(name="test")

        assert "Deleted" in result
        assert not (scripts_dir / "test.md").exists()

    def test_install_script_invalid_url(self):
        """Install script handles fetch error."""
        from mcp_server import install_script
        import urllib.error

        with patch("urllib.request.urlopen") as mock:
            mock.side_effect = urllib.error.URLError("Connection failed")
            result = install_script(url="http://invalid.url/script.md")

        assert "Failed to fetch" in result