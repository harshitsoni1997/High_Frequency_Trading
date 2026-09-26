"""
Free market data using Yahoo Finance (via yfinance), for use alongside the
Kite Connect Personal (free) tier — which covers orders/positions/holdings
but not live or historical market data.

This is a reasonable stand-in for personal/retail use, but be aware:
- Yahoo Finance data can lag real exchange prices by a few seconds to a
  couple of minutes, and is not official exchange data.
- It's rate-limited and unofficial; don't rely on it for latency-sensitive
  or high-frequency strategies.
- If you later upgrade to Kite Connect (paid), switch back to
  src/market_data.py for exchange-grade data.

Zerodha trading symbols (e.g. 'INFY', 'TCS') need a suffix to work with
Yahoo Finance: '.NS' for NSE, '.BO' for BSE.
"""
import yfinance as yf

EXCHANGE_SUFFIX = {
    "NSE": ".NS",
    "BSE": ".BO",
}


def to_yahoo_symbol(tradingsymbol: str, exchange: str = "NSE") -> str:
    """Convert a Zerodha tradingsymbol + exchange into a Yahoo Finance symbol."""
    suffix = EXCHANGE_SUFFIX.get(exchange.upper())
    if suffix is None:
        raise ValueError(f"Unsupported exchange '{exchange}'. Use 'NSE' or 'BSE'.")
    return f"{tradingsymbol.upper()}{suffix}"


def get_ltp_free(tradingsymbol: str, exchange: str = "NSE") -> float:
    """
    Return the latest available price for a single symbol.
    Falls back through a couple of yfinance fields since availability
    varies (pre-market, weekends, delisted symbols, etc.).
    """
    symbol = to_yahoo_symbol(tradingsymbol, exchange)
    ticker = yf.Ticker(symbol)

    info = ticker.fast_info
    price = getattr(info, "last_price", None)
    if price:
        return float(price)

    hist = ticker.history(period="1d", interval="1m")
    if not hist.empty:
        return float(hist["Close"].iloc[-1])

    raise RuntimeError(f"Could not fetch a price for {symbol}. Check the symbol/exchange.")


def get_ltp_batch_free(instruments: list[tuple[str, str]]) -> dict[str, float]:
    """
    instruments: list of (tradingsymbol, exchange) tuples,
                 e.g. [('INFY', 'NSE'), ('TCS', 'NSE')]
    Returns {tradingsymbol: price}.
    """
    result = {}
    for tradingsymbol, exchange in instruments:
        try:
            result[tradingsymbol] = get_ltp_free(tradingsymbol, exchange)
        except RuntimeError as exc:
            print(f"Warning: {exc}")
    return result


def get_historical_data_free(
    tradingsymbol: str,
    exchange: str = "NSE",
    period: str = "6mo",
    interval: str = "1d",
):
    """
    period: '1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'
    interval: '1m','5m','15m','30m','60m','1d','1wk','1mo'
              (intraday intervals like '1m' only cover the last ~7 days)
    Returns a pandas DataFrame with columns: Open, High, Low, Close, Volume.
    """
    symbol = to_yahoo_symbol(tradingsymbol, exchange)
    df = yf.Ticker(symbol).history(period=period, interval=interval)
    if df.empty:
        raise RuntimeError(
            f"No historical data returned for {symbol}. Check the symbol/exchange/period."
        )
    return df


if __name__ == "__main__":
    # quick manual check: python -m src.free_market_data
    price = get_ltp_free("INFY", "NSE")
    print(f"INFY LTP (Yahoo Finance): {price}")

    df = get_historical_data_free("INFY", "NSE", period="5d", interval="1d")
    print(df.tail())
