# autoMate API Reference

## Table of Contents
1. [Agent APIs](#agent-apis)
2. [Tool APIs](#tool-apis)
3. [Executor API](#executor-api)
4. [Data Models](#data-models)
5. [LLM Integration](#llm-integration)
6. [Examples](#examples)

---

## Agent APIs

All agents inherit from `BaseAgent` and follow a consistent interface.

### BaseAgent

**Module:** `gradio_ui/agent/base_agent.py`

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(
        self,
        model_config: Dict[str, Any],
        api_key: str,
        base_url: Optional[str] = None
    ):
        """
        Initialize agent with configuration.

        Args:
            model_config: Model configuration dictionary
                - provider: str (openai, yeka, openai-next)
                - model: str (gpt-4o, o1, etc.)
                - temperature: float (0.0-1.0)
                - max_tokens: int
            api_key: API key for LLM provider
            base_url: Optional custom API endpoint
        """
        pass

    async def analyze(self, **kwargs) -> Dict[str, Any]:
        """
        Analyze input and return results.
        Must be implemented by subclasses.

        Returns:
            Dictionary with analysis results (schema varies by agent)
        """
        pass

    def _format_prompt(self, **kwargs) -> str:
        """Format input parameters into prompt text"""
        pass

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured output"""
        pass

    async def _call_llm(
        self,
        messages: List[Dict],
        schema: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call LLM with messages.

        Args:
            messages: List of message dictionaries
            schema: Optional JSON schema for structured output
            **kwargs: Additional parameters for LLM call

        Returns:
            LLM response as dictionary
        """
        pass
```

---

### Vision Agent

**Module:** `gradio_ui/agent/vision_agent.py`

Analyzes screenshots and detects UI elements using computer vision models.

```python
class VisionAgent(BaseAgent):
    """Analyzes screen content and detects UI elements"""

    async def analyze(
        self,
        screenshot_path: Optional[str] = None,
        screenshot_data: Optional[np.ndarray] = None,
        focus_region: Optional[Tuple[int, int, int, int]] = None
    ) -> Dict[str, Any]:
        """
        Analyze screenshot and return UI elements.

        Args:
            screenshot_path: Path to screenshot file
            screenshot_data: Numpy array of screenshot (RGB format)
            focus_region: Optional region to focus on (x, y, width, height)

        Returns:
            {
                "success": bool,
                "elements": List[UIElement],
                "cursor_position": Tuple[int, int],
                "image_width": int,
                "image_height": int,
                "processing_time": float
            }
        """
        pass
```

#### UIElement Data Model

```python
@dataclass
class UIElement:
    """Represents a detected UI element"""
    id: str                          # Unique identifier (e.g., "elem_0")
    bbox: Tuple[int, int, int, int]  # (x, y, width, height)
    x: int                            # Top-left x coordinate
    y: int                            # Top-left y coordinate
    width: int                        # Element width
    height: int                       # Element height
    text: str                         # Extracted text content
    type: str                         # Element type (button, input, etc.)
    caption: str                      # Description from vision model
    confidence: float                 # Detection confidence (0-1)

    @property
    def center(self) -> Tuple[int, int]:
        """Get center coordinates"""
        return (self.x + self.width // 2, self.y + self.height // 2)
```

#### Vision Agent Methods

```python
class VisionAgent(BaseAgent):

    def _detect_ui_elements(self, image: np.ndarray) -> List[Detection]:
        """
        Run YOLO detection on image.

        Args:
            image: RGB image as numpy array

        Returns:
            List of YOLO detections with bounding boxes
        """
        pass

    def _extract_text(
        self,
        image: np.ndarray,
        regions: List[Tuple]
    ) -> List[str]:
        """
        Extract text using EasyOCR.

        Args:
            image: Image as numpy array
            regions: List of (x, y, w, h) regions

        Returns:
            List of extracted text strings
        """
        pass

    def _generate_captions(
        self,
        image: np.ndarray,
        regions: List[Tuple]
    ) -> List[str]:
        """
        Generate captions using Florence-2.

        Args:
            image: Image as numpy array
            regions: List of (x, y, w, h) regions

        Returns:
            List of caption strings
        """
        pass
```

---

### Task Plan Agent

**Module:** `gradio_ui/agent/task_plan_agent.py`

Decomposes user requests into actionable subtasks.

```python
class TaskPlanAgent(BaseAgent):
    """Decomposes tasks into subtasks"""

    async def analyze(
        self,
        task_description: str,
        ui_elements: List[UIElement],
        screenshot_data: Optional[np.ndarray] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze task and create plan.

        Args:
            task_description: Natural language task description
            ui_elements: List of detected UI elements
            screenshot_data: Optional screenshot for visual context
            context: Optional additional context about the task

        Returns:
            {
                "success": bool,
                "main_task": str,
                "subtasks": List[str],
                "reasoning": str,
                "difficulty": str  # "easy", "medium", "hard"
            }
        """
        pass
```

#### Response Structure

```python
@dataclass
class TaskPlan:
    """Task decomposition plan"""
    main_task: str                   # Original task description
    subtasks: List[str]              # Ordered list of subtasks
    reasoning: str                   # Why tasks are decomposed this way
    estimated_steps: int             # Estimated number of actions needed
    difficulty: str                  # Difficulty level
    dependencies: Dict[int, List[int]] # Task dependencies (optional)
```

---

### Task Run Agent

**Module:** `gradio_ui/agent/task_run_agent.py`

Executes individual tasks and generates next actions.

```python
class TaskRunAgent(BaseAgent):
    """Executes tasks and determines next actions"""

    async def analyze(
        self,
        current_task: str,
        ui_elements: List[UIElement],
        screenshot_data: np.ndarray,
        previous_actions: Optional[List[Dict]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze current state and determine next action.

        Args:
            current_task: Current subtask to execute
            ui_elements: Available UI elements
            screenshot_data: Current screenshot
            previous_actions: History of previous actions
            context: Additional context

        Returns:
            {
                "success": bool,
                "action": Action,
                "reasoning": str,
                "target_element": UIElement,
                "is_complete": bool,
                "next_step": Optional[str]
            }
        """
        pass
```

#### Action Data Model

```python
@dataclass
class Action:
    """Represents an action to perform"""
    type: str                           # Action type (click, type, scroll, etc.)
    target: Optional[UIElement]         # Target UI element (if applicable)
    target_id: Optional[str]            # ID of target element
    parameters: Dict[str, Any]          # Action-specific parameters
    reasoning: str                      # Why this action was chosen
    confidence: float                   # Confidence in this action (0-1)

    @property
    def coordinates(self) -> Optional[Tuple[int, int]]:
        """Get action coordinates if applicable"""
        pass
```

#### Supported Actions

| Action Type | Parameters | Description |
|-------------|-----------|-------------|
| `click` | `target_id` | Click on element |
| `double_click` | `target_id` | Double-click on element |
| `right_click` | `target_id` | Right-click on element |
| `type` | `text`, `interval` | Type text into focused element |
| `key_press` | `key`, `modifiers` | Press keyboard key (shift, ctrl, alt) |
| `key_combination` | `keys` | Press multiple keys together |
| `scroll` | `direction`, `amount`, `x`, `y` | Scroll in direction (up/down/left/right) |
| `mouse_move` | `x`, `y` | Move mouse to coordinates |
| `drag` | `target_id`, `x`, `y` | Drag element to new position |
| `wait` | `seconds` | Wait for specified duration |
| `screenshot` | - | Capture current screen |

#### Example Action Responses

```json
{
  "success": true,
  "action": {
    "type": "click",
    "target_id": "elem_5",
    "parameters": {"button": "left"},
    "reasoning": "Click the login button",
    "confidence": 0.95
  },
  "is_complete": false,
  "next_step": "Wait for page to load"
}
```

```json
{
  "success": true,
  "action": {
    "type": "type",
    "parameters": {"text": "user@example.com", "interval": 0.05},
    "reasoning": "Type email into the input field",
    "confidence": 0.99
  },
  "is_complete": false
}
```

---

## Tool APIs

### BaseTool

**Module:** `gradio_ui/tools/base.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ToolResult:
    """Result of tool execution"""
    success: bool
    data: Any                        # Tool output data
    error: Optional[str] = None      # Error message if failed
    timestamp: datetime = field(default_factory=datetime.now)
    execution_time: float = 0.0      # Time taken to execute


class BaseTool(ABC):
    """Base class for all tools"""

    name: str                        # Tool identifier
    description: str                 # Tool description

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters.

        Returns:
            ToolResult with success status and data
        """
        pass
```

---

### Computer Tool

**Module:** `gradio_ui/tools/computer.py`

Provides interface control operations (mouse, keyboard, screen).

```python
class ComputerTool(BaseTool):
    """Controls computer input (mouse, keyboard, screen)"""

    name = "computer_control"

    def execute(
        self,
        action: str,
        **kwargs
    ) -> ToolResult:
        """
        Execute computer control action.

        Args:
            action: Type of action (click, type, scroll, etc.)
            **kwargs: Action-specific parameters

        Returns:
            ToolResult with execution status
        """
        pass
```

#### Supported Actions

```python
# Click action
tool.execute(
    action="click",
    x=500,           # x coordinate
    y=300,           # y coordinate
    button="left"    # "left", "right", "middle"
)

# Type action
tool.execute(
    action="type",
    text="Hello",    # text to type
    interval=0.05    # delay between characters (seconds)
)

# Keyboard action
tool.execute(
    action="key_press",
    key="enter",     # key name (enter, escape, tab, etc.)
    modifiers=["ctrl"]  # modifiers (shift, ctrl, alt)
)

# Combination
tool.execute(
    action="key_combination",
    keys=["ctrl", "c"]  # press Ctrl+C
)

# Scroll action
tool.execute(
    action="scroll",
    x=500,           # scroll position x
    y=300,           # scroll position y
    direction="down",  # "up", "down", "left", "right"
    amount=3         # number of scroll units
)

# Mouse move
tool.execute(
    action="mouse_move",
    x=500,           # target x
    y=300,           # target y
    duration=0.5     # movement duration (seconds)
)

# Drag
tool.execute(
    action="drag",
    start=(100, 100),  # start coordinates
    end=(200, 200),    # end coordinates
    duration=0.5       # drag duration (seconds)
)

# Wait
tool.execute(
    action="wait",
    seconds=2        # wait duration
)
```

---

### Screen Capture Tool

**Module:** `gradio_ui/tools/screen_capture.py`

Captures screenshots of the current screen state.

```python
class ScreenCaptureTool(BaseTool):
    """Captures screenshots"""

    name = "screen_capture"

    def execute(
        self,
        region: Optional[Tuple[int, int, int, int]] = None,
        include_cursor: bool = True,
        format: str = "numpy"
    ) -> ToolResult:
        """
        Capture screenshot.

        Args:
            region: Optional region (x, y, width, height) to capture
            include_cursor: Include mouse cursor in screenshot
            format: Output format ("numpy", "pil", "base64")

        Returns:
            ToolResult with screenshot data
        """
        pass
```

#### Return Data Formats

```python
# Numpy format
ToolResult(
    success=True,
    data={
        "image": np.ndarray,  # RGB image (height, width, 3)
        "size": (width, height),
        "cursor_position": (x, y)
    }
)

# PIL format
ToolResult(
    success=True,
    data={
        "image": PIL.Image,
        "size": (width, height),
        "cursor_position": (x, y)
    }
)

# Base64 format
ToolResult(
    success=True,
    data={
        "image": "data:image/png;base64,...",
        "size": (width, height),
        "cursor_position": (x, y)
    }
)
```

---

### Tool Collection

**Module:** `gradio_ui/tools/collection.py`

Manages and executes all available tools.

```python
class ToolCollection:
    """Manages collection of tools"""

    def __init__(self):
        """Initialize with default tools"""
        pass

    def register_tool(self, tool: BaseTool) -> None:
        """
        Register a new tool.

        Args:
            tool: Tool instance to register
        """
        pass

    def execute(
        self,
        tool_name: str,
        **kwargs
    ) -> ToolResult:
        """
        Execute a registered tool.

        Args:
            tool_name: Name of tool to execute
            **kwargs: Tool-specific parameters

        Returns:
            ToolResult from tool execution
        """
        pass

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get tool by name"""
        pass

    def list_tools(self) -> List[Dict[str, str]]:
        """
        List all registered tools.

        Returns:
            List of tool info (name, description)
        """
        pass
```

---

## Executor API

**Module:** `gradio_ui/executor/anthropic_executor.py`

Executes tool calls generated by Claude.

```python
class AnthropicExecutor:
    """Executes Claude-generated tool calls"""

    def __init__(self, tools: ToolCollection):
        """
        Initialize executor.

        Args:
            tools: ToolCollection with available tools
        """
        pass

    async def execute(
        self,
        tool_name: str,
        tool_input: Dict[str, Any]
    ) -> ToolResult:
        """
        Execute a tool call.

        Args:
            tool_name: Name of tool to execute
            tool_input: Input parameters for tool

        Returns:
            ToolResult from execution
        """
        pass

    def validate_tool_call(
        self,
        tool_name: str,
        tool_input: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate tool call before execution.

        Args:
            tool_name: Tool name to validate
            tool_input: Input to validate

        Returns:
            (is_valid, error_message)
        """
        pass
```

---

## Data Models

### Core Data Classes

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any

@dataclass
class Screenshot:
    """Screenshot data"""
    image: np.ndarray              # RGB image array
    width: int
    height: int
    cursor_position: Tuple[int, int]
    timestamp: datetime

@dataclass
class ScreenAnalysis:
    """Result of screen analysis"""
    screenshot: Screenshot
    elements: List[UIElement]
    text_content: str             # All extracted text combined
    analysis_time: float

@dataclass
class ExecutionContext:
    """Context during task execution"""
    task_id: str
    current_subtask: str
    iteration: int
    max_iterations: int = 50
    actions_taken: List[Action] = field(default_factory=list)
    last_screenshot: Optional[Screenshot] = None
    error_count: int = 0

@dataclass
class TaskResult:
    """Result of task execution"""
    success: bool
    task: str
    subtasks_completed: List[str]
    total_actions: int
    execution_time: float
    error: Optional[str] = None
    screenshots: List[Screenshot] = field(default_factory=list)
    actions_log: List[Action] = field(default_factory=list)
```

---

## LLM Integration

### Supported LLM Providers

#### OpenAI
```python
model_config = {
    "provider": "openai",
    "model": "gpt-4o",              # or "gpt-4o-2024-08-06"
    "api_key": "sk-...",
    "base_url": "https://api.openai.com/v1",
    "temperature": 0.7,
    "max_tokens": 4096
}
```

#### Yeka (2233.ai)
```python
model_config = {
    "provider": "yeka",
    "model": "gpt-4o",              # or "o1"
    "api_key": "sk-...",
    "base_url": "https://api.2233.ai/v1",
    "temperature": 0.7,
    "max_tokens": 4096
}
```

#### OpenAI-Next (API Proxy)
```python
model_config = {
    "provider": "openai-next",
    "model": "gpt-4o-2024-11-20",
    "api_key": "sk-...",
    "base_url": "https://api.openai-next.com/v1",
    "temperature": 0.7,
    "max_tokens": 4096
}
```

### Message Format

Agents use Claude's multi-modal message format:

```python
messages = [
    {
        "role": "system",
        "content": "You are a UI automation assistant..."
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Please analyze this screenshot and identify all buttons..."
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": "iVBORw0KGgoAAAANS..."
                }
            }
        ]
    }
]
```

### JSON Schema for Structured Output

Example for Task Plan Agent:

```python
schema = {
    "type": "object",
    "properties": {
        "main_task": {
            "type": "string",
            "description": "The main task to accomplish"
        },
        "subtasks": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of subtasks in order"
        },
        "reasoning": {
            "type": "string",
            "description": "Reasoning for task decomposition"
        }
    },
    "required": ["main_task", "subtasks", "reasoning"]
}
```

---

## Examples

### Example 1: Complete Task Execution Flow

```python
from gradio_ui.agent.vision_agent import VisionAgent
from gradio_ui.agent.task_plan_agent import TaskPlanAgent
from gradio_ui.agent.task_run_agent import TaskRunAgent
from gradio_ui.executor.anthropic_executor import AnthropicExecutor
from gradio_ui.tools.collection import ToolCollection

# Configuration
model_config = {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.7
}
api_key = "sk-..."

# Initialize agents
vision_agent = VisionAgent(model_config, api_key)
plan_agent = TaskPlanAgent(model_config, api_key)
run_agent = TaskRunAgent(model_config, api_key)
executor = AnthropicExecutor(ToolCollection())

# Step 1: Analyze current screen
analysis = await vision_agent.analyze(screenshot_path="current.png")
ui_elements = analysis["elements"]

# Step 2: Plan the task
plan = await plan_agent.analyze(
    task_description="Log in with email user@example.com",
    ui_elements=ui_elements,
    screenshot_data=analysis.get("screenshot")
)

subtasks = plan["subtasks"]

# Step 3: Execute each subtask
for subtask in subtasks:
    iteration = 0
    max_iterations = 20

    while iteration < max_iterations:
        # Get current screen state
        analysis = await vision_agent.analyze(screenshot_path="current.png")

        # Decide next action
        result = await run_agent.analyze(
            current_task=subtask,
            ui_elements=analysis["elements"],
            screenshot_data=analysis.get("screenshot")
        )

        action = result["action"]

        # Execute action
        exec_result = await executor.execute(
            tool_name="computer_control",
            tool_input={
                "action": action["type"],
                **action["parameters"]
            }
        )

        if result["is_complete"]:
            print(f"✓ Subtask complete: {subtask}")
            break

        iteration += 1
```

### Example 2: Using Vision Agent

```python
from gradio_ui.agent.vision_agent import VisionAgent

agent = VisionAgent(model_config, api_key)

result = await agent.analyze(screenshot_path="/path/to/screenshot.png")

if result["success"]:
    elements = result["elements"]

    # Find buttons
    buttons = [e for e in elements if e.type == "button"]

    # Find input fields
    inputs = [e for e in elements if e.type == "input"]

    # Print detected elements
    for elem in elements:
        print(f"ID: {elem.id}, Type: {elem.type}")
        print(f"  Text: {elem.text}")
        print(f"  Position: ({elem.x}, {elem.y})")
        print(f"  Size: {elem.width}x{elem.height}")
        print(f"  Caption: {elem.caption}")
        print(f"  Confidence: {elem.confidence}")
```

### Example 3: Custom Tool Implementation

```python
from gradio_ui.tools.base import BaseTool, ToolResult

class CustomSearchTool(BaseTool):
    """Custom tool for searching"""

    name = "custom_search"
    description = "Search for items in a database"

    def execute(self, query: str, limit: int = 10) -> ToolResult:
        try:
            # Your custom logic here
            results = self.search_database(query, limit)
            return ToolResult(
                success=True,
                data={"results": results}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )

    def search_database(self, query: str, limit: int):
        # Implementation
        pass
```

### Example 4: Using Tool Collection

```python
from gradio_ui.tools.collection import ToolCollection

tools = ToolCollection()

# List available tools
for tool_info in tools.list_tools():
    print(f"Tool: {tool_info['name']}")
    print(f"  Description: {tool_info['description']}")

# Execute a tool
result = tools.execute(
    "computer_control",
    action="click",
    x=500,
    y=300,
    button="left"
)

if result.success:
    print("Click successful")
else:
    print(f"Click failed: {result.error}")
```

---

## Error Handling

All API methods should handle errors gracefully:

```python
try:
    result = await agent.analyze(**params)
    if not result.get("success"):
        error = result.get("error")
        print(f"Agent error: {error}")
except Exception as e:
    print(f"Exception: {e}")
```

---

## Best Practices

1. **Always check success flag** before using results
2. **Handle timeouts** in API calls (default 30 seconds)
3. **Validate tool inputs** before execution
4. **Log actions** for debugging
5. **Use async/await** for agent calls
6. **Catch exceptions** at appropriate levels
7. **Implement retries** for network failures

---

For more details, see [ARCHITECTURE.md](./ARCHITECTURE.md) and [DEVELOPMENT.md](./DEVELOPMENT.md).
