"""
Cloud vision module for autoMate — screen parsing and action reasoning
via HuggingFace Inference Endpoints.

Configure with environment variables (see .env.example):
  AUTOMATE_HF_TOKEN               — HuggingFace API token
  AUTOMATE_SCREEN_PARSER_URL      — OmniParser-compatible endpoint URL
  AUTOMATE_ACTION_MODEL_URL       — OpenAI-compatible vision-language model endpoint URL
  AUTOMATE_ACTION_MODEL_NAME      — Model name for the action model (e.g. repo id)
  AUTOMATE_HF_NAMESPACE           — HuggingFace namespace for endpoint management API
  AUTOMATE_SCREEN_PARSER_ENDPOINT — Endpoint name for status checks (e.g. "omniparser-v2")
  AUTOMATE_ACTION_MODEL_ENDPOINT  — Endpoint name for status checks (e.g. "ui-tars-1-5-7b")

All inference runs in the cloud — zero local GPU required.
Endpoints that support scale-to-zero need a warmup step before use.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
from io import BytesIO
from pathlib import Path
from typing import Any

import pyautogui
from PIL import Image

LOGS_DIR = Path.home() / ".automate" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("automate.cloud_vision")

def _setup_logging():
    if logger.handlers:
        return
    log_file = LOGS_DIR / "cloud_vision.log"
    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.INFO)
    logger.addHandler(stderr_handler)
    logger.info("=== Cloud vision logging initialized ===")
    logger.info("Log file: %s", log_file)

# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------

def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _get_hf_token() -> str:
    return _env("AUTOMATE_HF_TOKEN", _env("HF_TOKEN"))


def _get_screen_parser_url() -> str:
    return _env("AUTOMATE_SCREEN_PARSER_URL")


def _get_action_model_url() -> str:
    return _env("AUTOMATE_ACTION_MODEL_URL")


def _get_action_model_name() -> str:
    return _env("AUTOMATE_ACTION_MODEL_NAME", "default")


def _get_hf_namespace() -> str:
    return _env("AUTOMATE_HF_NAMESPACE")


def _get_hf_api_base() -> str:
    ns = _get_hf_namespace()
    return f"https://api.endpoints.huggingface.cloud/v2/endpoint/{ns}" if ns else ""


def _get_screen_parser_endpoint() -> str:
    return _env("AUTOMATE_SCREEN_PARSER_ENDPOINT")


def _get_action_model_endpoint() -> str:
    return _env("AUTOMATE_ACTION_MODEL_ENDPOINT")


def is_configured() -> bool:
    """Return True if at least the screen parser or action model URL is set."""
    return bool(_get_screen_parser_url() or _get_action_model_url())


def get_config_summary() -> dict[str, Any]:
    """Return a redacted summary of the current configuration."""
    token = _get_hf_token()
    return {
        "hf_token_set": bool(token),
        "hf_token_preview": f"{token[:8]}..." if len(token) > 8 else ("set" if token else "not set"),
        "screen_parser_url": _get_screen_parser_url() or "not configured",
        "action_model_url": _get_action_model_url() or "not configured",
        "action_model_name": _get_action_model_name(),
        "hf_namespace": _get_hf_namespace() or "not configured",
        "screen_parser_endpoint": _get_screen_parser_endpoint() or "not configured",
        "action_model_endpoint": _get_action_model_endpoint() or "not configured",
    }


_setup_logging()
logger.info("Config summary: %s", json.dumps(get_config_summary(), indent=2))


# ---------------------------------------------------------------------------
# HTTP helpers — use curl to work around Python DNS resolution issues
# with *.endpoints.huggingface.cloud hostnames on some systems.
# ---------------------------------------------------------------------------

def _curl_post(url: str, payload: dict, timeout: int = 120) -> dict:
    """POST JSON via curl subprocess.

    Uses a temp file for the request body to avoid Windows command-line
    length limits (~32K chars) when payloads contain base64 image data.
    """
    logger.debug("_curl_post: url=%s, timeout=%s", url, timeout)
    token = _get_hf_token()
    headers = ["-H", "Content-Type: application/json"]
    if token:
        headers += ["-H", f"Authorization: Bearer {token}"]

    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(payload, tmp)
        tmp.close()
        logger.debug("_curl_post: payload written to %s (size=%d bytes)", tmp.name, os.path.getsize(tmp.name))

        result = subprocess.run(
            ["curl", "-s", "-X", "POST", url, *headers,
             "-d", f"@{tmp.name}", "--max-time", str(timeout)],
            capture_output=True, text=True, timeout=timeout + 10,
        )
        logger.debug("_curl_post: curl rc=%d, stdout_len=%d, stderr_len=%d", result.returncode, len(result.stdout), len(result.stderr))
    finally:
        if tmp:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

    if result.returncode != 0:
        logger.error("_curl_post FAILED: rc=%d, stderr=%s", result.returncode, result.stderr)
        raise RuntimeError(f"curl POST failed (rc={result.returncode}): {result.stderr}")
    body = result.stdout.strip()
    if not body:
        logger.error("_curl_post: empty response from %s", url)
        raise RuntimeError("Empty response from endpoint (DNS or network issue — retry may help)")
    try:
        resp = json.loads(body)
        logger.debug("_curl_post: response parsed OK, keys=%s", list(resp.keys())[:10])
        return resp
    except json.JSONDecodeError as e:
        logger.error("_curl_post: JSON decode error: %s | body=%s", e, body[:500])
        raise


def _curl_get(url: str, timeout: int = 30) -> dict:
    """GET JSON via curl subprocess."""
    token = _get_hf_token()
    headers = []
    if token:
        headers = ["-H", f"Authorization: Bearer {token}"]

    result = subprocess.run(
        ["curl", "-s", "-X", "GET", url, *headers, "--max-time", str(timeout)],
        capture_output=True, text=True, timeout=timeout + 10,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl GET failed: {result.stderr}")
    body = result.stdout.strip()
    if not body:
        raise RuntimeError("Empty response (DNS or network issue)")
    return json.loads(body)


def _screenshot_b64(region: list[int] | None = None) -> tuple[str, int, int]:
    """Take a screenshot and return (base64_png, width, height)."""
    if region and len(region) == 4:
        img = pyautogui.screenshot(region=(region[0], region[1], region[2], region[3]))
    else:
        img = pyautogui.screenshot()
    w, h = img.size
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode(), w, h


# ---------------------------------------------------------------------------
# Endpoint status & warmup (requires HF namespace + endpoint names)
# ---------------------------------------------------------------------------

def get_endpoint_status(endpoint_name: str) -> dict[str, str]:
    """Check the status of a HuggingFace Inference Endpoint by name."""
    api_base = _get_hf_api_base()
    if not api_base:
        return {"name": endpoint_name, "state": "unknown", "message": "HF namespace not configured"}

    data = _curl_get(f"{api_base}/{endpoint_name}")
    status = data.get("status", {})
    return {
        "name": endpoint_name,
        "state": status.get("state", "unknown"),
        "message": status.get("message", ""),
        "url": status.get("url", ""),
    }


def warm_endpoints(timeout_seconds: int = 600) -> dict[str, Any]:
    """
    Ensure both screen-parser and action-model endpoints are running.

    If scaled to zero, sends a wake-up request and polls until ready.
    Requires AUTOMATE_HF_NAMESPACE and endpoint name env vars to be set.

    Returns status dict for each configured endpoint.
    """
    logger.info("warm_endpoints: START (timeout=%s seconds)", timeout_seconds)
    if not _get_hf_api_base():
        logger.error("warm_endpoints: AUTOMATE_HF_NAMESPACE not set")
        return {"error": "AUTOMATE_HF_NAMESPACE not set — cannot manage endpoints"}

    targets: list[tuple[str, str, Any]] = []
    sp_ep = _get_screen_parser_endpoint()
    am_ep = _get_action_model_endpoint()
    logger.debug("warm_endpoints: screen_parser_endpoint=%s, action_model_endpoint=%s", sp_ep, am_ep)
    if sp_ep:
        targets.append((sp_ep, _get_screen_parser_url(), _test_screen_parser))
    if am_ep:
        targets.append((am_ep, _get_action_model_url(), _test_action_model))

    if not targets:
        logger.error("warm_endpoints: no endpoint names configured")
        return {"error": "No endpoint names configured (AUTOMATE_SCREEN_PARSER_ENDPOINT / AUTOMATE_ACTION_MODEL_ENDPOINT)"}

    results: dict[str, Any] = {}
    for name, url, test_fn in targets:
        logger.info("warm_endpoints: checking endpoint '%s' at %s", name, url)
        status = get_endpoint_status(name)
        state = status["state"]
        logger.info("warm_endpoints: '%s' initial state=%s message=%s", name, state, status.get("message", ""))
        results[name] = {"initial_state": state}

        if state == "running":
            logger.debug("warm_endpoints: '%s' is running, testing...", name)
            try:
                test_fn()
                logger.info("warm_endpoints: '%s' is READY (test passed)", name)
                results[name]["status"] = "ready"
                results[name]["warmup_needed"] = False
                continue
            except Exception as e:
                logger.warning("warm_endpoints: '%s' running but test failed: %s", name, e)

        if state in ("scaledToZero", "paused"):
            logger.info("warm_endpoints: '%s' needs warmup (state=%s)", name, state)
            results[name]["warmup_needed"] = True
            if state == "paused":
                try:
                    api_base = _get_hf_api_base()
                    logger.debug("warm_endpoints: sending resume request for '%s'", name)
                    _curl_post(f"{api_base}/{name}/resume", {}, timeout=30)
                    logger.info("warm_endpoints: resume request sent for %s", name)
                except Exception as e:
                    logger.warning("warm_endpoints: resume request for %s failed: %s", name, e)
            else:
                logger.debug("warm_endpoints: sending wake-up request to '%s'", name)
                try:
                    test_fn()
                except Exception as e:
                    logger.debug("warm_endpoints: wake-up request exception (expected): %s", e)

        start = time.time()
        logger.info("warm_endpoints: polling '%s' until ready...", name)
        while time.time() - start < timeout_seconds:
            elapsed = round(time.time() - start, 1)
            try:
                s = get_endpoint_status(name)
                logger.debug("warm_endpoints: '%s' poll at %ss: state=%s", name, elapsed, s["state"])
                if s["state"] == "running":
                    try:
                        test_fn()
                        results[name]["status"] = "ready"
                        results[name]["warmup_seconds"] = elapsed
                        logger.info("warm_endpoints: '%s' READY after %s seconds", name, elapsed)
                        break
                    except Exception as e:
                        logger.debug("warm_endpoints: '%s' running but test failed at %ss: %s", name, elapsed, e)
                        time.sleep(5)
                        continue
                elif s["state"] == "failed":
                    results[name]["status"] = "failed"
                    results[name]["error"] = s.get("message", "endpoint failed")
                    logger.error("warm_endpoints: '%s' FAILED: %s", name, s.get("message", ""))
                    break
                else:
                    logger.debug("warm_endpoints: '%s' not ready yet (state=%s), waiting...", name, s["state"])
                    time.sleep(10)
            except Exception as e:
                logger.warning("warm_endpoints: poll exception at %ss: %s", elapsed, e)
                time.sleep(10)
        else:
            logger.error("warm_endpoints: '%s' TIMEOUT after %s seconds", name, timeout_seconds)
            results[name]["status"] = "timeout"

    logger.info("warm_endpoints: COMPLETE, results=%s", json.dumps(results, indent=2))
    return results


def _test_screen_parser() -> None:
    """Quick health-check for the screen parser endpoint."""
    logger.debug("_test_screen_parser: START")
    url = _get_screen_parser_url()
    if not url:
        logger.error("_test_screen_parser: AUTOMATE_SCREEN_PARSER_URL not set")
        raise RuntimeError("AUTOMATE_SCREEN_PARSER_URL not set")
    img = Image.new("RGB", (10, 10), color="red")
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    logger.debug("_test_screen_parser: sending test request to %s", url)
    resp = _curl_post(url, {
        "inputs": {
            "image": f"data:image/png;base64,{b64}",
            "image_size": {"w": 10, "h": 10},
        }
    }, timeout=30)
    if "error" in resp:
        err_msg = resp["error"]
        logger.error("_test_screen_parser: endpoint returned error: %s", err_msg)
        if "not enough values to unpack" in str(err_msg):
            logger.info("_test_screen_parser: endpoint is responsive (YOLO found no detections in minimal test image, which is expected)")
            return
        raise RuntimeError(err_msg)
    logger.info("_test_screen_parser: SUCCESS, response keys=%s", list(resp.keys()))


def _test_action_model() -> None:
    """Quick health-check for the action model endpoint."""
    logger.debug("_test_action_model: START")
    url = _get_action_model_url()
    if not url:
        logger.error("_test_action_model: AUTOMATE_ACTION_MODEL_URL not set")
        raise RuntimeError("AUTOMATE_ACTION_MODEL_URL not set")
    logger.debug("_test_action_model: sending test request to %s/v1/chat/completions", url)
    resp = _curl_post(f"{url}/v1/chat/completions", {
        "model": _get_action_model_name(),
        "messages": [{"role": "user", "content": "Say OK"}],
        "max_tokens": 5,
    }, timeout=30)
    if "error" in resp:
        logger.error("_test_action_model: endpoint returned error: %s", resp["error"])
        raise RuntimeError(str(resp["error"]))
    logger.info("_test_action_model: SUCCESS, response keys=%s", list(resp.keys()))


# ---------------------------------------------------------------------------
# Screen parsing (OmniParser-compatible endpoint)
# ---------------------------------------------------------------------------

def parse_screen(
    region: list[int] | None = None,
    bbox_threshold: float = 0.05,
    iou_threshold: float = 0.7,
) -> dict[str, Any]:
    """
    Capture a screenshot and send to the screen parser endpoint for
    UI element detection (bounding boxes, OCR text, icon captions).

    The endpoint must be OmniParser-v2 compatible:
      - Input:  {"inputs": {"image": "data:...", "image_size": {"w": int, "h": int}}}
      - Output: {"image": "<base64>", "bboxes": [...]}

    Returns dict with 'elements', 'annotated_image', and 'screen_size'.
    """
    logger.info("parse_screen: START region=%s bbox_threshold=%s iou_threshold=%s", region, bbox_threshold, iou_threshold)
    url = _get_screen_parser_url()
    if not url:
        logger.error("parse_screen: AUTOMATE_SCREEN_PARSER_URL not set")
        raise RuntimeError(
            "Screen parser not configured. Set AUTOMATE_SCREEN_PARSER_URL to an "
            "OmniParser-compatible HuggingFace Inference Endpoint URL."
        )

    logger.debug("parse_screen: capturing screenshot...")
    b64, w, h = _screenshot_b64(region)
    logger.debug("parse_screen: screenshot size %dx%d, base64_len=%d", w, h, len(b64))

    logger.debug("parse_screen: sending to endpoint %s", url)
    resp = _curl_post(url, {
        "inputs": {
            "image": f"data:image/png;base64,{b64}",
            "image_size": {"w": w, "h": h},
            "bbox_threshold": bbox_threshold,
            "iou_threshold": iou_threshold,
        }
    })

    if "error" in resp:
        logger.error("parse_screen: endpoint error: %s", resp["error"])
        raise RuntimeError(f"Screen parser error: {resp['error']}")

    bbox_count = len(resp.get("bboxes", []))
    logger.info("parse_screen: SUCCESS, received %d bboxes", bbox_count)

    elements = []
    for i, bbox_info in enumerate(resp.get("bboxes", [])):
        norm = bbox_info["bbox"]
        px = [int(norm[0] * w), int(norm[1] * h), int(norm[2] * w), int(norm[3] * h)]
        el = {
            "id": i,
            "type": bbox_info.get("type", "unknown"),
            "content": bbox_info.get("content"),
            "interactivity": bbox_info.get("interactivity", False),
            "bbox_normalized": [round(v, 4) for v in norm],
            "bbox_px": px,
            "center": [(px[0] + px[2]) // 2, (px[1] + px[3]) // 2],
            "source": bbox_info.get("source", ""),
        }
        elements.append(el)
        if i < 5:
            logger.debug("parse_screen: element[%d] type=%s content='%s' center=%s", i, el["type"], el.get("content", ""), el["center"])

    annotated = resp.get("image", "")
    result = {
        "elements": elements,
        "element_count": len(elements),
        "annotated_image": f"data:image/png;base64,{annotated}" if annotated else "",
        "screen_size": {"w": w, "h": h},
    }
    logger.info("parse_screen: COMPLETE, %d elements, annotated_image_len=%d", len(elements), len(annotated))
    return result


# ---------------------------------------------------------------------------
# Action reasoning (OpenAI-compatible vision-language model endpoint)
# ---------------------------------------------------------------------------

def reason_action(
    task: str,
    elements: list[dict[str, Any]] | None = None,
    region: list[int] | None = None,
    max_tokens: int = 512,
) -> dict[str, Any]:
    """
    Send the current screenshot + task to the action model for reasoning.

    The endpoint must serve an OpenAI-compatible /v1/chat/completions API
    with vision support (e.g. vLLM serving UI-TARS, Qwen-VL, etc.).

    Args:
        task: Natural language description of what to accomplish.
        elements: Optional parsed elements from parse_screen() for richer context.
        region: Optional [x, y, w, h] to capture a sub-region.
        max_tokens: Maximum tokens for the response.

    Returns dict with 'reasoning', 'model', and 'usage'.
    """
    logger.info("reason_action: START task='%s' elements=%d region=%s max_tokens=%d", task[:50], len(elements) if elements else 0, region, max_tokens)
    url = _get_action_model_url()
    if not url:
        logger.error("reason_action: AUTOMATE_ACTION_MODEL_URL not set")
        raise RuntimeError(
            "Action model not configured. Set AUTOMATE_ACTION_MODEL_URL to an "
            "OpenAI-compatible vision-language model endpoint URL."
        )

    logger.debug("reason_action: capturing screenshot...")
    b64, w, h = _screenshot_b64(region)
    logger.debug("reason_action: screenshot size %dx%d, base64_len=%d", w, h, len(b64))

    prompt_parts = [f"Screen resolution: {w}x{h}\n"]
    if elements:
        logger.debug("reason_action: including %d parsed elements in prompt", len(elements))
        prompt_parts.append("Detected UI elements:\n")
        for el in elements:
            prompt_parts.append(
                f"  [{el['id']}] {el['type']}: \"{el.get('content', '?')}\" "
                f"at center ({el['center'][0]}, {el['center'][1]}) "
                f"bbox {el['bbox_px']}"
                f"{' [interactive]' if el.get('interactivity') else ''}\n"
            )
        prompt_parts.append("\n")

    prompt_parts.append(f"Task: {task}\n\n")
    prompt_parts.append(
        "Based on the screenshot and detected elements, what action should be taken? "
        "Provide exact pixel coordinates for any click actions.\n"
        "Format your response as:\n"
        "Thought: <your reasoning>\n"
        "Action: <action_type>(parameters)\n"
        "Supported actions: click(x, y), type(\"text\"), press(\"key\"), "
        "scroll(direction, amount), done()"
    )

    prompt_text = "".join(prompt_parts)
    logger.debug("reason_action: prompt length=%d chars", len(prompt_text))

    logger.debug("reason_action: sending to %s/v1/chat/completions", url)
    resp = _curl_post(f"{url}/v1/chat/completions", {
        "model": _get_action_model_name(),
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": prompt_text},
            ],
        }],
        "max_tokens": max_tokens,
    })

    if "error" in resp:
        logger.error("reason_action: endpoint error: %s", resp["error"])
        raise RuntimeError(f"Action model error: {resp['error']}")

    choice = resp["choices"][0]["message"]
    content = choice["content"]
    logger.info("reason_action: SUCCESS, response length=%d chars", len(content))
    logger.debug("reason_action: reasoning preview: %s", content[:200])
    return {
        "reasoning": content,
        "model": resp.get("model", _get_action_model_name()),
        "usage": resp.get("usage", {}),
    }


# ---------------------------------------------------------------------------
# Combined pipeline: parse + reason + execute
# ---------------------------------------------------------------------------

def _parse_coordinates(params: str) -> tuple[int, int]:
    """Extract x, y coordinates from various formats.
    
    Handles:
      - "x, y" (simple format)
      - "start_box='(x, y)'" (UI-TARS format with quoted tuple)
      - "start_box=(x, y)" (UI-TARS format without quotes)
      - "start_point='(x, y)'" (alternative UI-TARS format)
      - Truncated forms: "start_box='(x, y)", "(x, y", etc.
    """
    params = params.strip()
    
    # UI-TARS format: start_box='(x, y)' or start_box=(x, y) (also handles truncated)
    box_match = re.search(
        r"start_(?:box|point)=['\"]?\(\s*(\d+)\s*,\s*(\d+)\s*",
        params
    )
    if box_match:
        return int(box_match.group(1)), int(box_match.group(2))
    
    # Parenthesized format: (x, y) or (x, y (truncated)
    paren_match = re.search(r"\(\s*(\d+)\s*,\s*(\d+)\s*", params)
    if paren_match:
        return int(paren_match.group(1)), int(paren_match.group(2))
    
    # Simple format: x, y
    coords = [int(x.strip()) for x in params.split(",")]
    if len(coords) >= 2:
        return coords[0], coords[1]
    
    raise ValueError(f"Cannot parse coordinates from: {params}")


def _execute_action(action_type: str, params: str) -> str:
    """Execute a parsed action string. Returns description of what was done."""
    import platform
    import pyperclip

    if action_type == "click":
        x, y = _parse_coordinates(params)
        pyautogui.click(x, y)
        return f"click({x}, {y})"

    if action_type == "type":
        text = params.strip("\"'")
        old = pyperclip.paste()
        pyperclip.copy(text)
        pyautogui.hotkey("command" if platform.system() == "Darwin" else "ctrl", "v")
        time.sleep(0.05)
        pyperclip.copy(old)
        preview = f"{text[:30]}..." if len(text) > 30 else text
        return f'type("{preview}")'

    if action_type == "press":
        key = params.strip("\"'")
        parts = [k.strip() for k in key.split("+")]
        if len(parts) == 1:
            pyautogui.press(parts[0])
        else:
            pyautogui.hotkey(*parts)
        return f'press("{key}")'

    if action_type == "scroll":
        scroll_params = [x.strip().strip("\"'") for x in params.split(",")]
        direction = scroll_params[0] if scroll_params else "down"
        amount = int(scroll_params[1]) if len(scroll_params) > 1 else 3
        pyautogui.scroll(amount if direction == "up" else -amount)
        return f"scroll({direction}, {amount})"

    raise ValueError(f"Unknown action: {action_type}")


def smart_act(
    task: str,
    max_steps: int = 10,
    step_delay: float = 1.0,
) -> list[dict[str, Any]]:
    """
    Full automation loop: screenshot -> parse screen -> reason action -> execute.

    Repeats until the action model outputs done() or max_steps is reached.

    Args:
        task: What to accomplish (natural language).
        max_steps: Safety limit on iterations.
        step_delay: Seconds to wait between steps for UI to settle.

    Returns list of step result dicts.
    """
    logger.info("smart_act: START task='%s' max_steps=%d step_delay=%.1f", task[:50], max_steps, step_delay)
    steps: list[dict[str, Any]] = []

    for step_num in range(1, max_steps + 1):
        logger.info("smart_act: === Step %d/%d ===", step_num, max_steps)
        
        try:
            parsed = parse_screen()
            elements = parsed["elements"]
            logger.debug("smart_act: step %d found %d elements", step_num, len(elements))
        except Exception as e:
            logger.error("smart_act: step %d parse_screen FAILED: %s", step_num, e)
            steps.append({"step": step_num, "error": str(e), "action_taken": "parse_failed"})
            break

        try:
            result = reason_action(task, elements=elements)
            reasoning = result["reasoning"]
            logger.debug("smart_act: step %d reasoning: %s", step_num, reasoning[:200])
        except Exception as e:
            logger.error("smart_act: step %d reason_action FAILED: %s", step_num, e)
            steps.append({"step": step_num, "elements_found": len(elements), "error": str(e), "action_taken": "reason_failed"})
            break

        step_result: dict[str, Any] = {
            "step": step_num,
            "elements_found": len(elements),
            "reasoning": reasoning,
            "action_taken": None,
        }

        action_match = re.search(
            r"Action:\s*(click|type|press|scroll|done)\s*\(",
            reasoning, re.IGNORECASE,
        )

        if not action_match:
            logger.warning("smart_act: step %d no action parsed from reasoning", step_num)
            step_result["action_taken"] = "no_action_parsed"
            steps.append(step_result)
            continue

        action_type = action_match.group(1).lower()

        # Extract params using paren counting (handles UI-TARS nested parens and truncated output)
        # We're inside the action paren already, so start at depth=1
        rest = reasoning[action_match.end():].strip()
        params = ""
        depth = 1
        for i, c in enumerate(rest):
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    params = rest[:i]
                    break
        
        # Fallback for truncated output (no matching closing paren found)
        if not params:
            params = rest
        
        params = params.strip()
        logger.info("smart_act: step %d parsed action: %s(%s)", step_num, action_type, params)

        if action_type == "done":
            logger.info("smart_act: step %d DONE signal received", step_num)
            step_result["action_taken"] = "done"
            steps.append(step_result)
            break

        try:
            logger.debug("smart_act: step %d executing %s(%s)", step_num, action_type, params)
            step_result["action_taken"] = _execute_action(action_type, params)
            logger.info("smart_act: step %d executed: %s", step_num, step_result["action_taken"])
        except Exception as e:
            logger.error("smart_act: step %d execution FAILED: %s", step_num, e)
            step_result["action_taken"] = f"error: {e}"

        steps.append(step_result)
        logger.debug("smart_act: step %d complete, sleeping %.1f seconds", step_num, step_delay)
        time.sleep(step_delay)

    logger.info("smart_act: COMPLETE after %d steps", len(steps))
    return steps
