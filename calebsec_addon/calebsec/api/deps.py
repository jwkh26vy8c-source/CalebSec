from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status

from calebsec.auth.rbac import has_permission
from calebsec.auth.store import get_user
from calebsec.auth.tokens import parse_token
from calebsec.core.models import Role


def current_user(authorization: str | None = Header(default=None)) -> dict[str, str]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = parse_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    user = get_user(str(payload["sub"]))
    if not user or user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User disabled or not found")
    return {"username": user.username, "role": user.role.value}


def require_permission(permission: str):
    def dependency(user: dict[str, str] = Depends(current_user)) -> dict[str, str]:
        role = Role(user["role"])
        if not has_permission(role, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role permissions")
        return user
    return dependency
