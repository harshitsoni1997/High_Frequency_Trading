"""
Market data helpers. These require the paid Kite Connect subscription —
the free Personal API does not include live or historical data.
"""
from datetime import datetime

from kiteconnect import KiteConnect


def get_ltp(kite: KiteConnect, instruments: list[str]) -> dict:
    """
    instruments: list like ['NSE:INFY', 'NSE:TCS']
    Returns last traded price for each.
    """
    return kite.ltp(instruments)


def get_quote(kite: KiteConnect, instruments: list[str]) -> dict:
    """Full quote (depth, OHLC, volume, etc.) for each instrument."""
    return kite.quote(instruments)


def get_historical_data(
    kite: KiteConnect,
    instrument_token: int,
    from_date: datetime,
    to_date: datetime,
    interval: str = "day",
) -> list[dict]:
    """
    interval: 'minute', '3minute', '5minute', '15minute', '30minute', '60minute', 'day'
    instrument_token: numeric token from kite.instruments(), not the trading symbol.
    """
    return kite.historical_data(instrument_token, from_date, to_date, interval)
