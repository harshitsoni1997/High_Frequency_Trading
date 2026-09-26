"""
Handles the daily Kite Connect login flow.

Zerodha has no headless/programmatic login: you must open a browser, log in,
and capture the `request_token` from the redirect URL. This module wraps
that exchange. See scripts/login.py for the interactive CLI that uses it.
"""
from kiteconnect import KiteConnect

from config import settings


def get_login_url() -> str:
    """Return the URL the user must open in a browser to log in."""
    settings.require_credentials()
    kite = KiteConnect(api_key=settings.KITE_API_KEY)
    return kite.login_url()


def generate_access_token(request_token: str) -> str:
    """
    Exchange a request_token (captured from the redirect URL after login)
    for an access_token. The access_token is valid until ~6 AM IST the next day.
    """
    settings.require_credentials()
    kite = KiteConnect(api_key=settings.KITE_API_KEY)
    data = kite.generate_session(request_token, api_secret=settings.KITE_API_SECRET)
    return data["access_token"]
