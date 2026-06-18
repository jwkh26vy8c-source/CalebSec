from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from calebsec.api.deps import require_permission
from calebsec.auth.store import create_user, get_user, list_users, verify_password
from calebsec.auth.tokens import create_token
from calebsec.core.config import RULES_DIR
from calebsec.core.models import LogEvent, LoginRequest, TokenResponse, UserCreate, UserPublic
from calebsec.ingestion.engine import IngestionEngine
from calebsec.sigma.rules import load_rules


def build_router(engine: IngestionEngine) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict[str, str | int]:
        return {"status": "ok", "rules_loaded": len(engine.rules), "events": len(engine.events), "alerts": len(engine.alerts)}

    @router.post("/auth/login", response_model=TokenResponse)
    def login(payload: LoginRequest) -> TokenResponse:
        user = get_user(payload.username)
        if not user or user.disabled or not verify_password(payload.password, user.password_hash, user.salt):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return TokenResponse(access_token=create_token(user.username, user.role), role=user.role)

    @router.get("/users", response_model=list[UserPublic])
    def users(_: dict = Depends(require_permission("users:read"))) -> list[UserPublic]:
        return [UserPublic(username=u.username, role=u.role, disabled=u.disabled) for u in list_users()]

    @router.post("/users", response_model=UserPublic)
    def add_user(payload: UserCreate, _: dict = Depends(require_permission("users:write"))) -> UserPublic:
        try:
            user = create_user(payload.username, payload.password, payload.role)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Could not create user: {exc}") from exc
        return UserPublic(username=user.username, role=user.role, disabled=user.disabled)

    @router.post("/ingest")
    def ingest(event: LogEvent, _: dict = Depends(require_permission("logs:ingest"))) -> dict:
        alerts = engine.ingest(event)
        return {"ingested": True, "alerts_generated": len(alerts), "alerts": alerts}

    @router.get("/events", response_model=list[LogEvent])
    def events(_: dict = Depends(require_permission("logs:read")), limit: int = 100) -> list[LogEvent]:
        return engine.events[-limit:]

    @router.get("/alerts")
    def alerts(_: dict = Depends(require_permission("alerts:read")), limit: int = 100) -> list:
        return engine.alerts[-limit:]

    @router.get("/rules")
    def rules(_: dict = Depends(require_permission("rules:read"))) -> list[dict]:
        return [{"id": r.rule_id, "title": r.title, "level": r.level, "filepath": r.filepath} for r in engine.rules]

    @router.post("/rules/reload")
    def reload_rules(_: dict = Depends(require_permission("rules:reload"))) -> dict[str, int]:
        engine.set_rules(load_rules(RULES_DIR))
        return {"rules_loaded": len(engine.rules)}

    return router
