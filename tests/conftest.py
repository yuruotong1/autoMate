"""
pytest configuration and shared fixtures for autoMate tests.
"""

import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def temp_scripts_dir(tmp_path):
    """Temporary scripts directory for testing."""
    scripts = tmp_path / ".automate" / "scripts"
    scripts.mkdir(parents=True)
    return scripts


@pytest.fixture
def mock_home(monkeypatch, tmp_path):
    """Mock Path.home() to use temporary directory."""
    def mock_home_func():
        return tmp_path
    monkeypatch.setattr(Path, "home", mock_home_func)


@pytest.fixture
def sample_script_markdown():
    """Sample valid script markdown for testing."""
    return """---
name: test_script
description: Test automation script
created_at: 2024-01-01T10:00:00
stability: draft
total_runs: 0
success_runs: 0
---

# Test Script

This is a test automation script.

## Steps

1. Open application [key:ctrl+r]
2. Click the OK button [click:OK]
3. Type message [type:Hello World]
4. Wait 2 seconds [wait:2]
5. Scroll down [scroll_down]
"""