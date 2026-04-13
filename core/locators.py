"""
Locator helpers — find (x, y) on screen using various strategies.

Exported functions
------------------
resolve_ocr(text, confidence)   — find element by visible text (OmniParser)
resolve_image(template, conf)   — find element by template image (OpenCV)
resolve_coord(x, y)             — return stored absolute coordinates directly
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

log = logging.getLogger(__name__)

_SNAPSHOTS_DIR = Path.home() / ".automate" / "snapshots"


# ---------------------------------------------------------------------------
# OCR / OmniParser
# ---------------------------------------------------------------------------

def resolve_ocr(text: str, confidence: float = 0.70) -> Optional[Tuple[int, int]]:
    """
    Use OmniParser (YOLO-based UI detector) to find an element whose
    visible label contains *text* (case-insensitive, partial match).
    Returns (x, y) centre of the best match, or None.
    """
    try:
        import numpy as np
        import pyautogui
        from auto_control.icon_detection import get_parsed_content_icon_scaled

        screenshot = pyautogui.screenshot()
        img_np     = np.array(screenshot)
        parsed     = get_parsed_content_icon_scaled(
            img_np, 0, 0, img_np.shape[1], img_np.shape[0]
        )

        target = text.lower()
        best: Optional[Tuple[int, int, float]] = None

        for item in parsed:
            label = str(item.get("content", "") or item.get("label", "")).lower()
            if target in label:
                bbox = item.get("bbox", [])
                if len(bbox) == 4:
                    cx   = int((bbox[0] + bbox[2]) / 2)
                    cy   = int((bbox[1] + bbox[3]) / 2)
                    conf = float(item.get("confidence", 1.0))
                    if conf >= confidence and (best is None or conf > best[2]):
                        best = (cx, cy, conf)

        if best:
            log.debug("OCR found '%s' at (%d, %d) conf=%.2f", text, best[0], best[1], best[2])
            return (best[0], best[1])

    except Exception as exc:
        log.debug("resolve_ocr error: %s", exc)

    return None


# ---------------------------------------------------------------------------
# Image template (OpenCV)
# ---------------------------------------------------------------------------

def resolve_image(template_name: str, confidence: float = 0.85) -> Optional[Tuple[int, int]]:
    """
    Match a saved template PNG against the current screenshot.
    *template_name* is a filename under ~/.automate/snapshots/.
    Returns (x, y) centre of the best match, or None.
    """
    try:
        import cv2
        import numpy as np
        import pyautogui

        template_path = _SNAPSHOTS_DIR / template_name
        if not template_path.exists():
            log.debug("Template not found: %s", template_path)
            return None

        template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)
        if template is None:
            return None

        screenshot = pyautogui.screenshot()
        screen_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result            = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            th, tw = template.shape[:2]
            cx = max_loc[0] + tw // 2
            cy = max_loc[1] + th // 2
            log.debug("Image match '%s' at (%d, %d) score=%.2f", template_name, cx, cy, max_val)
            return (cx, cy)

    except Exception as exc:
        log.debug("resolve_image error: %s", exc)

    return None


# ---------------------------------------------------------------------------
# Absolute coordinate (trivial)
# ---------------------------------------------------------------------------

def resolve_coord(x: int, y: int) -> Tuple[int, int]:
    return (x, y)


# ---------------------------------------------------------------------------
# Nearby text helper (used by Learner)
# ---------------------------------------------------------------------------

def nearby_ocr_text(x: int, y: int, radius: int = 60) -> Optional[str]:
    """Return the label of the closest parsed UI element to (x, y)."""
    try:
        import numpy as np
        import pyautogui
        from auto_control.icon_detection import get_parsed_content_icon_scaled

        screenshot = pyautogui.screenshot()
        img_np     = np.array(screenshot)
        parsed     = get_parsed_content_icon_scaled(
            img_np, 0, 0, img_np.shape[1], img_np.shape[0]
        )

        best_dist = float("inf")
        best_text: Optional[str] = None

        for item in parsed:
            bbox = item.get("bbox", [])
            if len(bbox) < 4:
                continue
            cx   = (bbox[0] + bbox[2]) / 2
            cy   = (bbox[1] + bbox[3]) / 2
            dist = ((cx - x) ** 2 + (cy - y) ** 2) ** 0.5
            if dist < radius and dist < best_dist:
                best_dist = dist
                best_text = str(item.get("content", "") or item.get("label", ""))

        return best_text or None

    except Exception as exc:
        log.debug("nearby_ocr_text error: %s", exc)
        return None
