"""Tests for the data models."""
from decimal import Decimal
import pytest

from nt_trading_api import (
    MarketPosition, OrderState, ConnectionState,
    OrderType, Action, TimeInForce
)
from nt_trading_api.models import Position, Order, Connection

def test_position_from_file():
    """Test creating a Position from file content."""
    content = "LONG;1;4500.50"
    position = Position.from_file_content("ES 12-23", "TestAccount", content)
    
    assert position.instrument == "ES 12-23"
    assert position.account == "TestAccount"
    assert position.market_position == MarketPosition.LONG
    assert position.quantity == 1
    assert position.average_entry_price == Decimal("4500.50")

def test_order_from_file():
    """Test creating an Order from file content."""
    content = "Working;0;0"
    order = Order.from_file_content(
        order_id="test_order",
        content=content,
        account="TestAccount",
        instrument="ES 12-23",
        action=Action.BUY,
        quantity=1,
        order_type=OrderType.MARKET,
        limit_price=None,
        stop_price=None,
        tif=TimeInForce.DAY,
        oco_id=None,
        strategy=None,
        strategy_id=None
    )
    
    assert order.order_id == "test_order"
    assert order.state == OrderState.WORKING
    assert order.filled_amount == 0
    assert order.average_fill_price is None
    assert order.account == "TestAccount"
    assert order.instrument == "ES 12-23"
    assert order.action == Action.BUY
    assert order.quantity == 1
    assert order.order_type == OrderType.MARKET
    assert order.tif == TimeInForce.DAY

def test_connection_from_file():
    """Test creating a Connection from file content."""
    content = "CONNECTED"
    connection = Connection.from_file_content("Sim101", content)
    
    assert connection.name == "Sim101"
    assert connection.state == ConnectionState.CONNECTED

def test_position_invalid_market_position():
    """Test handling invalid market position."""
    content = "INVALID;1;4500.50"
    with pytest.raises(ValueError):
        Position.from_file_content("ES 12-23", "TestAccount", content)

def test_order_invalid_state():
    """Test handling invalid order state."""
    content = "INVALID;0;0"
    with pytest.raises(ValueError):
        Order.from_file_content(
            order_id="test_order",
            content=content,
            account="TestAccount",
            instrument="ES 12-23",
            action=Action.BUY,
            quantity=1,
            order_type=OrderType.MARKET,
            limit_price=None,
            stop_price=None,
            tif=TimeInForce.DAY,
            oco_id=None,
            strategy=None,
            strategy_id=None
        )

def test_connection_invalid_state():
    """Test handling invalid connection state."""
    content = "INVALID"
    with pytest.raises(ValueError):
        Connection.from_file_content("Sim101", content) 