from __future__ import annotations

from calebsec.core.models import Role

PERMISSIONS: dict[Role, set[str]] = {
    Role.admin: {
        "users:read", "users:write", "logs:ingest", "logs:read", "alerts:read", "rules:read", "rules:reload"
    },
    Role.analyst: {"logs:ingest", "logs:read", "alerts:read", "rules:read", "rules:reload"},
    Role.viewer: {"logs:read", "alerts:read", "rules:read"},
}


def has_permission(role: Role, permission: str) -> bool:
    return permission in PERMISSIONS.get(role, set())
