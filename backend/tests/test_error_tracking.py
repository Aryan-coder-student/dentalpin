"""Error tracking helper: DSN-gated, never raises, PII-free."""

from __future__ import annotations

import sys

from app.core.log_context import setup_error_tracking


def test_no_dsn_is_noop() -> None:
    assert setup_error_tracking(dsn="") is False
    assert setup_error_tracking() is False


def test_missing_sdk_is_noop(monkeypatch) -> None:
    """Without sentry_sdk installed, a configured DSN logs and stays off."""
    monkeypatch.setitem(sys.modules, "sentry_sdk", None)
    assert setup_error_tracking(dsn="https://key@sentry.io/1") is False
