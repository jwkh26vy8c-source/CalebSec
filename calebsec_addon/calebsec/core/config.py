from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "calebsec.sqlite3"
RULES_DIR = BASE_DIR / "rules"

SECRET_KEY = os.getenv("CALEBSEC_SECRET", "dev-only-change-me")
TOKEN_TTL_SECONDS = int(os.getenv("CALEBSEC_TOKEN_TTL_SECONDS", "28800"))
