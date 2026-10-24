from __future__ import annotations

import pytest

from malltest.logging_utils import MASK, log_snapshot, redact_sensitive


pytestmark = pytest.mark.unit


def test_nested_credentials_are_redacted_without_mutating_input() -> None:
    payload = {
        "username": "admin",
        "password": "macro123",
        "data": {
            "token": "header.payload.signature",
            "profile": {"Authorization": "Bearer secret", "displayName": "tester"},
        },
        "items": [{"cookie": "SESSION=abc", "id": 1}],
    }

    safe = redact_sensitive(payload)

    assert safe["password"] == MASK
    assert safe["data"]["token"] == MASK
    assert safe["data"]["profile"]["Authorization"] == MASK
    assert safe["items"][0]["cookie"] == MASK
    assert safe["username"] == "admin"
    assert safe["data"]["profile"]["displayName"] == "tester"
    assert payload["password"] == "macro123"


def test_log_snapshot_is_bounded_and_redacted() -> None:
    snapshot = log_snapshot(
        {"authorization": "Bearer secret-token", "description": "x" * 800},
        limit=80,
    )

    assert "secret-token" not in snapshot
    assert MASK in snapshot
    assert snapshot.endswith("...<truncated>")
    assert len(snapshot) < 120
