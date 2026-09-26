"""
Builds a single, ready-to-use authenticated KiteConnect client for the rest
of the codebase to import, so nothing else has to worry about credentials.
"""
from kiteconnect import KiteConnect

from config import settings


def get_kite() -> KiteConnect:
    """
    Return an authenticated KiteConnect instance.

    Requires KITE_API_KEY and KITE_ACCESS_TOKEN to already be set in the
    environment (the access token is generated once a day via
    scripts/login.py).
    """
    settings.require_credentials()
    if not settings.KITE_ACCESS_TOKEN:
        raise RuntimeError(
            "KITE_ACCESS_TOKEN is not set. Run `python scripts/login.py` first "
            "to log in and generate today's access token."
        )

    kite = KiteConnect(api_key=settings.KITE_API_KEY)
    kite.set_access_token(settings.KITE_ACCESS_TOKEN)
    return kite
