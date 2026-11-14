"""Homework 2 authentication tests.

Offline only: no Langfuse, Docker, or model provider key. Tracing is checked
by inspecting spans in Langfuse (Part E), not here.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException


def test_create_session_rejects_role_mismatch(world: dict) -> None:
    """Claiming a role that differs from the database role must return HTTP 403."""
    from server import app as server_app

    server_app._SESSIONS.clear()
    with pytest.raises(HTTPException) as exc_info:
        server_app.create_session(
            server_app.SessionCreate(user_id=1, role="merchant")
        )
    assert exc_info.value.status_code == 403


def test_token_cannot_authorize_different_session(world: dict) -> None:
    """A token issued for one session must not authorize a different session."""
    from server import app as server_app

    server_app._SESSIONS.clear()
    first = server_app.create_session(
        server_app.SessionCreate(user_id=1, role="shopper")
    )
    second = server_app.create_session(
        server_app.SessionCreate(user_id=2, role="shopper")
    )
    with pytest.raises(HTTPException) as exc_info:
        server_app._authorize(
            second["session_id"],
            f"Bearer {first['token']}",
        )
    assert exc_info.value.status_code == 403
