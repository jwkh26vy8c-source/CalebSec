from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any

from calebsec.core.config import SECRET_KEY, TOKEN_TTL_SECONDS
from calebsec.core.models import Role


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _unb64(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(payload_b64: str) -> str:
    return hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()


def create_token(username: str, role: Role) -> str:
    payload: dict[str, Any] = {
        "sub": username,
        "role": role.value,
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }
    payload_b64 = _b64(json.dumps(payload, separators=(",", ":")).encode())
    return f"{payload_b64}.{_sign(payload_b64)}"


def parse_token(token: str) -> dict[str, Any]:
    try:
        payload_b64, sig = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Malformed token") from exc
    expected = _sign(payload_b64)
    if not hmac.compare_digest(sig, expected):
        raise ValueError("Invalid token signature")
    payload = json.loads(_unb64(payload_b64))
    if int(payload.get("exp", 0)) < int(time.time()):
        raise ValueError("Token expired")
    return payload
