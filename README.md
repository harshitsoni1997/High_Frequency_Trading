# Zerodha Trading Bot

A Python project for placing and managing trades on Zerodha via the official
[Kite Connect](https://kite.trade) API.

> ⚠️ **Trading involves real money and real risk.** Test everything with small
> quantities first. Nothing here is financial advice — you are responsible for
> every order this code places.

## What's in here

```
zerodha-trading-bot/
├── config/
│   └── settings.py        # loads API credentials from .env
├── src/
│   ├── auth.py             # login / access-token generation
│   ├── kite_client.py      # thin wrapper around KiteConnect client
│   ├── orders.py           # place / modify / cancel orders
│   ├── portfolio.py        # holdings, positions, margins
│   ├── market_data.py      # quotes, LTP, historical candles
│   └── strategy_example.py # a simple example strategy
├── scripts/
│   └── login.py            # run this once a day to log in and save the access token
├── tests/
│   └── test_orders.py
├── logs/                    # runtime logs land here (gitignored)
├── .env.example
├── requirements.txt
└── README.md
```

## 1. Get API access from Zerodha

1. Go to [developers.kite.trade](https://developers.kite.trade) and create an app.
   You'll receive an **API key** and **API secret**.
2. Zerodha now offers two tiers:
   - **Kite Connect Personal** — free for individual traders. Lets you place
     orders and read positions/holdings/funds, but gives **no live or
     historical market data**.
   - **Kite Connect (paid)** — adds live quotes, historical candles and
     WebSocket streaming.
   - Check current pricing/terms on the developer console yourself, since
     Zerodha updates this from time to time.
3. When creating the app, set the redirect URL to something like
   `http://127.0.0.1:5000/` (you don't need a real server there for the
   manual login flow described below).

## 2. Set up the project

```bash
git clone <your-new-repo-url>
cd zerodha-trading-bot
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and fill in:

```
KITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
```

## 3. Log in and generate today's access token

Kite Connect has **no headless/programmatic login** — Zerodha requires you to
authenticate through their browser login page once a day (the access token
expires every day around 6 AM IST). Run:

```bash
python scripts/login.py
```

This will:
1. Print a login URL — open it, log in with your Zerodha credentials, and
   approve the app.
2. You'll be redirected to your redirect URL with a `request_token` in the
   query string — paste that back into the terminal when prompted.
3. The script exchanges it for an `access_token` and saves it to `.env`
   (or `access_token.json`, see the script) for the rest of your scripts to use.

You'll need to repeat this once per trading day.

## 4. Place a trade

```bash
python -c "
from src.kite_client import get_kite
from src.orders import place_market_order

kite = get_kite()
order_id = place_market_order(
    kite,
    tradingsymbol='INFY',
    exchange='NSE',
    transaction_type='BUY',
    quantity=1,
)
print('Order placed:', order_id)
"
```

Or look at `src/strategy_example.py` for a fuller example that checks a
condition before placing an order.

## 5. Run tests

```bash
pytest tests/
```

Tests use a mocked Kite client — they never hit the real API or place real
orders.

## Notes on safety

- Start with `product='MIS'` (intraday) and tiny quantities while you test.
- Consider adding `validity='DAY'` and explicit stop-loss orders (`SL`,
  `SL-M`) rather than relying only on your script staying alive.
- Wrap all order calls in try/except and log every request/response —
  see `src/orders.py` for the pattern.
- Keep `.env` and `access_token.json` out of version control (already in
  `.gitignore`).
