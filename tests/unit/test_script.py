"""
Unit tests for core.script module - Script model and parsing.
"""

import pytest
from core.script import Script, _parse_hint, MarkdownStep


class TestParseHint:
    """Tests for inline hint parsing."""

    def test_click_with_text(self):
        """[click:OK] -> action=click, value=OK"""
        result = _parse_hint("click", "OK")
        assert result == {"action": "click", "value": "OK"}

    def test_click_with_coord(self):
        """[click:coord=320,240] -> action=click, coord=[320, 240]"""
        result = _parse_hint("click", "coord=320,240")
        assert result == {"action": "click", "coord": [320, 240]}

    def test_click_with_coord_spaces(self):
        """[click:coord=320, 240] -> action=click, coord=[320, 240]"""
        result = _parse_hint("click", "coord=320, 240")
        assert result == {"action": "click", "coord": [320, 240]}

    def test_type_with_text(self):
        """[type:Hello World] -> action=type, value=Hello World"""
        result = _parse_hint("type", "Hello World")
        assert result == {"action": "type", "value": "Hello World"}

    def test_key_single(self):
        """[key:enter] -> action=key, value=enter"""
        result = _parse_hint("key", "enter")
        assert result == {"action": "key", "value": "enter"}

    def test_key_combo(self):
        """[key:ctrl+s] -> action=key, value=ctrl+s"""
        result = _parse_hint("key", "ctrl+s")
        assert result == {"action": "key", "value": "ctrl+s"}

    def test_wait_with_seconds(self):
        """[wait:2] -> action=wait, value=2"""
        result = _parse_hint("wait", "2")
        assert result == {"action": "wait", "value": "2"}

    def test_scroll_up_no_arg(self):
        """[scroll_up] -> action=scroll_up"""
        result = _parse_hint("scroll_up", None)
        assert result == {"action": "scroll_up"}

    def test_scroll_down_no_arg(self):
        """[scroll_down] -> action=scroll_down"""
        result = _parse_hint("scroll_down", None)
        assert result == {"action": "scroll_down"}

    def test_double_click(self):
        """[double_click] -> action=double_click"""
        result = _parse_hint("double_click", None)
        assert result == {"action": "double_click"}

    def test_right_click(self):
        """[right_click] -> action=right_click"""
        result = _parse_hint("right_click", None)
        assert result == {"action": "right_click"}

    def test_empty_arg_returns_action_only(self):
        """[key:] -> action=key, no value"""
        result = _parse_hint("key", "")
        assert result == {"action": "key"}


class TestScriptFromMarkdown:
    """Tests for Script.from_markdown()."""

    def test_parse_full_frontmatter(self):
        """Parse complete frontmatter correctly."""
        text = """---
name: my_script
description: A test script
created_at: 2024-01-15 08:30:00
stability: stable
total_runs: 10
success_runs: 8
---

# My Script

Some description.

## Steps

1. Step one [key:enter]
"""
        script = Script.from_markdown(text)

        assert script.name == "my_script"
        assert script.description == "A test script"
        assert script.created_at == "2024-01-15 08:30:00"
        assert script.stability == "stable"
        assert script.total_runs == 10
        assert script.success_runs == 8

    def test_parse_minimal_frontmatter(self):
        """Parse minimal frontmatter with defaults."""
        text = """---
name: minimal
---

# Minimal

## Steps

1. Do something [key:space]
"""
        script = Script.from_markdown(text)

        assert script.name == "minimal"
        assert script.description == ""
        assert script.stability == "draft"
        assert script.total_runs == 0
        assert script.success_runs == 0

    def test_parse_no_frontmatter(self):
        """Parse markdown without frontmatter."""
        text = """# No Frontmatter

## Steps

1. Just do it [key:enter]
"""
        script = Script.from_markdown(text)

        assert script.name == "unnamed"
        assert script.body.strip() == text.strip()

    def test_parse_body_preserves_content(self):
        """Body content is preserved after parsing."""
        text = """---
name: test
---

# Title

This is the body content.

## Steps

1. Step one [key:a]
2. Step two [key:b]
"""
        script = Script.from_markdown(text)

        assert "Title" in script.body
        assert "This is the body content" in script.body


class TestScriptToMarkdown:
    """Tests for Script.to_markdown()."""

    def test_roundtrip_full(self):
        """Parse then serialize should produce equivalent output."""
        original = """---
name: roundtrip_test
description: Testing roundtrip
stability: stable
total_runs: 5
success_runs: 3
---

# Roundtrip Test

## Steps

1. Press key [key:ctrl+s]
"""
        script = Script.from_markdown(original)
        regenerated = script.to_markdown()
        script2 = Script.from_markdown(regenerated)

        assert script2.name == script.name
        assert script2.description == script.description
        assert script2.stability == script.stability

    def test_to_markdown_format(self):
        """to_markdown produces valid YAML frontmatter."""
        script = Script(
            name="format_test",
            description="Test format",
            body="# Test\n\n## Steps\n\n1. Done [key:enter]",
            stability="draft",
            total_runs=1,
            success_runs=1,
        )

        result = script.to_markdown()

        assert result.startswith("---")
        assert "name: format_test" in result
        assert "description: Test format" in result
        assert "stability: draft" in result


class TestScriptSteps:
    """Tests for Script.steps() extraction."""

    def test_extract_numbered_steps(self):
        """Extract numbered list steps."""
        text = """---
name: steps_test
---

## Steps

1. First step [key:a]
2. Second step [key:b]
3. Third step [key:c]
"""
        script = Script.from_markdown(text)
        steps = script.steps()

        assert len(steps) == 3
        assert steps[0].action == "key"
        assert steps[0].value == "a"
        assert steps[1].action == "key"
        assert steps[2].action == "key"

    def test_extract_bullet_steps(self):
        """Extract bullet list steps."""
        text = """---
name: bullet_test
---

## Steps

- First [key:1]
- Second [key:2]
"""
        script = Script.from_markdown(text)
        steps = script.steps()

        assert len(steps) == 2

    def test_steps_preserve_text(self):
        """Step text should be cleaned of hint markup."""
        text = """---
name: text_test
---

## Steps

1. Click the button [click:Submit]
"""
        script = Script.from_markdown(text)
        steps = script.steps()

        assert "Click the button" in steps[0].text
        assert "[click:Submit]" not in steps[0].text

    def test_no_steps_section(self):
        """Script without Steps section returns empty list."""
        text = """---
name: no_steps
---

# No Steps Here

Just some text.
"""
        script = Script.from_markdown(text)
        steps = script.steps()

        assert len(steps) == 0


class TestMarkdownStep:
    """Tests for MarkdownStep class."""

    def test_is_code_property(self):
        """is_code returns True when code is present."""
        step = MarkdownStep(index=1, text="code", code="print('hello')")
        assert step.is_code is True

    def test_is_code_property_false(self):
        """is_code returns False when no code."""
        step = MarkdownStep(index=1, text="regular step", hints={"action": "key"})
        assert step.is_code is False

    def test_action_property(self):
        """action returns the action from hints."""
        step = MarkdownStep(index=1, text="step", hints={"action": "click", "value": "OK"})
        assert step.action == "click"

    def test_value_property(self):
        """value returns the value from hints."""
        step = MarkdownStep(index=1, text="step", hints={"action": "type", "value": "hello"})
        assert step.value == "hello"

    def test_repr(self):
        """__repr__ produces expected format."""
        step = MarkdownStep(index=1, text="Click OK", hints={"action": "click", "value": "OK"})
        repr_str = repr(step)
        assert "MarkdownStep" in repr_str
        assert "1" in repr_str