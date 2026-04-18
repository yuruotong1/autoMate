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
import tempfile
import time
from io import BytesIO
from typing import Any

import pyautogui
from PIL import Image

logger = logging.getLogger("automate.cloud_vision")

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


# ---------------------------------------------------------------------------
# HTTP helpers — use curl to work around Python DNS resolution issues
# with *.endpoints.huggingface.cloud hostnames on some systems.
# ---------------------------------------------------------------------------

def _curl_post(url: str, payload: dict, timeout: int = 120) -> dict:
    """POST JSON via curl subprocess.

    Uses a temp file for the request body to avoid Windows command-line
    length limits (~32K chars) when payloads contain base64 image data.
    """
    token = _get_hf_token()
    headers = ["-H", "Content-Type: application/json"]
    if token:
        headers += ["-H", f"Authorization: Bearer {token}"]

    # Write payload to temp file to avoid [WinError 206] on large payloads
    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(payload, tmp)
        tmp.close()

        result = subprocess.run(
            ["curl", "-s", "-X", "POST", url, *headers,
             "-d", f"@{tmp.name}", "--max-time", str(timeout)],
            capture_output=True, text=True, timeout=timeout + 10,
        )
    finally:
        if tmp:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

    if result.returncode != 0:
        raise RuntimeError(f"curl POST failed (rc={result.returncode}): {result.stderr}")
    body = result.stdout.strip()
    if not body:
        raise RuntimeError("Empty response from endpoint (DNS or network issue — retry may help)")
    return json.loads(body)


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
        img = pyautogui.screenshot(region=tuple(region))
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
    if not _get_hf_api_base():
        return {"error": "AUTOMATE_HF_NAMESPACE not set — cannot manage endpoints"}

    targets: list[tuple[str, str, Any]] = []
    sp_ep = _get_screen_parser_endpoint()
    am_ep = _get_action_model_endpoint()
    if sp_ep:
        targets.append((sp_ep, _get_screen_parser_url(), _test_screen_parser))
    if am_ep:
        targets.append((am_ep, _get_action_model_url(), _test_action_model))

    if not targets:
        return {"error": "No endpoint names configured (AUTOMATE_SCREEN_PARSER_ENDPOINT / AUTOMATE_ACTION_MODEL_ENDPOINT)"}

    results: dict[str, Any] = {}
    for name, url, test_fn in targets:
        status = get_endpoint_status(name)
        state = status["state"]
        results[name] = {"initial_state": state}

        if state == "running":
            try:
                test_fn()
                results[name]["status"] = "ready"
                results[name]["warmup_needed"] = False
                continue
            except Exception:
                pass

        if state in ("scaledToZero", "paused"):
            results[name]["warmup_needed"] = True
            if state == "paused":
                # Paused endpoints must be explicitly resumed via API
                try:
                    api_base = _get_hf_api_base()
                    _curl_post(f"{api_base}/{name}/resume", {}, timeout=30)
                    logger.info("Sent resume request for %s", name)
                except Exception as e:
                    logger.warning("Resume request for %s failed: %s", name, e)
            else:
                # scaledToZero — any request wakes it up
                try:
                    test_fn()
                except Exception:
                    pass

        start = time.time()
        while time.time() - start < timeout_seconds:
            try:
                s = get_endpoint_status(name)
                if s["state"] == "running":
                    try:
                        test_fn()
                        results[name]["status"] = "ready"
                        results[name]["warmup_seconds"] = round(time.time() - start, 1)
                        break
                    except Exception:
                        time.sleep(5)
                        continue
                elif s["state"] == "failed":
                    results[name]["status"] = "failed"
                    results[name]["error"] = s.get("message", "endpoint failed")
                    break
                else:
                    time.sleep(10)
            except Exception:
                time.sleep(10)
        else:
            results[name]["status"] = "timeout"

    return results


def _test_screen_parser() -> None:
    """Quick health-check for the screen parser endpoint."""
    url = _get_screen_parser_url()
    if not url:
        raise RuntimeError("AUTOMATE_SCREEN_PARSER_URL not set")
    img = Image.new("RGB", (10, 10), color="red")
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    resp = _curl_post(url, {
        "inputs": {
            "image": f"data:image/png;base64,{b64}",
            "image_size": {"w": 10, "h": 10},
        }
    }, timeout=30)
    if "error" in resp:
        raise RuntimeError(resp["error"])


def _test_action_model() -> None:
    """Quick health-check for the action model endpoint."""
    url = _get_action_model_url()
    if not url:
        raise RuntimeError("AUTOMATE_ACTION_MODEL_URL not set")
    resp = _curl_post(f"{url}/v1/chat/completions", {
        "model": _get_action_model_name(),
        "messages": [{"role": "user", "content": "Say OK"}],
        "max_tokens": 5,
    }, timeout=30)
    if "error" in resp:
        raise RuntimeError(str(resp["error"]))


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
    url = _get_screen_parser_url()
    if not url:
        raise RuntimeError(
            "Screen parser not configured. Set AUTOMATE_SCREEN_PARSER_URL to an "
            "OmniParser-compatible HuggingFace Inference Endpoint URL."
        )

    b64, w, h = _screenshot_b64(region)

    resp = _curl_post(url, {
        "inputs": {
            "image": f"data:image/png;base64,{b64}",
            "image_size": {"w": w, "h": h},
            "bbox_threshold": bbox_threshold,
            "iou_threshold": iou_threshold,
        }
    })

    if "error" in resp:
        raise RuntimeError(f"Screen parser error: {resp['error']}")

    elements = []
    for i, bbox_info in enumerate(resp.get("bboxes", [])):
        norm = bbox_info["bbox"]
        px = [int(norm[0] * w), int(norm[1] * h), int(norm[2] * w), int(norm[3] * h)]
        elements.append({
            "id": i,
            "type": bbox_info.get("type", "unknown"),
            "content": bbox_info.get("content"),
            "interactivity": bbox_info.get("interactivity", False),
            "bbox_normalized": [round(v, 4) for v in norm],
            "bbox_px": px,
            "center": [(px[0] + px[2]) // 2, (px[1] + px[3]) // 2],
            "source": bbox_info.get("source", ""),
        })

    annotated = resp.get("image", "")
    return {
        "elements": elements,
        "element_count": len(elements),
        "annotated_image": f"data:image/png;base64,{annotated}" if annotated else "",
        "screen_size": {"w": w, "h": h},
    }


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
    url = _get_action_model_url()
    if not url:
        raise RuntimeError(
            "Action model not configured. Set AUTOMATE_ACTION_MODEL_URL to an "
            "OpenAI-compatible vision-language model endpoint URL."
        )

    b64, w, h = _screenshot_b64(region)

    prompt_parts = [f"Screen resolution: {w}x{h}\n"]
    if elements:
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

    resp = _curl_post(f"{url}/v1/chat/completions", {
        "model": _get_action_model_name(),
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": "".join(prompt_parts)},
            ],
        }],
        "max_tokens": max_tokens,
    })

    if "error" in resp:
        raise RuntimeError(f"Action model error: {resp['error']}")

    choice = resp["choices"][0]["message"]
    return {
        "reasoning": choice["content"],
        "model": resp.get("model", _get_action_model_name()),
        "usage": resp.get("usage", {}),
    }


# ---------------------------------------------------------------------------
# Combined pipeline: parse + reason + execute
# ---------------------------------------------------------------------------

def _execute_action(action_type: str, params: str) -> str:
    """Execute a parsed action string. Returns description of what was done."""
    import platform
    import pyperclip

    if action_type == "click":
        coords = [int(x.strip()) for x in params.split(",")]
        if len(coords) >= 2:
            pyautogui.click(coords[0], coords[1])
            return f"click({coords[0]}, {coords[1]})"
        raise ValueError(f"click needs x,y coordinates, got: {params}")

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
    steps: list[dict[str, Any]] = []

    for step_num in range(1, max_steps + 1):
        # 1. Parse screen
        parsed = parse_screen()
        elements = parsed["elements"]

        # 2. Reason about next action
        result = reason_action(task, elements=elements)
        reasoning = result["reasoning"]

        step_result: dict[str, Any] = {
            "step": step_num,
            "elements_found": len(elements),
            "reasoning": reasoning,
            "action_taken": None,
        }

        # 3. Extract action from model output
        action_match = re.search(
            r"Action:\s*(click|type|press|scroll|done)\(([^)]*)\)",
            reasoning, re.IGNORECASE,
        )

        if not action_match:
            step_result["action_taken"] = "no_action_parsed"
            steps.append(step_result)
            continue

        action_type = action_match.group(1).lower()
        params = action_match.group(2).strip()

        if action_type == "done":
            step_result["action_taken"] = "done"
            steps.append(step_result)
            break

        # 4. Execute
        try:
            step_result["action_taken"] = _execute_action(action_type, params)
        except Exception as e:
            step_result["action_taken"] = f"error: {e}"

        steps.append(step_result)
        time.sleep(step_delay)

    return steps
