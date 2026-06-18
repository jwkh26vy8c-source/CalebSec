from __future__ import annotations

import argparse
import asyncio
import threading

import uvicorn
from fastapi import FastAPI

from calebsec.api.routes import build_router
from calebsec.auth.store import init_db
from calebsec.core.config import RULES_DIR
from calebsec.ingestion.engine import IngestionEngine
from calebsec.sigma.rules import load_rules

engine = IngestionEngine()
engine.set_rules(load_rules(RULES_DIR))
app = FastAPI(title="CalebSec", version="0.1.0")
app.include_router(build_router(engine))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CalebSec security backend scaffold")
    parser.add_argument("--init-db", action="store_true", help="Initialize the SQLite database and default admin user")
    parser.add_argument("--serve", action="store_true", help="Run the FastAPI server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--tail", help="Optional file path to live-tail into CalebSec")
    return parser.parse_args()


def _start_tail_thread(file_path: str) -> None:
    def runner() -> None:
        asyncio.run(engine.tail_file(file_path))

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    print(f"Live tail enabled for {file_path}")


def main() -> None:
    args = parse_args()
    if args.init_db:
        init_db()
        print("Database initialized. Default admin: admin / ChangeMe123!")
    if args.tail:
        _start_tail_thread(args.tail)
    if args.serve:
        uvicorn.run(app, host=args.host, port=args.port)
    if not args.init_db and not args.serve:
        print("Nothing to do. Try: python -m calebsec.main --init-db --serve")


if __name__ == "__main__":
    main()
