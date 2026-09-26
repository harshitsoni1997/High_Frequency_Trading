"""
A deliberately simple example strategy: if the LTP of a stock has dropped
more than X% from a reference price, buy a fixed quantity.

This is a template to adapt, not a strategy to run as-is — plug in your own
signal, sizing, and risk logic before pointing it at a real account.
"""
from src.kite_client import get_kite
from src.market_data import get_ltp
from src.orders import place_market_order


def run_dip_buy_strategy(
    tradingsymbol: str,
    exchange: str,
    reference_price: float,
    dip_threshold_pct: float,
    quantity: int,
    product: str = "MIS",
) -> str | None:
    """
    Buys `quantity` shares of `tradingsymbol` if the current LTP has fallen
    by at least `dip_threshold_pct` percent below `reference_price`.

    Returns the order_id if an order was placed, else None.
    """
    kite = get_kite()
    instrument = f"{exchange}:{tradingsymbol}"

    ltp_data = get_ltp(kite, [instrument])
    current_price = ltp_data[instrument]["last_price"]

    dip_pct = (reference_price - current_price) / reference_price * 100

    print(f"{tradingsymbol}: reference={reference_price}, ltp={current_price}, dip={dip_pct:.2f}%")

    if dip_pct >= dip_threshold_pct:
        order_id = place_market_order(
            kite,
            tradingsymbol=tradingsymbol,
            exchange=exchange,
            transaction_type="BUY",
            quantity=quantity,
            product=product,
        )
        print(f"Dip threshold hit -> placed BUY order {order_id}")
        return order_id

    print("Dip threshold not hit -> no order placed")
    return None


if __name__ == "__main__":
    # Example: buy 1 share of INFY if it has dropped 2% from 1500
    run_dip_buy_strategy(
        tradingsymbol="INFY",
        exchange="NSE",
        reference_price=1500.0,
        dip_threshold_pct=2.0,
        quantity=1,
    )
