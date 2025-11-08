# Configuration Guide

## Table of Contents
1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [API Key Configuration](#api-key-configuration)
4. [Model Configuration](#model-configuration)
5. [Advanced Configuration](#advanced-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### System Requirements

**Minimum:**
- OS: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- Python: 3.12+
- RAM: 8GB
- Disk Space: 20GB (for models)

**Recommended:**
- CPU: 8+ cores
- GPU: NVIDIA RTX 3060 (8GB VRAM) or better
- CUDA: 11.8+ (for GPU support)
- RAM: 16GB+
- Disk Space: 30GB SSD

### Step 1: Clone Repository

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
```

### Step 2: Create Python Environment

Using Conda (recommended):
```bash
conda create -n automate python=3.12
conda activate automate
```

Using venv:
```bash
python3.12 -m venv automate_env
source automate_env/bin/activate  # On Windows: automate_env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Model Weights

Models are automatically downloaded on first run. To manually pre-download:

```bash
python -c "from util.download_weights import download_weights; download_weights()"
```

This downloads:
- **YOLO v8 nano** (~7MB) - For UI element detection
- **Florence-2-base-ft** (~10GB) - For image understanding
- **EasyOCR** models (~200MB) - For text recognition

**Note:** Florence-2 download requires sufficient disk space and internet bandwidth. Consider 20-30 minutes for first-time download.

### Step 5: Verify Installation

```bash
python main.py
```

Should output:
```
Loading models...
Starting Gradio server...
Server running at http://localhost:7888/
```

---

## Environment Setup

### Operating System Specific Setup

#### Windows
1. Install [Python 3.12](https://www.python.org/downloads/)
2. Ensure Python is added to PATH during installation
3. Install [Git for Windows](https://git-scm.com/download/win)
4. Install [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) (optional, for GPU)

#### macOS
```bash
# Using Homebrew
brew install python@3.12
brew install git

# For GPU support (Apple Silicon)
# Note: PyTorch will auto-detect and use Metal Performance Shaders
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
sudo apt install git

# For NVIDIA GPU support
# Follow official CUDA installation guide
```

### Virtual Environment Activation

**Linux/macOS:**
```bash
source automate_env/bin/activate
```

**Windows (PowerShell):**
```powershell
.\automate_env\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
automate_env\Scripts\activate.bat
```

---

## API Key Configuration

### Setting Up API Keys

autoMate supports multiple LLM providers. You need at least one API key to function.

#### Option 1: Environment Variables

```bash
# Linux/macOS
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export OPENAI_API_BASE="https://api.openai.com/v1"

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:OPENAI_API_KEY="sk-..."
$env:OPENAI_API_BASE="https://api.openai.com/v1"

# Windows Command Prompt
set ANTHROPIC_API_KEY=sk-ant-...
set OPENAI_API_KEY=sk-...
set OPENAI_API_BASE=https://api.openai.com/v1
```

#### Option 2: Configuration File

Create `~/.anthropic/api_key`:
```bash
sk-ant-your-api-key-here
```

#### Option 3: Web UI Configuration

1. Open `http://localhost:7888/`
2. Navigate to "Settings" tab
3. Enter API key and model configuration
4. Click "Save Settings"

### Obtaining API Keys

#### Anthropic API
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create account or sign in
3. Navigate to "API Keys"
4. Create new key
5. Copy key and store securely

#### OpenAI API
1. Visit [platform.openai.com](https://platform.openai.com)
2. Create account or sign in
3. Navigate to "API Keys"
4. Create new key
5. Copy key and store securely

#### Yeka (2233.ai)
1. Visit [2233.ai](https://2233.ai)
2. Register and log in
3. Navigate to API settings
4. Create new key
5. Copy key for use

---

## Model Configuration

### Supported Models

#### OpenAI
```python
{
    "provider": "openai",
    "model": "gpt-4o",                    # Latest recommended
    "api_key": "sk-...",
    "base_url": "https://api.openai.com/v1",
    "temperature": 0.7,
    "max_tokens": 4096
}
```

Available models:
- `gpt-4o` - Latest O model with best performance
- `gpt-4o-2024-08-06` - Stable version
- `gpt-4o-2024-11-20` - Recent version
- `o1` - Reasoning model (requires temperature=1)
- `gpt-4-turbo` - Previous generation

#### Anthropic Claude
```python
{
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",  # Recommended
    "api_key": "sk-ant-...",
    "temperature": 0.7,
    "max_tokens": 4096
}
```

Available models:
- `claude-3-5-sonnet-20241022` - Recommended for automation
- `claude-3-opus-20240229` - More powerful but slower
- `claude-3-sonnet-20240229` - Balanced performance

#### Yeka (2233.ai)
```python
{
    "provider": "yeka",
    "model": "gpt-4o",                    # Most models supported
    "api_key": "sk-...",
    "base_url": "https://api.2233.ai/v1",
    "temperature": 0.7,
    "max_tokens": 4096
}
```

#### OpenAI-Next (API Proxy)
```python
{
    "provider": "openai-next",
    "model": "gpt-4o-2024-11-20",
    "api_key": "sk-...",
    "base_url": "https://api.openai-next.com/v1",
    "temperature": 0.7,
    "max_tokens": 4096
}
```

### Configuration in Web UI

1. **Open Settings Tab:**
   - Navigate to `http://localhost:7888/`
   - Click "Settings" tab

2. **Configure API:**
   - Select Provider (OpenAI, Anthropic, Yeka, OpenAI-Next)
   - Enter API Key
   - (Optional) Enter Custom Base URL for proxy services

3. **Select Model:**
   - Choose model from dropdown
   - Adjust temperature (0.0-1.0, lower=more deterministic)
   - Set max tokens (higher=longer responses)

4. **Apply Settings:**
   - Click "Save Settings"
   - Settings persist across sessions

### Programmatic Configuration

```python
from gradio_ui.agent.vision_agent import VisionAgent

config = {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 4096
}

api_key = "sk-..."
base_url = "https://api.openai.com/v1"  # Optional

agent = VisionAgent(config, api_key, base_url)
```

---

## Advanced Configuration

### GPU Configuration

#### NVIDIA CUDA

Check CUDA version:
```bash
nvidia-smi
```

Install correct PyTorch version:
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# For CUDA 12.4
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

#### Apple Metal (M1/M2/M3 Macs)

PyTorch will automatically detect and use Metal Performance Shaders:
```bash
# Standard installation works, will auto-select Metal
pip install torch torchvision
```

#### CPU-Only Mode

For systems without GPU (slower but functional):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Memory Optimization

#### Reduce Model Load

In `gradio_ui/agent/vision_agent.py`, you can use smaller models:

```python
# Use YOLOv8 nano instead of small
self.yolo_model = YOLO("yolov8n.pt")  # nano

# Or disable Florence-2 captions for speed
self.use_florence = False
```

#### Batch Processing

For processing multiple screenshots:
```python
from gradio_ui.tools.screen_capture import ScreenCaptureTool

capture_tool = ScreenCaptureTool()

# Capture and analyze multiple regions
results = []
for region in regions:
    result = capture_tool.execute(region=region)
    results.append(result)
```

### Custom Model Paths

Override model download paths in environment:

```bash
# Set custom models directory
export AUTOMATE_MODELS_DIR="/custom/path/to/models"

# Set specific model paths
export YOLO_MODEL_PATH="/custom/yolov8n.pt"
export FLORENCE_MODEL_PATH="/custom/florence-2-base-ft"
```

### Screen Region Selection

Limit processing to specific screen area for performance:

1. In Web UI:
   - Click "Screen Selector" button
   - Click and drag to select region
   - Automation will focus on this region

2. Programmatically:
```python
focus_region = (x, y, width, height)
result = await vision_agent.analyze(
    screenshot_path="...",
    focus_region=focus_region
)
```

### Request Timeout Configuration

Adjust API timeout (in seconds):

```python
# In gradio_ui/agent/base_agent.py
self.api_timeout = 60  # Default 30
```

### Logging Configuration

Enable detailed logging:

```bash
# Set logging level
export LOG_LEVEL=DEBUG

# Run with logging
python main.py --log-level DEBUG
```

---

## Environment Variables

Complete list of configurable environment variables:

```bash
# API Configuration
ANTHROPIC_API_KEY          # Anthropic API key
OPENAI_API_KEY            # OpenAI API key
OPENAI_API_BASE           # OpenAI base URL (for proxies)
YEKA_API_KEY              # Yeka API key
YEKA_API_BASE             # Yeka base URL

# Model Configuration
AUTOMATE_MODEL_PROVIDER   # Default: "openai"
AUTOMATE_MODEL_NAME       # Default: "gpt-4o"
AUTOMATE_TEMPERATURE      # Default: 0.7
AUTOMATE_MAX_TOKENS       # Default: 4096

# Performance
AUTOMATE_MODELS_DIR       # Directory for downloaded models
CUDA_VISIBLE_DEVICES      # GPU selection (e.g., "0,1")
PYTORCH_CUDA_ALLOC_CONF   # CUDA memory config

# Behavior
AUTOMATE_MAX_ITERATIONS   # Max steps per task (default: 50)
AUTOMATE_TIMEOUT          # API timeout in seconds (default: 30)
AUTOMATE_ENABLE_LOGGING   # Enable debug logging (default: false)

# UI
GRADIO_PORT               # Port for web UI (default: 7888)
GRADIO_SERVER_NAME        # Server name (default: 127.0.0.1)
```

---

## Troubleshooting Configuration

### Issue: "CUDA out of memory"

**Solution:**
```bash
# Use CPU instead
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Or reduce model size
export AUTOMATE_YOLO_SIZE="nano"  # Instead of small
```

### Issue: "Could not find CUDA libraries"

**Solution:**
```bash
# Ensure PyTorch CUDA version matches system CUDA
nvidia-smi  # Check your CUDA version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124  # Replace 124 with your version
```

### Issue: "API key not working"

**Solution:**
1. Verify API key is correct (copy from provider)
2. Check key has necessary permissions
3. Ensure key is not expired
4. Try in Web UI settings first

```bash
# Test API key
python -c "
import os
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
msg = client.messages.create(model='claude-3-5-sonnet-20241022', max_tokens=100, messages=[{'role': 'user', 'content': 'test'}])
print('✓ API key works')
"
```

### Issue: "Models not downloading"

**Solution:**
```bash
# Check internet connection
ping google.com

# Manually download models
python -c "from util.download_weights import download_weights; download_weights()"

# Use mirror/proxy if in region with restrictions
export HF_ENDPOINT="https://hf-mirror.com"
```

### Issue: "Port 7888 already in use"

**Solution:**
```bash
# Use different port
export GRADIO_PORT=7889
python main.py
```

---

## Security Best Practices

### Protecting API Keys

1. **Never commit API keys to git:**
```bash
# Create .env file (add to .gitignore)
ANTHROPIC_API_KEY="sk-ant-..."
OPENAI_API_KEY="sk-..."

# Load from .env
export $(cat .env | xargs)
```

2. **Use environment variables:**
```bash
# Safer than hardcoding
export ANTHROPIC_API_KEY="your-key-here"
python main.py
```

3. **Use .env with python-dotenv:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
```

4. **Restrict file permissions:**
```bash
chmod 600 ~/.anthropic/api_key
```

### Data Privacy

- All processing happens locally
- Screenshots are not uploaded (unless using cloud API)
- API calls only send task descriptions and results
- Configure local-only operation by using self-hosted models

---

## Next Steps

- [Architecture Guide](./ARCHITECTURE.md) - Understand system design
- [API Reference](./API.md) - Detailed API documentation
- [Development Guide](./DEVELOPMENT.md) - Extend and contribute
- [Troubleshooting](./TROUBLESHOOTING.md) - Common issues
