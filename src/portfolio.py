"""Read-only account info: holdings, positions, funds/margins."""
from kiteconnect import KiteConnect


def get_holdings(kite: KiteConnect) -> list[dict]:
    """Long-term (delivery) holdings."""
    return kite.holdings()


def get_positions(kite: KiteConnect) -> dict:
    """Intraday and carry-forward positions, split into 'day' and 'net'."""
    return kite.positions()


def get_margins(kite: KiteConnect, segment: str | None = None) -> dict:
    """Available cash/margins. segment: 'equity' or 'commodity', or None for both."""
    return kite.margins(segment) if segment else kite.margins()
