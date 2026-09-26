"""
Run this once per trading day to authenticate with Zerodha and generate
today's access token.

Usage:
    python scripts/login.py
"""
import sys
from pathlib import Path

# allow running as `python scripts/login.py` from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.auth import generate_access_token, get_login_url  # noqa: E402

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def update_env_access_token(token: str) -> None:
    """Rewrite (or add) the KITE_ACCESS_TOKEN line in .env."""
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    found = False
    for i, line in enumerate(lines):
        if line.startswith("KITE_ACCESS_TOKEN="):
            lines[i] = f"KITE_ACCESS_TOKEN={token}"
            found = True
            break
    if not found:
        lines.append(f"KITE_ACCESS_TOKEN={token}")
    ENV_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    print("Open this URL in your browser and log in to Zerodha:\n")
    print(get_login_url())
    print(
        "\nAfter logging in, you'll be redirected to your app's redirect URL "
        "with a 'request_token' in the query string, e.g.:\n"
        "  http://127.0.0.1:5000/?request_token=abcXYZ...&action=login&status=success\n"
    )
    request_token = input("Paste the request_token here: ").strip()

    access_token = generate_access_token(request_token)
    update_env_access_token(access_token)

    print(f"\nSuccess. Access token saved to {ENV_PATH}.")
    print("This token is valid until ~6 AM IST tomorrow.")


if __name__ == "__main__":
    main()
