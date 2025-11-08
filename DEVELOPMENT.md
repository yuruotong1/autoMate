# Development Guide

## Table of Contents
1. [Setting Up Development Environment](#setting-up-development-environment)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Adding Features](#adding-features)
5. [Creating Custom Tools](#creating-custom-tools)
6. [Creating Custom Agents](#creating-custom-agents)
7. [Testing](#testing)
8. [Code Style & Standards](#code-style--standards)
9. [Contributing](#contributing)

---

## Setting Up Development Environment

### Prerequisites

- Python 3.12+
- Git
- A code editor (VS Code, PyCharm, etc.)
- Basic understanding of AI/ML concepts

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode

# Install dev tools
pip install pytest pytest-asyncio black flake8 mypy
```

### Project Structure

```
autoMate/
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies
├── README.md                         # Main documentation
├── LICENSE                           # MIT License
│
├── gradio_ui/                        # Main application package
│   ├── __init__.py
│   ├── app.py                        # Web interface (Gradio)
│   ├── loop.py                       # Main processing loop
│   │
│   ├── agent/                        # AI Agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Base agent class
│   │   ├── vision_agent.py          # Screen analysis
│   │   ├── task_plan_agent.py       # Task decomposition
│   │   └── task_run_agent.py        # Task execution
│   │
│   ├── executor/                     # Tool execution engine
│   │   ├── __init__.py
│   │   └── anthropic_executor.py    # Claude tool executor
│   │
│   └── tools/                        # Available tools
│       ├── __init__.py
│       ├── base.py                   # BaseTool interface
│       ├── computer.py               # Computer control
│       ├── screen_capture.py         # Screenshot capture
│       ├── collection.py             # Tool manager
│       └── __init__.py
│
├── util/                             # Utility functions
│   ├── __init__.py
│   ├── download_weights.py          # Model downloading
│   ├── auto_control.py              # Input monitoring
│   ├── screen_selector.py           # Screen region selection
│   └── tool.py                      # Helper utilities
│
├── resources/                        # Static resources
│   ├── logo.png
│   └── wxchat.png
│
├── imgs/                             # UI images
│   └── header_bar_thin.png
│
└── weights/                          # Downloaded model cache
    └── AI-ModelScope/
        ├── OmniParser-v2.0
        └── Florence-2-base-ft
```

---

## Development Workflow

### 1. Creating a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/my-feature-name
```

Branch naming conventions:
- Features: `feature/description`
- Bugfixes: `bugfix/issue-description`
- Documentation: `docs/description`
- Refactoring: `refactor/description`

### 2. Making Changes

```bash
# Make your changes to the code

# Run tests to ensure nothing is broken
pytest

# Check code style
flake8 gradio_ui/
black gradio_ui/

# Type checking
mypy gradio_ui/
```

### 3. Committing Changes

```bash
# Stage changes
git add .

# Create descriptive commit
git commit -m "feat: add X feature" -m "Detailed description of changes"

# Commit message format:
# feat: new feature
# fix: bug fix
# docs: documentation
# style: formatting
# refactor: code reorganization
# test: test additions/updates
# perf: performance improvements
```

### 4. Pushing and Creating Pull Request

```bash
# Push to origin
git push origin feature/my-feature-name

# Create PR on GitHub with detailed description
```

---

## Adding Features

### Adding a New Tool

Example: Create a file browser tool

#### Step 1: Create Tool Class

**File:** `gradio_ui/tools/file_browser.py`

```python
from gradio_ui.tools.base import BaseTool, ToolResult
from typing import List, Optional
import os
from datetime import datetime

class FileBrowserTool(BaseTool):
    """Browse and interact with file system"""

    name = "file_browser"
    description = "Browse files and directories"

    def execute(
        self,
        action: str,
        **kwargs
    ) -> ToolResult:
        """
        Execute file browser action.

        Args:
            action: "list" | "exists" | "open" | "create"
            **kwargs: Action-specific parameters

        Returns:
            ToolResult with operation status
        """
        try:
            if action == "list":
                return self._list_directory(kwargs.get("path", "."))
            elif action == "exists":
                return self._check_exists(kwargs.get("path"))
            else:
                return ToolResult(
                    success=False,
                    error=f"Unknown action: {action}"
                )
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _list_directory(self, path: str) -> ToolResult:
        """List files in directory"""
        try:
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                is_dir = os.path.isdir(item_path)
                items.append({
                    "name": item,
                    "path": item_path,
                    "is_dir": is_dir,
                    "size": os.path.getsize(item_path) if not is_dir else 0
                })
            return ToolResult(success=True, data={"items": items})
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _check_exists(self, path: str) -> ToolResult:
        """Check if file/directory exists"""
        exists = os.path.exists(path)
        return ToolResult(
            success=True,
            data={"exists": exists, "is_dir": os.path.isdir(path)}
        )
```

#### Step 2: Register Tool

**File:** `gradio_ui/tools/collection.py`

```python
from gradio_ui.tools.file_browser import FileBrowserTool

class ToolCollection:
    def __init__(self):
        self.tools = {}
        self.register_tool(FileBrowserTool())
        # ... other tools
```

#### Step 3: Update Agent Prompts

Modify agents to use the new tool by including it in the prompt:

```python
# In task_run_agent.py
tool_descriptions = """
Available Tools:
- computer_control: Control mouse and keyboard
- screen_capture: Capture screenshots
- file_browser: Browse and manage files
"""
```

### Adding a New Agent

Example: Create a database agent

#### Step 1: Create Agent Class

**File:** `gradio_ui/agent/database_agent.py`

```python
from gradio_ui.agent.base_agent import BaseAgent
from typing import Dict, Any, Optional, List
import json

class DatabaseAgent(BaseAgent):
    """Agent for database operations"""

    async def analyze(
        self,
        query: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze database query.

        Args:
            query: SQL query or natural language database request
            context: Additional context about the database

        Returns:
            Analysis results with query recommendations
        """
        prompt = self._format_prompt(query=query, context=context)

        response = await self._call_llm(
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt}
            ],
            schema=self._response_schema()
        )

        return self._parse_response(response)

    def _system_prompt(self) -> str:
        return """You are a database expert. Analyze SQL queries and database operations.
        Provide recommendations for optimization and best practices."""

    def _format_prompt(self, **kwargs) -> str:
        query = kwargs.get("query", "")
        context = kwargs.get("context", "")
        return f"Analyze this query: {query}\nContext: {context}"

    def _response_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "is_valid": {"type": "boolean"},
                "analysis": {"type": "string"},
                "recommendations": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"success": False, "error": "Invalid response format"}
```

#### Step 2: Integrate into Main Loop

**File:** `gradio_ui/loop.py`

```python
from gradio_ui.agent.database_agent import DatabaseAgent

class MainLoop:
    def __init__(self, config: Dict, api_key: str):
        self.db_agent = DatabaseAgent(config, api_key)
        # ... other agents

    async def run_loop(self, user_input: str):
        # Use database agent for database-related tasks
        if "database" in user_input.lower():
            db_result = await self.db_agent.analyze(query=user_input)
            # Process result
```

---

## Creating Custom Tools

### Basic Tool Template

```python
from gradio_ui.tools.base import BaseTool, ToolResult
from typing import Dict, Any, Optional

class MyCustomTool(BaseTool):
    """Description of what your tool does"""

    name = "my_custom_tool"
    description = "What this tool does"

    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            ToolResult with success status and data
        """
        try:
            # Your implementation here
            result = self._do_something(**kwargs)

            return ToolResult(
                success=True,
                data=result
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )

    def _do_something(self, **kwargs) -> Dict[str, Any]:
        """Implementation of core logic"""
        # Your code here
        pass
```

### Example: Weather Tool

```python
import requests
from gradio_ui.tools.base import BaseTool, ToolResult

class WeatherTool(BaseTool):
    """Get current weather information"""

    name = "weather"
    description = "Get weather information for a location"

    def execute(self, location: str, **kwargs) -> ToolResult:
        try:
            # Call weather API
            response = requests.get(
                f"https://api.weather.example.com/current",
                params={"location": location}
            )
            response.raise_for_status()

            data = response.json()
            return ToolResult(
                success=True,
                data={
                    "location": location,
                    "temperature": data["temp"],
                    "conditions": data["description"],
                    "humidity": data["humidity"]
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))
```

---

## Creating Custom Agents

### Agent Development Steps

1. **Inherit from BaseAgent**
2. **Implement `analyze()` method**
3. **Define system prompt**
4. **Create response schema**
5. **Parse and return results**

### Example: Analysis Agent

```python
from gradio_ui.agent.base_agent import BaseAgent
from typing import Dict, Any, List
import json

class AnalysisAgent(BaseAgent):
    """Analyzes content and extracts insights"""

    async def analyze(
        self,
        content: str,
        analysis_type: str = "summary"
    ) -> Dict[str, Any]:
        """Analyze content"""
        messages = [
            {
                "role": "system",
                "content": self._system_prompt(analysis_type)
            },
            {
                "role": "user",
                "content": f"Analyze this content:\n\n{content}"
            }
        ]

        response = await self._call_llm(
            messages=messages,
            schema=self._response_schema()
        )

        return self._parse_response(response)

    def _system_prompt(self, analysis_type: str) -> str:
        prompts = {
            "summary": "Provide a concise summary of the content.",
            "sentiment": "Analyze sentiment and provide breakdown.",
            "keywords": "Extract key topics and themes.",
        }
        return prompts.get(analysis_type, prompts["summary"])

    def _response_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "result": {"type": "string"},
                "confidence": {"type": "number"},
                "details": {"type": "array", "items": {"type": "string"}}
            }
        }

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            data = json.loads(response)
            return {"success": True, **data}
        except json.JSONDecodeError:
            return {"success": False, "error": "Invalid response"}
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=gradio_ui

# Run async tests
pytest -v tests/test_async.py
```

### Writing Tests

**File:** `tests/test_my_tool.py`

```python
import pytest
from gradio_ui.tools.my_custom_tool import MyCustomTool

@pytest.fixture
def tool():
    return MyCustomTool()

def test_tool_execute(tool):
    """Test tool execution"""
    result = tool.execute(action="test")
    assert result.success == True
    assert result.data is not None

@pytest.mark.asyncio
async def test_async_agent():
    """Test async agent"""
    from gradio_ui.agent.my_agent import MyAgent

    agent = MyAgent(config, api_key)
    result = await agent.analyze(input_data="test")
    assert result["success"] == True
```

### Test Structure

```
tests/
├── __init__.py
├── test_agents.py          # Agent tests
├── test_tools.py           # Tool tests
├── test_integration.py     # Integration tests
└── fixtures/
    └── sample_screenshots/  # Test images
```

---

## Code Style & Standards

### Python Code Style

Follow PEP 8 with Black formatter:

```bash
# Format code
black gradio_ui/

# Check style
flake8 gradio_ui/ --max-line-length=100

# Type checking
mypy gradio_ui/ --ignore-missing-imports
```

### Naming Conventions

- **Classes:** PascalCase (e.g., `VisionAgent`)
- **Functions/Methods:** snake_case (e.g., `execute_action`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`)
- **Private:** Prefix with `_` (e.g., `_internal_method`)

### Documentation

All functions should have docstrings:

```python
def analyze(self, input: str) -> Dict[str, Any]:
    """
    Brief one-line description.

    Extended description explaining what the function does,
    how it works, and any important details.

    Args:
        input: Description of input parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When input is invalid
        RuntimeError: When operation fails
    """
    pass
```

### Type Hints

Use type hints for better code clarity:

```python
from typing import Dict, List, Optional, Tuple, Any

def process_data(
    data: List[Dict[str, Any]],
    filter: Optional[str] = None
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Process and filter data"""
    pass
```

---

## Contributing

### Contribution Process

1. **Fork the repository**
2. **Create feature branch** (`feature/my-feature`)
3. **Make changes** with tests
4. **Submit pull request** with clear description

### Pull Request Guidelines

1. **Title:** Clear and descriptive
2. **Description:** Explain what, why, and how
3. **Tests:** Include relevant tests
4. **Documentation:** Update docs if needed
5. **Code Review:** Be responsive to feedback

### Example PR Description

```markdown
## Description
Add support for dark mode in the web UI

## Related Issues
Closes #123

## Changes
- Added dark theme CSS
- Updated Gradio configuration
- Added theme toggle button
- Updated settings to persist theme preference

## Testing
- Tested in Chrome, Firefox, Safari
- Verified theme persists across sessions
- No performance impact

## Screenshots
[Add screenshots if applicable]
```

### Reporting Issues

1. **Search existing issues** first
2. **Provide details:**
   - Python version
   - OS and version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

3. **Example issue:**
```markdown
## Bug Report: API key not persisting

### Environment
- Python 3.12
- Ubuntu 22.04
- autoMate v0.1.0

### Steps to Reproduce
1. Open web UI
2. Enter API key in settings
3. Refresh page
4. API key is gone

### Expected Behavior
API key should persist across sessions

### Actual Behavior
API key is cleared on page refresh
```

---

## Development Tools & Resources

### Useful Tools

- **VS Code:** Popular editor with Python extensions
- **PyCharm:** Full-featured Python IDE
- **Jupyter:** For interactive development
- **Git Extensions:** GitHub Desktop, GitKraken

### Learning Resources

- [Anthropic API Docs](https://docs.anthropic.com)
- [Python Async Guide](https://docs.python.org/3/library/asyncio.html)
- [Computer Vision Guide](https://pytorch.org/vision/stable/index.html)
- [Design Patterns](https://refactoring.guru/design-patterns)

### Performance Profiling

```bash
# Profile code execution
pip install py-spy
py-spy record -o profile.svg -- python main.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler main.py
```

---

## Deployment

### Building for Distribution

```bash
# Create wheel distribution
python setup.py bdist_wheel

# Create source distribution
python setup.py sdist

# Install distribution
pip install dist/automate-0.1.0-py3-none-any.whl
```

### Continuous Integration

The project uses GitHub Actions for CI/CD:

- Runs tests on every push
- Checks code style
- Validates type hints
- Builds distributions

---

## Getting Help

- **GitHub Issues:** Report bugs and request features
- **Discussions:** Ask questions and share ideas
- **WeChat:** Contact via QR code in README
- **Documentation:** Check [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to create an inclusive and welcoming community.

---

For more information, see [ARCHITECTURE.md](./ARCHITECTURE.md) and [API.md](./API.md).
