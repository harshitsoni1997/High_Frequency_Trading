"""
Unit tests for src/orders.py using a mocked KiteConnect client — these never
hit the real API or place real orders.
"""
from unittest.mock import MagicMock

import pytest

from src.orders import (
    cancel_order,
    get_order_status,
    place_limit_order,
    place_market_order,
)


@pytest.fixture
def mock_kite():
    kite = MagicMock()
    kite.ORDER_TYPE_MARKET = "MARKET"
    kite.ORDER_TYPE_LIMIT = "LIMIT"
    kite.place_order.return_value = "ORDER123"
    return kite


def test_place_market_order(mock_kite):
    order_id = place_market_order(
        mock_kite,
        tradingsymbol="INFY",
        exchange="NSE",
        transaction_type="BUY",
        quantity=1,
    )
    assert order_id == "ORDER123"
    mock_kite.place_order.assert_called_once()
    _, kwargs = mock_kite.place_order.call_args
    assert kwargs["tradingsymbol"] == "INFY"
    assert kwargs["transaction_type"] == "BUY"
    assert kwargs["order_type"] == "MARKET"


def test_place_limit_order(mock_kite):
    order_id = place_limit_order(
        mock_kite,
        tradingsymbol="TCS",
        exchange="NSE",
        transaction_type="SELL",
        quantity=2,
        price=3500.5,
    )
    assert order_id == "ORDER123"
    _, kwargs = mock_kite.place_order.call_args
    assert kwargs["price"] == 3500.5
    assert kwargs["order_type"] == "LIMIT"


def test_cancel_order(mock_kite):
    cancel_order(mock_kite, order_id="ORDER123")
    mock_kite.cancel_order.assert_called_once_with(
        variety="regular", order_id="ORDER123"
    )


def test_get_order_status(mock_kite):
    mock_kite.order_history.return_value = [
        {"status": "OPEN"},
        {"status": "COMPLETE"},
    ]
    status = get_order_status(mock_kite, "ORDER123")
    assert status == "COMPLETE"
