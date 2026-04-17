"""
Integration tests for core.engine module - Script execution engine.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from core.engine import Engine, StepStatus, RunResult, Script
from core.script import MarkdownStep


class TestEngineBasic:
    """Basic Engine tests."""

    @pytest.fixture
    def engine(self):
        """Create Engine instance with AI fallback disabled."""
        return Engine(use_ai_fallback=False)

    def test_engine_initialization(self):
        """Engine initializes with correct defaults."""
        engine = Engine()
        assert engine.use_ai_fallback is True
        assert engine.on_teach is None
        assert engine.on_progress is None

    def test_engine_with_callbacks(self):
        """Engine accepts callback functions."""
        on_teach = Mock()
        on_progress = Mock()
        engine = Engine(on_teach=on_teach, on_progress=on_progress, use_ai_fallback=False)

        assert engine.on_teach is on_teach
        assert engine.on_progress is on_progress
        assert engine.use_ai_fallback is False


class TestEngineKeyAction:
    """Tests for key action execution."""

    @pytest.fixture
    def engine(self):
        return Engine(use_ai_fallback=False)

    @pytest.fixture
    def script_with_key(self):
        body = """## Steps
1. Press Enter [key:enter]
"""
        return Script(name="key_test", body=body)

    def test_exec_key_single(self, engine, script_with_key):
        """Single key press works correctly."""
        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script_with_key)
            assert result.success is True
            mock_pyautogui.press.assert_called_once_with("enter")

    def test_exec_key_combo(self):
        """Key combination works correctly."""
        body = """## Steps
1. Save [key:ctrl+s]
"""
        script = Script(name="combo_test", body=body)
        engine = Engine(use_ai_fallback=False)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.hotkey.assert_called_once_with("ctrl", "s")

    def test_key_combo_with_multiple_modifiers(self):
        """Multiple modifier keys work correctly."""
        body = """## Steps
1. Search [key:ctrl+shift+f]
"""
        script = Script(name="multi_modifier", body=body)
        engine = Engine(use_ai_fallback=False)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.hotkey.assert_called_once_with("ctrl", "shift", "f")


class TestEngineWaitAction:
    """Tests for wait action execution."""

    @pytest.fixture
    def engine(self):
        return Engine(use_ai_fallback=False)

    @pytest.fixture
    def script_with_wait(self):
        body = """## Steps
1. Wait [wait:0.5]
"""
        return Script(name="wait_test", body=body)

    def test_exec_wait(self, engine, script_with_wait):
        """Wait action executes correctly."""
        with patch("core.engine.time.sleep") as mock_sleep:
            result = engine.run(script_with_wait)
            assert result.success is True
            mock_sleep.assert_called_once_with(0.5)

    def test_exec_wait_default(self):
        """Wait with no value uses default 1 second."""
        body = """## Steps
1. Wait [wait:]
"""
        script = Script(name="wait_default", body=body)
        engine = Engine(use_ai_fallback=False)

        with patch("core.engine.time.sleep") as mock_sleep:
            result = engine.run(script)
            assert result.success is True
            mock_sleep.assert_called_once_with(1)


class TestEngineScrollAction:
    """Tests for scroll action execution."""

    @pytest.fixture
    def engine(self):
        return Engine(use_ai_fallback=False)

    def test_scroll_up(self, engine):
        """scroll_up works correctly."""
        body = """## Steps
1. Scroll up [scroll_up]
"""
        script = Script(name="scroll_up", body=body)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.scroll.assert_called_once_with(3)

    def test_scroll_down(self, engine):
        """scroll_down works correctly."""
        body = """## Steps
1. Scroll down [scroll_down]
"""
        script = Script(name="scroll_down", body=body)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.scroll.assert_called_once_with(-3)


class TestEngineClickAction:
    """Tests for click action execution."""

    @pytest.fixture
    def engine(self):
        return Engine(use_ai_fallback=False)

    def test_click_with_coord(self, engine):
        """Click with absolute coordinates works."""
        body = """## Steps
1. Click at position [click:coord=100,200]
"""
        script = Script(name="click_coord", body=body)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.click.assert_called_once_with(100, 200)

    def test_double_click_with_coord(self, engine):
        """Double-click with coordinates works."""
        body = """## Steps
1. Double-click [double_click:coord=150,250]
"""
        script = Script(name="double_click", body=body)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.doubleClick.assert_called_once_with(150, 250)

    def test_right_click_with_coord(self, engine):
        """Right-click with coordinates works."""
        body = """## Steps
1. Right-click [right_click:coord=300,400]
"""
        script = Script(name="right_click", body=body)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.rightClick.assert_called_once_with(300, 400)


class TestEngineTypeAction:
    """Tests for type action execution."""

    @pytest.fixture
    def engine(self):
        return Engine(use_ai_fallback=False)

    def test_type_text(self, engine):
        """Type text works correctly."""
        body = """## Steps
1. Type message [type:Hello]
"""
        script = Script(name="type_test", body=body)

        with patch("core.engine.pyautogui") as mock_pyautogui:
            result = engine.run(script)
            assert result.success is True
            mock_pyautogui.typewrite.assert_called_once()


class TestEngineTeachCallback:
    """Tests for human-in-the-loop teach callback."""

    def test_teach_callback_triggered_on_ocr_failure(self):
        """Teach callback is called when OCR cannot find element."""
        on_teach = Mock(return_value=(500, 600))
        engine = Engine(on_teach=on_teach, use_ai_fallback=False)

        # Step with click but no coord - needs OCR
        step = MarkdownStep(
            index=1,
            text="Click OK button",
            hints={"action": "click", "value": "OK"}
        )
        script = Script(name="teach_test", body="## Steps\n1. Click OK button")

        with patch("core.engine.resolve_ocr", return_value=None):
            with patch("core.engine.pyautogui") as mock_pyautogui:
                result = engine._run_step(step, script)

        assert result.status == StepStatus.OK
        on_teach.assert_called_once()
        mock_pyautogui.click.assert_called_once_with(500, 600)

    def test_teach_callback_returns_none(self):
        """When teach returns None, status is TEACH_ME."""
        on_teach = Mock(return_value=None)
        engine = Engine(on_teach=on_teach, use_ai_fallback=False)

        step = MarkdownStep(
            index=1,
            text="Click button",
            hints={"action": "click", "value": "NotFound"}
        )
        script = Script(name="teach_none", body="## Steps\n1. Click button")

        with patch("core.engine.resolve_ocr", return_value=None):
            result = engine._run_step(step, script)

        assert result.status == StepStatus.TEACH_ME


class TestEngineProgressCallback:
    """Tests for progress callback."""

    def test_progress_callback_called(self):
        """Progress callback is called after each step."""
        on_progress = Mock()
        engine = Engine(on_progress=on_progress, use_ai_fallback=False)

        body = """## Steps
1. Step one [key:a]
2. Step two [key:b]
"""
        script = Script(name="progress_test", body=body)

        with patch("core.engine.pyautogui"):
            result = engine.run(script)

        assert on_progress.call_count == 2


class TestEngineRunResult:
    """Tests for RunResult dataclass."""

    def test_run_result_success(self):
        """Successful run sets success=True."""
        body = """## Steps
1. Press Enter [key:enter]
"""
        script = Script(name="success_test", body=body)
        engine = Engine(use_ai_fallback=False)

        with patch("core.engine.pyautogui"):
            result = engine.run(script)

        assert result.success is True
        assert result.script_name == "success_test"
        assert result.error is None

    def test_run_result_unknown_action(self):
        """Unknown action returns SKIPPED but doesn't fail the run."""
        body = """## Steps
1. Invalid action [invalid:foo]
"""
        script = Script(name="fail_test", body=body)
        engine = Engine(use_ai_fallback=False)

        with patch("core.engine.pyautogui"):
            result = engine.run(script)

        # Unknown action returns SKIPPED, which doesn't set success=False
        # The run completes (all steps executed), just some were skipped
        assert len(result.step_results) == 1
        assert result.step_results[0].status == StepStatus.SKIPPED
        assert "unknown action" in result.step_results[0].message

    def test_run_result_step_results(self):
        """RunResult contains step results."""
        body = """## Steps
1. Key a [key:a]
2. Key b [key:b]
"""
        script = Script(name="steps_test", body=body)
        engine = Engine(use_ai_fallback=False)

        with patch("core.engine.pyautogui"):
            result = engine.run(script)

        assert len(result.step_results) == 2
        assert all(sr.status == StepStatus.OK for sr in result.step_results)


class TestEngineNoHintSteps:
    """Tests for steps without hints."""

    def test_skip_without_ai_fallback(self):
        """Steps without hints are skipped when AI fallback disabled."""
        body = """## Steps
1. Just do something
"""
        script = Script(name="no_hint", body=body)
        engine = Engine(use_ai_fallback=False)

        with patch("core.engine.pyautogui"):
            result = engine.run(script)

        # SKIPPED doesn't fail the run, but step returns SKIPPED status
        assert result.success is True  # run completed, just step was skipped
        assert len(result.step_results) == 1
        assert result.step_results[0].status == StepStatus.SKIPPED
        assert "AI fallback disabled" in result.step_results[0].message

    def test_skip_with_ai_fallback_enabled(self):
        """Steps without hints attempt AI interpretation when enabled."""
        body = """## Steps
1. Just do something
"""
        script = Script(name="ai_fallback", body=body)
        engine = Engine(use_ai_fallback=True)

        with patch("core.engine.pyautogui"):
            result = engine.run(script)

        # Will fail because we mock pyautogui, but it should attempt
        # The key is it doesn't skip immediately
        assert result.error is not None or result.success is False