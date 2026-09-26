"""
Central place for all configuration. Everything is loaded from environment
variables (via a .env file in development) so secrets never get hard-coded
or committed.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

KITE_API_KEY = os.getenv("KITE_API_KEY", "")
KITE_API_SECRET = os.getenv("KITE_API_SECRET", "")
KITE_ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN", "")

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


def require_credentials() -> None:
    """Fail fast and clearly if the app isn't configured yet."""
    missing = [
        name
        for name, value in [
            ("KITE_API_KEY", KITE_API_KEY),
            ("KITE_API_SECRET", KITE_API_SECRET),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(
            f"Missing required settings: {', '.join(missing)}. "
            "Copy .env.example to .env and fill in your Kite Connect app credentials."
        )
