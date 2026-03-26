# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

import re
import time
import html
from collections import defaultdict

# ── Rate limiting ──────────────────────────────────────────────────────────────
_rate_store = defaultdict(list)
RATE_LIMITS = {
    "ocr":   {"calls": 10, "window": 60},
    "check": {"calls": 20, "window": 60},
}

def check_rate_limit(action: str, key: str = "global") -> tuple[bool, str]:
    """Returns (allowed, message). True = allowed."""
    limit = RATE_LIMITS.get(action, {"calls": 30, "window": 60})
    now = time.time()
    window = limit["window"]
    max_calls = limit["calls"]
    store_key = f"{action}:{key}"
    _rate_store[store_key] = [t for t in _rate_store[store_key] if now - t < window]
    if len(_rate_store[store_key]) >= max_calls:
        wait = int(window - (now - _rate_store[store_key][0]))
        return False, f"Too many requests. Please wait {wait} seconds."
    _rate_store[store_key].append(now)
    return True, ""

# ── Input sanitization ─────────────────────────────────────────────────────────
MAX_INPUT_CHARS = 10_000

def sanitize_text(text: str) -> str:
    """Remove dangerous content, normalize whitespace, limit size."""
    if not text:
        return ""
    # Decode HTML entities
    text = html.unescape(text)
    # Remove script/html tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove null bytes and control characters (keep newlines and tabs)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # Remove potential injection patterns
    text = re.sub(r"(javascript:|data:|vbscript:)", "", text, flags=re.IGNORECASE)
    # Normalize whitespace — collapse multiple spaces/newlines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Limit size
    if len(text) > MAX_INPUT_CHARS:
        text = text[:MAX_INPUT_CHARS]
    return text.strip()

def sanitize_filename(name: str) -> str:
    """Sanitize a filename."""
    return re.sub(r"[^\w\-.]", "_", name)[:100]

def validate_image_file(file) -> tuple[bool, str]:
    """Validate uploaded image file."""
    if file is None:
        return False, "No file provided."
    allowed = {"image/jpeg", "image/png", "image/jpg"}
    if hasattr(file, "type") and file.type not in allowed:
        return False, f"Invalid file type: {file.type}. Only JPG and PNG allowed."
    max_size = 10 * 1024 * 1024  # 10 MB
    if hasattr(file, "size") and file.size > max_size:
        return False, "File too large. Maximum size is 10 MB."
    return True, ""
