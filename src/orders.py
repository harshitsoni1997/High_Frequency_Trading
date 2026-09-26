"""
Order placement helpers. Every function logs what it sent and what came
back, and raises on failure rather than swallowing errors silently — with
real money on the line you want loud, obvious failures.
"""
import logging
from pathlib import Path

from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException

from config.settings import LOG_DIR

logging.basicConfig(
    filename=Path(LOG_DIR) / "orders.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def place_market_order(
    kite: KiteConnect,
    tradingsymbol: str,
    exchange: str,
    transaction_type: str,
    quantity: int,
    product: str = "MIS",
    variety: str = "regular",
) -> str:
    """
    Place a simple market order.

    transaction_type: 'BUY' or 'SELL'
    product: 'MIS' (intraday), 'CNC' (delivery), 'NRML' (F&O carry-forward)
    """
    try:
        order_id = kite.place_order(
            variety=variety,
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
            order_type=kite.ORDER_TYPE_MARKET,
        )
        logger.info(
            "Placed MARKET %s order for %s x%s (%s): order_id=%s",
            transaction_type, tradingsymbol, quantity, product, order_id,
        )
        return order_id
    except KiteException as exc:
        logger.error("Order placement failed for %s: %s", tradingsymbol, exc)
        raise


def place_limit_order(
    kite: KiteConnect,
    tradingsymbol: str,
    exchange: str,
    transaction_type: str,
    quantity: int,
    price: float,
    product: str = "MIS",
    variety: str = "regular",
) -> str:
    """Place a limit order at a specific price."""
    try:
        order_id = kite.place_order(
            variety=variety,
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
            order_type=kite.ORDER_TYPE_LIMIT,
            price=price,
        )
        logger.info(
            "Placed LIMIT %s order for %s x%s @ %s (%s): order_id=%s",
            transaction_type, tradingsymbol, quantity, price, product, order_id,
        )
        return order_id
    except KiteException as exc:
        logger.error("Limit order placement failed for %s: %s", tradingsymbol, exc)
        raise


def place_stop_loss_order(
    kite: KiteConnect,
    tradingsymbol: str,
    exchange: str,
    transaction_type: str,
    quantity: int,
    trigger_price: float,
    price: float | None = None,
    product: str = "MIS",
    variety: str = "regular",
) -> str:
    """
    Place a stop-loss order. Pass `price` for an SL (limit) order, or leave
    it None for an SL-M (market) order that fires at trigger_price.
    """
    order_type = kite.ORDER_TYPE_SL if price is not None else kite.ORDER_TYPE_SLM
    kwargs = dict(
        variety=variety,
        exchange=exchange,
        tradingsymbol=tradingsymbol,
        transaction_type=transaction_type,
        quantity=quantity,
        product=product,
        order_type=order_type,
        trigger_price=trigger_price,
    )
    if price is not None:
        kwargs["price"] = price

    try:
        order_id = kite.place_order(**kwargs)
        logger.info(
            "Placed %s order for %s x%s trigger=%s: order_id=%s",
            order_type, tradingsymbol, quantity, trigger_price, order_id,
        )
        return order_id
    except KiteException as exc:
        logger.error("Stop-loss order placement failed for %s: %s", tradingsymbol, exc)
        raise


def cancel_order(kite: KiteConnect, order_id: str, variety: str = "regular") -> None:
    try:
        kite.cancel_order(variety=variety, order_id=order_id)
        logger.info("Cancelled order_id=%s", order_id)
    except KiteException as exc:
        logger.error("Cancel failed for order_id=%s: %s", order_id, exc)
        raise


def get_order_status(kite: KiteConnect, order_id: str) -> str:
    """Return the latest status string for an order (e.g. COMPLETE, REJECTED)."""
    history = kite.order_history(order_id)
    return history[-1]["status"] if history else "UNKNOWN"
