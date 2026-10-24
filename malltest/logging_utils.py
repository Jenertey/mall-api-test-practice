from __future__ import annotations

import json
from typing import Any


MASK = "<redacted>"
SENSITIVE_KEYS = frozenset(
    {
        "access_token",
        "accesstoken",
        "api_key",
        "apikey",
        "authorization",
        "cookie",
        "password",
        "refresh_token",
        "refreshtoken",
        "secret",
        "set-cookie",
        "set_cookie",
        "token",
    }
)


def redact_sensitive(value: Any) -> Any:
    """Return a copy with credential-like values replaced recursively."""
    if isinstance(value, dict):
        return {
            key: MASK if str(key).strip().lower() in SENSITIVE_KEYS else redact_sensitive(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact_sensitive(item) for item in value]
    return value


def log_snapshot(value: Any, limit: int = 600) -> str:
    """Build a bounded, redacted representation suitable for debug logs."""
    safe_value = redact_sensitive(value)
    if isinstance(safe_value, (dict, list)):
        text = json.dumps(safe_value, ensure_ascii=False, sort_keys=True)
    else:
        text = str(safe_value)
    if len(text) <= limit:
        return text
    return f"{text[:limit]}...<truncated>"
