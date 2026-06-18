from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Role(str, Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role


class UserCreate(BaseModel):
    username: str
    password: str = Field(min_length=8)
    role: Role = Role.viewer


class UserPublic(BaseModel):
    username: str
    role: Role
    disabled: bool = False


class LogEvent(BaseModel):
    source: str = "unknown"
    message: str
    event_id: Optional[int | str] = None
    user: Optional[str] = None
    src_ip: Optional[str] = None
    host: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)


class Alert(BaseModel):
    rule_id: str
    title: str
    level: str = "medium"
    event: LogEvent
    matched_fields: List[str] = Field(default_factory=list)
