# Troubleshooting Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Dependency Issues](#dependency-issues)
3. [API & Configuration Issues](#api--configuration-issues)
4. [Runtime Issues](#runtime-issues)
5. [Performance Issues](#performance-issues)
6. [Vision & Detection Issues](#vision--detection-issues)
7. [Task Execution Issues](#task-execution-issues)
8. [GPU/Hardware Issues](#gpuhardware-issues)
9. [FAQ](#faq)

---

## Installation Issues

### Issue: Python 3.12 not found

**Symptoms:**
```
python3.12: command not found
```

**Solutions:**

1. **Check installed Python version:**
```bash
python --version
python3 --version
python3.12 --version
```

2. **Install Python 3.12:**

**macOS (Homebrew):**
```bash
brew install python@3.12
brew link python@3.12
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Ensure "Add Python to PATH" is checked

3. **Use specific python version:**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

---

### Issue: pip is not available

**Symptoms:**
```
pip: command not found
```

**Solutions:**

1. **Install pip for Python 3.12:**

**Linux/macOS:**
```bash
python3.12 -m ensurepip --upgrade
```

**Windows:**
```cmd
python -m ensurepip --upgrade
```

2. **Use python module directly:**
```bash
python -m pip install -r requirements.txt
```

---

### Issue: Cannot create virtual environment

**Symptoms:**
```
Error: Command '[...] -m venv' failed with exit code 1
```

**Solutions:**

1. **Install venv module:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3.12-venv
```

**macOS:**
```bash
# Usually included with Python
# If missing: reinstall Python via Homebrew
```

2. **Use conda instead:**
```bash
conda create -n automate python=3.12
conda activate automate
pip install -r requirements.txt
```

3. **Use alternative location:**
```bash
python3.12 -m venv /tmp/automate_venv
source /tmp/automate_venv/bin/activate
```

---

## Dependency Issues

### Issue: `pip install -r requirements.txt` fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**

1. **Upgrade pip, setuptools, wheel:**
```bash
pip install --upgrade pip setuptools wheel
```

2. **Install dependencies one by one to identify problem:**
```bash
pip install anthropic
pip install gradio
pip install torch
# Continue with other dependencies
```

3. **Check Python version compatibility:**
```bash
python --version  # Should be 3.12+
```

4. **Try with specific requirement versions:**
```bash
pip install -r requirements.txt --only-binary :all:
```

---

### Issue: PyTorch installation fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement torch
```

**Solutions:**

1. **Install CPU-only version (no GPU):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

2. **Check and install CUDA-compatible version:**
```bash
# Check NVIDIA CUDA version
nvidia-smi

# Install for specific CUDA version (example: CUDA 12.1)
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

3. **Use pre-built wheels:**
```bash
# Download wheel file manually from PyTorch website
pip install /path/to/torch-*.whl
```

---

### Issue: Incompatible library versions

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages
```

**Solutions:**

1. **Clear pip cache:**
```bash
pip cache purge
```

2. **Use specific versions:**
```bash
pip install gradio==4.0.0
pip install anthropic==0.15.0
```

3. **Recreate virtual environment:**
```bash
# Backup your settings
deactivate
rm -rf venv

# Create fresh environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## API & Configuration Issues

### Issue: API key not accepted

**Symptoms:**
```
Authentication failed
401 Unauthorized
Invalid API key
```

**Solutions:**

1. **Verify API key format:**
   - OpenAI keys start with `sk-`
   - Anthropic keys start with `sk-ant-`
   - Check for extra spaces/characters

2. **Test API key directly:**

**Anthropic:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python -c "
from anthropic import Anthropic
client = Anthropic()
msg = client.messages.create(
    model='claude-3-5-sonnet-20241022',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'test'}]
)
print('✓ API key works')
"
```

**OpenAI:**
```bash
export OPENAI_API_KEY="sk-..."
python -c "
from openai import OpenAI
client = OpenAI()
msg = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': 'test'}]
)
print('✓ API key works')
"
```

3. **Check key expiration/permissions:**
   - Visit API provider website
   - Verify key is not expired
   - Verify key has required permissions
   - Try creating a new key

4. **Check API provider status:**
   - Is the API provider online?
   - Are there any service disruptions?
   - Check provider's status page

---

### Issue: "No API key provided"

**Symptoms:**
```
Error: No API key provided
Could not find api key in environment
```

**Solutions:**

1. **Set environment variable:**

**Linux/macOS:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py
```

**Windows PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
python main.py
```

**Windows Command Prompt:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
python main.py
```

2. **Create .env file:**
```bash
# Create .env file
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env

# Load in Python
from dotenv import load_dotenv
load_dotenv()
```

3. **Use Web UI settings:**
   - Open `http://localhost:7888/`
   - Go to Settings tab
   - Enter API key directly

---

### Issue: Wrong API base URL

**Symptoms:**
```
Connection error
API endpoint not found
```

**Solutions:**

1. **Verify correct base URL:**

| Provider | Base URL |
|----------|----------|
| OpenAI | `https://api.openai.com/v1` |
| Anthropic | Default (built-in) |
| Yeka | `https://api.2233.ai/v1` |
| OpenAI-Next | `https://api.openai-next.com/v1` |

2. **Update environment variable:**
```bash
export OPENAI_API_BASE="https://api.openai.com/v1"
```

3. **Test connection:**
```bash
curl -H "Authorization: Bearer sk-..." \
  https://api.openai.com/v1/models
```

---

## Runtime Issues

### Issue: Application won't start

**Symptoms:**
```
Traceback (most recent call last):
  ...
```

**Solutions:**

1. **Check Python version:**
```bash
python --version  # Should be 3.12+
```

2. **Verify dependencies installed:**
```bash
pip list | grep -E "anthropic|gradio|torch"
```

3. **Run with debug output:**
```bash
python main.py --verbose
PYTHONVERBOSE=2 python main.py
```

4. **Check port availability:**
```bash
# Check if port 7888 is in use
lsof -i :7888  # macOS/Linux
netstat -ano | findstr :7888  # Windows

# Use different port
export GRADIO_PORT=7889
python main.py
```

5. **Clear cache and models:**
```bash
rm -rf ~/.cache/huggingface
rm -rf ./weights
python main.py  # Will re-download models
```

---

### Issue: "Module not found" error

**Symptoms:**
```
ModuleNotFoundError: No module named 'gradio_ui'
```

**Solutions:**

1. **Verify installation directory:**
```bash
pwd  # Should be in autoMate directory
ls -la gradio_ui/  # Should exist
```

2. **Reinstall package:**
```bash
pip install -e .
```

3. **Check Python path:**
```bash
python -c "import sys; print(sys.path)"
```

4. **Use absolute imports:**
```bash
cd /path/to/autoMate
python main.py
```

---

### Issue: "No module named anthropic"

**Symptoms:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solutions:**

1. **Activate virtual environment:**
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

2. **Install Anthropic package:**
```bash
pip install anthropic
```

3. **Check pip location:**
```bash
which pip
pip show anthropic
```

---

## Performance Issues

### Issue: Slow model loading

**Symptoms:**
- Application takes 30+ seconds to start
- Models loading very slowly

**Solutions:**

1. **Check disk I/O:**
```bash
# Monitor disk activity
iotop  # Linux
Activity Monitor  # macOS
```

2. **Move models to faster storage:**
```bash
# Use SSD instead of HDD
export AUTOMATE_MODELS_DIR="/fast/ssd/models"
```

3. **Use smaller models:**
```python
# In vision_agent.py, use nano instead of small
self.yolo_model = YOLO("yolov8n.pt")
```

4. **Pre-warm models:**
```bash
python -c "
from gradio_ui.agent.vision_agent import VisionAgent
config = {'model': 'gpt-4o'}
agent = VisionAgent(config, 'key')
# Models now loaded
print('Ready!')
"
```

---

### Issue: Task execution very slow

**Symptoms:**
- Each action takes 10+ seconds
- Vision analysis very slow

**Solutions:**

1. **Check API latency:**
```bash
time curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

2. **Reduce image quality:**
```python
# Lower resolution for faster processing
screenshot = cv2.resize(image, (960, 540))
```

3. **Use smaller models:**
   - Use gpt-4o-mini instead of gpt-4o
   - Use smaller YOLO model (nano)
   - Disable Florence-2 captions

4. **Optimize prompt length:**
```python
# Shorter, more focused prompts
shorter_prompt = "Click login button"
# Instead of
longer_prompt = """Please analyze the current screen and click on the button that says 'Login'..."""
```

---

## Vision & Detection Issues

### Issue: UI elements not being detected

**Symptoms:**
- Vision agent returns empty element list
- YOLO not finding any elements

**Solutions:**

1. **Check screenshot quality:**
```bash
# Verify screenshot is being captured
python -c "
from gradio_ui.tools.screen_capture import ScreenCaptureTool
tool = ScreenCaptureTool()
result = tool.execute()
if result.success:
    from PIL import Image
    img = Image.fromarray(result.data['image'])
    img.save('debug_screenshot.png')
    print('Screenshot saved')
"
```

2. **Adjust YOLO confidence threshold:**
```python
# In vision_agent.py
results = model.predict(image, conf=0.3)  # Lower threshold
```

3. **Use larger YOLO model:**
```python
# Use small instead of nano
self.yolo_model = YOLO("yolov8s.pt")
```

4. **Check screen settings:**
   - High DPI scaling can cause issues
   - Try disabling scaling
   - Ensure reasonable resolution (1920x1080 minimum)

---

### Issue: OCR not extracting text correctly

**Symptoms:**
- Extracted text is garbled
- Text recognition failing

**Solutions:**

1. **Check text is actually visible:**
```bash
# Take screenshot and inspect manually
import pyautogui
pyautogui.screenshot().save('check.png')
```

2. **Adjust EasyOCR parameters:**
```python
# In vision_agent.py
result = reader.readtext(image, low_text=0.1)  # Lower threshold
```

3. **Add specific languages:**
```python
# Initialize with English + Chinese
reader = easyocr.Reader(['en', 'ch_sim'], gpu=True)
```

4. **Preprocess image:**
```python
import cv2
# Improve contrast
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
enhanced = cv2.equalizeHist(gray)
```

---

### Issue: Florence-2 captions are generic

**Symptoms:**
- Captions like "a button" instead of "login button"
- Unclear descriptions

**Solutions:**

1. **Use model fine-tuned for UI:**
```python
# Current model is already fine-tuned for UI
# Consider custom fine-tuning for specific domains
```

2. **Provide context to Claude:**
```python
# Include surrounding elements in context
"This button is in the top-right corner, next to the 'Settings' link"
```

3. **Post-process captions:**
```python
# Enhance captions based on extracted text
if element.text:
    element.caption = f"Button labeled: {element.text}"
```

---

## Task Execution Issues

### Issue: Task doesn't complete

**Symptoms:**
- Task runs for max iterations without completing
- Agent stuck in loop

**Solutions:**

1. **Check task feasibility:**
   - Is the task actually possible?
   - Are all required UI elements visible?
   - Is the app in correct state?

2. **Increase iteration limit:**
```python
# In loop.py
max_iterations = 100  # Default 50
```

3. **Add more specific instructions:**
```python
# Instead of "Log in"
# Use "Click the email input, type user@example.com, then click Login"
```

4. **Check error logs:**
```bash
export LOG_LEVEL=DEBUG
python main.py
```

5. **Break into smaller subtasks:**
```python
# Instead of one large task
# "Fill form and submit"
# Use multiple smaller tasks
# 1. "Fill email field"
# 2. "Fill password field"
# 3. "Click submit"
```

---

### Issue: Wrong element being clicked

**Symptoms:**
- Agent clicks wrong button
- Clicks outside element

**Solutions:**

1. **Verify element detection:**
```python
# Get element coordinates
print(f"Element: {element.id}")
print(f"Position: ({element.x}, {element.y})")
print(f"Size: {element.width}x{element.height}")
```

2. **Check element matching:**
   - Ensure unique element IDs
   - Verify element text matches
   - Check coordinates are accurate

3. **Add explicit instructions:**
```python
# Instead of relying on detection
# "Click the button with text 'Login' in the top-right"
```

4. **Adjust click offset:**
```python
# In computer_tool.py
# Click center of element instead of top-left
click_x = element.x + element.width // 2
click_y = element.y + element.height // 2
```

---

## GPU/Hardware Issues

### Issue: CUDA out of memory

**Symptoms:**
```
CUDA out of memory. Tried to allocate ... GiB
```

**Solutions:**

1. **Use CPU only:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

2. **Reduce batch size:**
```python
# Process one image at a time instead of batch
```

3. **Clear CUDA cache:**
```bash
# In code
import torch
torch.cuda.empty_cache()

# Environment
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb=1024
```

4. **Use smaller models:**
```python
# Use nano YOLO instead of small
model = YOLO("yolov8n.pt")
```

5. **Check available VRAM:**
```bash
nvidia-smi  # Shows VRAM usage
```

---

### Issue: CUDA version mismatch

**Symptoms:**
```
RuntimeError: CUDA runtime error: no kernel image is available for execution
```

**Solutions:**

1. **Check system CUDA version:**
```bash
nvidia-smi
# Look for CUDA Version
```

2. **Check PyTorch CUDA version:**
```bash
pip list | grep torch
python -c "import torch; print(torch.version.cuda)"
```

3. **Reinstall PyTorch with correct CUDA:**

Get correct command from [pytorch.org](https://pytorch.org):

```bash
# Example for CUDA 12.1
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

### Issue: GPU not being used

**Symptoms:**
```
GPU utilization shows 0%
CPU at 100%
```

**Solutions:**

1. **Check GPU availability:**
```bash
python -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA device: {torch.cuda.get_device_name(0)}')
print(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f}GB')
"
```

2. **Force GPU usage:**
```python
import torch
torch.cuda.is_available = lambda: True
```

3. **Check PyTorch installation:**
```bash
pip install torch torchvision --upgrade
```

---

## FAQ

### Q: Can I run autoMate on a Mac?

**A:** Yes! autoMate works on macOS:
- Intel Macs: Use CPU or NVIDIA GPU
- Apple Silicon (M1/M2/M3): PyTorch will use Metal Performance Shaders automatically
- M-series Macs are actually quite fast!

---

### Q: Is my data private?

**A:** Yes! autoMate is designed for privacy:
- All processing happens locally
- Screenshots are not uploaded (unless you explicitly use an API)
- Only task descriptions and results sent to LLM API
- No tracking or telemetry

---

### Q: Can I use free APIs?

**A:** Partially:
- **Anthropic (Claude):** Free trial available
- **OpenAI:** Free trial available (limited credits)
- **Yeka (2233.ai):** May have free tier
- Most require paid API keys after trial

---

### Q: How much does it cost to run?

**A:** Depends on usage:
- **Vision analysis:** ~$0.01 per screenshot
- **Task planning:** ~$0.05 per task
- **Task execution:** ~$0.01-0.10 per action

Example: 100 actions per task × 5 tasks/day = ~$5-10/month

---

### Q: Why is Florence-2 so slow?

**A:** Florence-2 is a large model:
- ~850M parameters
- Requires GPU for decent speed
- Takes 2-3 seconds per image on GPU
- Takes 30+ seconds per image on CPU

**Solutions:**
- Use GPU (10x faster)
- Disable Florence captions if not needed
- Use smaller regions for captioning

---

### Q: Can I use local LLMs?

**A:** Partially:
- Current code uses Anthropic/OpenAI API
- Could modify to support Ollama/LLaMA
- Would need significant code changes
- Consider feature request on GitHub

---

### Q: How do I get better detection?

**A:** Try these:
1. Ensure good screen visibility
2. Use high resolution (1080p+)
3. Reduce screen scaling
4. Use larger YOLO model (yolov8s)
5. Adjust confidence threshold lower

---

### Q: Can autoMate handle multiple monitors?

**A:** Currently:
- Works with main display
- Can capture specific regions
- Multiple monitor support coming in future

**Workaround:**
- Use screen region selection
- Focus on specific monitor area

---

### Q: What if the task is too complex?

**A:** Break it down:
- Complex tasks take more actions
- More actions = higher cost
- Split into smaller subtasks
- Provide detailed instructions

Example:
```
# Don't use this (too complex)
"Automate my entire workflow"

# Use this (specific, manageable)
"Open email, read first unread message, reply 'Thanks'"
```

---

## Getting More Help

- **GitHub Issues:** [Report bugs](https://github.com/yuruotong1/autoMate/issues)
- **Documentation:** Check [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Discord/Community:** Join community discussions
- **Email Support:** Contact maintainers

---

## Debugging Tips

### Enable Verbose Logging
```bash
export LOGLEVEL=DEBUG
python main.py 2>&1 | tee debug.log
```

### Capture Screenshots for Analysis
```python
from PIL import Image
import pyautogui

# Take screenshot
screenshot = pyautogui.screenshot()
screenshot.save('current_state.png')

# Analyze
from gradio_ui.agent.vision_agent import VisionAgent
agent = VisionAgent(config, api_key)
result = await agent.analyze(screenshot_path='current_state.png')
print(result['elements'])
```

### Test API Connectivity
```bash
# Test OpenAI
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Test Anthropic
curl -X GET https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

---

Still stuck? Open an issue on GitHub with:
1. Python version
2. OS and version
3. Steps to reproduce
4. Full error message
5. Screenshot of the issue
