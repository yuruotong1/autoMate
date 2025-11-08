# autoMate Architecture Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [Processing Pipeline](#processing-pipeline)
4. [Data Flow](#data-flow)
5. [Agent System](#agent-system)
6. [Tool System](#tool-system)
7. [Vision Pipeline](#vision-pipeline)

---

## System Overview

autoMate is a multi-agent AI automation system that combines computer vision, large language models (LLMs), and automated control to simulate human-like interactions with computer interfaces.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Gradio)                  │
│                   (gradio_ui/app.py)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Main Processing Loop (loop.py)                 │
│     - Coordinates agent execution                          │
│     - Manages task state and execution flow                │
└────────────────────────┬────────────────────────────────────┘
                         │
    ┌────────┬───────────┼───────────┬──────────┐
    │        │           │           │          │
┌───▼──┐┌────▼──┐┌──────▼────┐┌─────▼────┐┌────▼──┐
│Vision││ Task  ││   Task    ││ Tool    ││Config ││
│Agent ││ Plan  ││   Run     ││Executor ││Manage ││
│      ││ Agent ││   Agent   ││         ││       ││
└──────┘└───────┘└───────────┘└─────────┘└───────┘
    │        │           │           │          │
    └────────┴───────────┼───────────┴──────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│             Computer Vision Models & Tools                  │
│   - YOLO (UI Detection)                                    │
│   - Florence-2 (Image Captioning)                          │
│   - EasyOCR (Text Recognition)                             │
│   - PyAutoGUI (Computer Control)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Main Application Entry Point
**File:** `main.py`

Responsibilities:
- Initialize the application
- Download and verify pre-trained model weights
- Launch the Gradio web interface on `localhost:7888`
- Handle application lifecycle

```python
# Key functions:
- main() : Entry point
- download_models() : Initialize model weights
```

### 2. Web User Interface
**File:** `gradio_ui/app.py`

Provides a web-based interface with:
- **Chat Interface:** Accept natural language task descriptions
- **Settings Panel:** Configure API keys, models, and base URLs
- **Task Display:** Show active tasks and their progress
- **Screen Selector:** Allow users to focus on specific screen regions
- **History:** Display past interactions and results

Key Features:
- Real-time task updates via Gradio events
- Screenshot display with UI element overlays
- Settings persistence via environment variables
- Support for multiple LLM providers

### 3. Processing Loop
**File:** `gradio_ui/loop.py`

The orchestrator that coordinates the entire automation workflow:

```
User Input → Vision Agent → Task Plan Agent → Execution Loop
                                                   ├─ Task Run Agent
                                                   ├─ Tool Executor
                                                   ├─ Vision Agent
                                                   └─ Repeat
```

**Key Methods:**
- `run_loop()` : Main entry point for task execution
- `_vision_analysis()` : Analyze current screen state
- `_plan_tasks()` : Decompose user input into subtasks
- `_run_task()` : Execute a single task iteration
- `_execute_tool()` : Run LLM-generated tool calls

### 4. Agent System
**Base Class:** `gradio_ui/agent/base_agent.py`

Defines the interface for all agents:
- `analyze()` : Core analysis method
- `_format_prompt()` : Prepare input for LLM
- `_parse_response()` : Extract structured data from LLM output

#### Vision Agent
**File:** `gradio_ui/agent/vision_agent.py`

**Purpose:** Analyze current screen state and identify UI elements

**Process:**
1. Capture screenshot of current screen
2. Run YOLO to detect UI elements and their bounding boxes
3. Extract text from detected regions using EasyOCR
4. Generate descriptive captions using Florence-2 model
5. Return structured UIElement list with metadata

**Output Structure:**
```python
UIElement:
  - id: str (unique identifier)
  - bbox: (x, y, width, height)
  - text: str (extracted text content)
  - type: str (element type from YOLO)
  - caption: str (description from Florence-2)
  - confidence: float (detection confidence)
```

#### Task Plan Agent
**File:** `gradio_ui/agent/task_plan_agent.py`

**Purpose:** Decompose user request into actionable subtasks

**Process:**
1. Receive user input (task description)
2. Analyze current screen state from Vision Agent
3. Call Claude API with multi-modal prompt (text + screenshot)
4. Parse structured response containing task breakdown
5. Return list of subtasks with dependencies

**Claude Prompt Structure:**
- System: Task decomposition instructions
- User: Current screen screenshot + task description
- Schema: Expected JSON output format with task list

#### Task Run Agent
**File:** `gradio_ui/agent/task_run_agent.py`

**Purpose:** Execute individual tasks and decide next actions

**Process:**
1. Receive current subtask and screen state
2. Call Claude with vision capabilities
3. Claude analyzes screen and determines next action
4. Returns structured action with tool call
5. Tool executor runs the action
6. Feedback loop continues until subtask complete

**Interaction Model:**
- Uses Claude's `computer_control` tool
- Actions include: click, type, scroll, wait, key_press, etc.
- Iterative refinement based on screen feedback

---

## Processing Pipeline

### Step 1: Screen Analysis (Vision Agent)
```
Input: User task description
Process:
  1. Capture current screenshot
  2. Run YOLO on screenshot → UI element bounding boxes
  3. Extract text with EasyOCR for each region
  4. Generate captions with Florence-2
  5. Create UIElement objects with metadata
Output: List of UIElements with positions and descriptions
```

### Step 2: Task Planning (Task Plan Agent)
```
Input: User task + list of UIElements from Vision Agent
Process:
  1. Prepare multi-modal prompt with screenshot
  2. Call Claude API with task decomposition prompt
  3. Claude analyzes screen and breaks task into subtasks
  4. Parse JSON response containing task list
Output: List of subtasks with natural language descriptions
```

### Step 3: Task Execution Loop (Task Run Agent + Executor)
```
For each subtask:
  1. Capture screenshot
  2. Run Vision Agent analysis
  3. Call Task Run Agent with current subtask
  4. Claude decides next action (click, type, scroll, etc.)
  5. Execute action via Tool Executor
  6. Check if subtask is complete
  7. Repeat until subtask is done or max iterations reached

Output: Execution results and reasoning at each step
```

---

## Data Flow

### Core Data Structures

```
UserInput
  ├─ task: str (natural language)
  ├─ screen_region: Optional[Tuple] (selected region)
  └─ model_config: Dict[str, Any]

ScreenAnalysis
  ├─ screenshot: np.ndarray (RGB image)
  ├─ elements: List[UIElement]
  ├─ cursor_position: Tuple[int, int]
  └─ timestamp: datetime

UIElement
  ├─ id: str
  ├─ bbox: BoundingBox (x, y, w, h)
  ├─ text: str
  ├─ type: str (button, input, text, etc.)
  ├─ caption: str
  └─ confidence: float

TaskPlan
  ├─ main_task: str
  ├─ subtasks: List[str]
  └─ reasoning: str

ExecutionState
  ├─ current_subtask: str
  ├─ actions_taken: List[Action]
  ├─ last_screenshot: Screenshot
  ├─ iteration_count: int
  └─ status: "running" | "completed" | "failed"

Action
  ├─ type: str (click, type, scroll, wait, key_press)
  ├─ target: Optional[UIElement]
  ├─ parameters: Dict[str, Any]
  ├─ reasoning: str
  └─ result: ActionResult
```

### Data Flow Diagram

```
┌──────────────────┐
│   User Input     │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ Vision Agent             │
│ (Screenshot Analysis)    │
└────────┬─────────────────┘
         │UIElement List
         ▼
┌──────────────────────────┐
│ Task Plan Agent          │
│ (Decompose Task)         │
└────────┬─────────────────┘
         │ Task List
         ▼
    ┌────────────────────────────────────────┐
    │ Execution Loop (for each subtask)      │
    │                                        │
    │ 1. Vision Agent (Screenshot)           │
    │    ├─ Capture Screen                   │
    │    └─ Detect UI Elements               │
    │                                        │
    │ 2. Task Run Agent (Decide Action)      │
    │    ├─ Analyze State                    │
    │    └─ Generate Action                  │
    │                                        │
    │ 3. Tool Executor (Execute Action)      │
    │    ├─ Click/Type/Scroll                │
    │    └─ Update State                     │
    │                                        │
    │ 4. Check Progress                      │
    │    ├─ Task Complete? → Exit Loop       │
    │    └─ Not Complete? → Repeat from 1    │
    └────────────┬────────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │ Result & History │
         └──────────────────┘
```

---

## Agent System

### Base Agent Class
**File:** `gradio_ui/agent/base_agent.py`

All agents inherit from `BaseAgent` which provides:

```python
class BaseAgent:
    def __init__(self, model_config: Dict, api_key: str):
        self.model_config = model_config
        self.api_key = api_key
        self.client = initialize_anthropic_client(api_key, base_url)

    async def analyze(self, **kwargs) -> Dict:
        """Override in subclasses"""
        pass

    def _format_prompt(self, **kwargs) -> str:
        """Format input for LLM"""
        pass

    def _parse_response(self, response: str) -> Dict:
        """Parse LLM output"""
        pass
```

### Agent Communication Protocol

Agents communicate through:
1. **Input:** Dictionary with task-specific parameters
2. **Processing:** Call Anthropic Claude API with structured prompts
3. **Output:** Structured JSON response (validated against schema)

### Vision Agent Flow

```
Input: Screenshot path/data
├─ Resize image if needed
├─ Run YOLO detection
│  └─ Get bounding boxes and class predictions
├─ Extract text with EasyOCR
│  └─ Get text content and coordinates
├─ Generate captions with Florence-2
│  └─ Get description for each region
├─ Combine results into UIElements
└─ Return structured UIElement list
```

### Task Plan Agent Flow

```
Input: User task + UIElement list + screenshot
├─ Format prompt with task and visual context
├─ Call Claude API with vision capabilities
├─ Claude analyzes current screen
├─ Claude decomposes task into subtasks
├─ Parse response JSON
└─ Return task breakdown
```

### Task Run Agent Flow

```
Input: Current subtask + UIElement list + screenshot
├─ Format prompt with task and visual context
├─ Call Claude with computer_control tool
├─ Claude decides next action
├─ Parse action response
├─ Prepare action parameters
└─ Return action for execution
```

---

## Tool System

### Base Tool Interface
**File:** `gradio_ui/tools/base.py`

```python
class BaseTool:
    name: str
    description: str

    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool"""
        pass

class ToolResult:
    success: bool
    data: Any
    error: Optional[str]
    timestamp: datetime
```

### Computer Control Tool
**File:** `gradio_ui/tools/computer.py`

Implements interface control operations:

**Supported Actions:**

| Action | Parameters | Description |
|--------|-----------|-------------|
| `click` | x, y, button | Click at coordinates |
| `double_click` | x, y | Double-click at coordinates |
| `right_click` | x, y | Right-click at coordinates |
| `type` | text, interval | Type text character by character |
| `key_press` | key, modifiers | Press keyboard keys (ctrl, shift, alt) |
| `mouse_move` | x, y, duration | Move mouse to position |
| `drag` | start, end, duration | Drag from one position to another |
| `scroll` | x, y, distance, direction | Scroll up/down/left/right |
| `wait` | seconds | Pause execution |

**Example Usage:**
```python
computer_tool = ComputerTool()
result = computer_tool.execute(
    action="click",
    x=500,
    y=300,
    button="left"
)
```

### Screen Capture Tool
**File:** `gradio_ui/tools/screen_capture.py`

Captures current screen state:
- Takes full-screen screenshot
- Overlays mouse cursor
- Can capture specific regions
- Returns image data in multiple formats (numpy, PIL, base64)

### Tool Collection Manager
**File:** `gradio_ui/tools/collection.py`

Manages all available tools:
- Registers tools
- Validates tool calls
- Executes tools with error handling
- Maintains tool state and history

---

## Vision Pipeline

### Component Overview

```
Screenshot
    │
    ├─→ YOLO v8
    │   └─ Detects UI elements
    │      └─ Returns bounding boxes & classes
    │
    ├─→ EasyOCR
    │   └─ Extracts text
    │      └─ Returns text & confidence
    │
    └─→ Florence-2-base-ft
        └─ Generates descriptions
           └─ Returns captions
```

### Vision Models Used

#### 1. YOLO v8 (Object Detection)
- **Model:** YOLOv8n (nano) or YOLOv8s (small)
- **Task:** Detect UI elements (buttons, inputs, text, images, etc.)
- **Input:** Screenshot (any resolution)
- **Output:** Bounding boxes with class predictions

#### 2. Florence-2-base-ft (Image Understanding)
- **Model:** Florence-2-base-ft from AI-ModelScope
- **Task:** Generate descriptive captions for image regions
- **Input:** Cropped image regions
- **Output:** Natural language descriptions

#### 3. EasyOCR (Text Recognition)
- **Models:** English + Chinese support
- **Task:** Extract text from images
- **Input:** Screenshot or image regions
- **Output:** Text content with bounding boxes

### Vision Processing Steps

```
1. Screenshot Capture
   ├─ Input: Screen area to capture
   ├─ Process: Use Pillow/OpenCV to capture
   └─ Output: RGB numpy array

2. YOLO Detection
   ├─ Input: Screenshot image
   ├─ Process: Run YOLO inference
   └─ Output: Detections with boxes and classes

3. Region Extraction
   ├─ Input: Screenshot + YOLO detections
   ├─ Process: Crop image regions for each detection
   └─ Output: Cropped images for each element

4. Text Recognition
   ├─ Input: Cropped regions
   ├─ Process: Run EasyOCR on regions
   └─ Output: Text content for each region

5. Caption Generation
   ├─ Input: Cropped regions
   ├─ Process: Run Florence-2 on regions
   └─ Output: Descriptions for each element

6. UIElement Assembly
   ├─ Input: All extracted data
   ├─ Process: Combine into UIElement objects
   └─ Output: Structured UIElement list
```

### Model Configuration

Models are downloaded and cached in `weights/AI-ModelScope/`:
- `OmniParser-v2.0/` - YOLO weights
- `Florence-2-base-ft/` - Florence model weights

Automatic download and verification:
```python
# models/download_weights.py
- Checks if models exist
- Downloads from ModelScope if missing
- Verifies checksums
- Extracts and organizes files
```

---

## Configuration & State Management

### Configuration Sources (Priority Order)
1. Environment variables
2. Runtime configuration via UI
3. Hardcoded defaults

### LLM Configuration
```python
ModelConfig:
  - provider: str ("openai", "yeka", "openai-next")
  - model: str (gpt-4o, o1, etc.)
  - base_url: str (API endpoint)
  - api_key: str (authentication)
  - temperature: float (0.0-1.0)
  - max_tokens: int
```

### API Provider Support
- **OpenAI:** Official ChatGPT API
- **Yeka (2233.ai):** API proxy service
- **OpenAI-Next:** API-compatible endpoint

---

## Error Handling & Robustness

### Error Types & Recovery

| Error Type | Source | Recovery |
|-----------|--------|----------|
| API Error | Claude API | Retry with exponential backoff |
| Vision Error | YOLO/OCR | Skip element or use OCR-only |
| Execution Error | PyAutoGUI | Log error, continue next iteration |
| Model Not Found | Startup | Download model, restart |
| GPU Out of Memory | Vision | Fall back to CPU |

### Retry Strategy
- API calls: Up to 3 retries with exponential backoff
- Vision analysis: Skip problematic elements gracefully
- Task execution: Max iterations limit (default 50)

---

## Performance Considerations

### Optimization Areas

1. **Vision Pipeline:**
   - Model inference speed (YOLO, Florence-2, EasyOCR)
   - GPU memory usage
   - Image processing overhead

2. **LLM Calls:**
   - Batch vision images when possible
   - Optimize prompt length
   - Use model-appropriate temperature

3. **Tool Execution:**
   - Minimize screenshot delays
   - Cache stable screen states
   - Parallel where possible

### Hardware Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- GPU: Optional (CPU fallback available)

**Recommended:**
- CPU: 8+ cores
- RAM: 16GB
- GPU: NVIDIA 8GB+ (CUDA 11.8+)

---

## Extension Points

Developers can extend autoMate by:

1. **Adding Custom Tools:** Inherit from `BaseTool`
2. **Creating Custom Agents:** Inherit from `BaseAgent`
3. **Adding Vision Models:** Integrate with vision pipeline
4. **Custom UI Components:** Extend Gradio interface
5. **LLM Integration:** Add provider support

See [DEVELOPMENT.md](./DEVELOPMENT.md) for implementation details.
