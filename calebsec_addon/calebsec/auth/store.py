from __future__ import annotations

import hashlib
import hmac
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from calebsec.core.config import DB_PATH, DATA_DIR
from calebsec.core.models import Role


@dataclass
class UserRecord:
    username: str
    password_hash: str
    salt: str
    role: Role
    disabled: bool = False


def _connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 210_000).hex()
    return digest, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    digest, _ = hash_password(password, salt)
    return hmac.compare_digest(digest, stored_hash)


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL,
                disabled INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        existing = conn.execute("SELECT username FROM users WHERE username = ?", ("admin",)).fetchone()
        if not existing:
            pwd_hash, salt = hash_password("ChangeMe123!")
            conn.execute(
                "INSERT INTO users(username, password_hash, salt, role, disabled) VALUES (?, ?, ?, ?, 0)",
                ("admin", pwd_hash, salt, Role.admin.value),
            )
        conn.commit()


def get_user(username: str) -> UserRecord | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        return None
    return UserRecord(
        username=row["username"],
        password_hash=row["password_hash"],
        salt=row["salt"],
        role=Role(row["role"]),
        disabled=bool(row["disabled"]),
    )


def create_user(username: str, password: str, role: Role) -> UserRecord:
    pwd_hash, salt = hash_password(password)
    with _connect() as conn:
        conn.execute(
            "INSERT INTO users(username, password_hash, salt, role, disabled) VALUES (?, ?, ?, ?, 0)",
            (username, pwd_hash, salt, role.value),
        )
        conn.commit()
    return get_user(username)  # type: ignore[return-value]


def list_users() -> list[UserRecord]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY username").fetchall()
    return [
        UserRecord(
            username=row["username"],
            password_hash=row["password_hash"],
            salt=row["salt"],
            role=Role(row["role"]),
            disabled=bool(row["disabled"]),
        )
        for row in rows
    ]
