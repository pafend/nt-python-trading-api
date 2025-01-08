"""Tests for the core NinjaTrader functionality."""
import os
from decimal import Decimal
import time
import pytest

from nt_trading_api import (
    NinjaTrader, OrderType, Action, TimeInForce,
    MarketPosition, OrderState, ConnectionState
)
from nt_trading_api.exceptions import ValidationError

def test_initialization(temp_dir):
    """Test NinjaTrader initialization."""
    nt = NinjaTrader(documents_dir=temp_dir)
    
    # Check directories are created
    assert os.path.exists(nt.incoming_dir)
    assert os.path.exists(nt.outgoing_dir)

def test_place_order(nt):
    """Test placing an order."""
    order_id = nt.place_order(
        account="TestAccount",
        instrument="ES 12-23",
        action=Action.BUY,
        quantity=1,
        order_type=OrderType.MARKET,
        tif=TimeInForce.DAY
    )
    
    # Check command file was created
    files = list(os.listdir(nt.incoming_dir))
    assert len(files) == 1
    
    # Check command content
    with open(os.path.join(nt.incoming_dir, files[0])) as f:
        content = f.read()
        parts = content.split("|")
        assert parts[0] == "PLACE"
        assert "TestAccount" in parts
        assert "ES 12-23" in parts
        assert "BUY" in parts
        assert "1" in parts
        assert "MARKET" in parts
        assert "DAY" in parts

def test_order_updates(nt, mock_order_update):
    """Test order state updates."""
    order_id = "test_order"
    mock_order_update(order_id, "Working", 0, 0)
    time.sleep(0.1)  # Allow file watcher to process
    
    order = nt.get_order(order_id)
    assert order is not None
    assert order.state == OrderState.WORKING
    assert order.filled_amount == 0

    # Test fill update
    mock_order_update(order_id, "Filled", 1, 4500.50)
    time.sleep(0.1)
    
    order = nt.get_order(order_id)
    assert order.state == OrderState.FILLED
    assert order.filled_amount == 1
    assert order.average_fill_price == Decimal("4500.50")

def test_position_updates(nt, mock_position_update):
    """Test position updates."""
    mock_position_update("ES 12-23", "TestAccount", "LONG", 1, 4500.50)
    time.sleep(0.1)
    
    position = nt.get_position("ES 12-23", "TestAccount")
    assert position is not None
    assert position.market_position == MarketPosition.LONG
    assert position.quantity == 1
    assert position.average_entry_price == Decimal("4500.50")

def test_connection_updates(nt, mock_connection_update):
    """Test connection state updates."""
    mock_connection_update("Sim101", "CONNECTED")
    time.sleep(0.1)
    
    connection = nt.get_connection("Sim101")
    assert connection is not None
    assert connection.state == ConnectionState.CONNECTED

def test_cancel_order(nt):
    """Test canceling an order."""
    nt.cancel_order("test_order")
    
    files = list(os.listdir(nt.incoming_dir))
    assert len(files) == 1
    
    with open(os.path.join(nt.incoming_dir, files[0])) as f:
        content = f.read()
        parts = content.split("|")
        assert parts[0] == "CANCEL"
        assert "test_order" in parts

def test_change_order(nt):
    """Test changing an order."""
    nt.change_order(
        order_id="test_order",
        quantity=2,
        limit_price=Decimal("4500.50")
    )
    
    files = list(os.listdir(nt.incoming_dir))
    assert len(files) == 1
    
    with open(os.path.join(nt.incoming_dir, files[0])) as f:
        content = f.read()
        parts = content.split("|")
        assert parts[0] == "CHANGE"
        assert "test_order" in parts
        assert "2" in parts
        assert "4500.50" in parts

def test_close_position(nt):
    """Test closing a position."""
    nt.close_position("TestAccount", "ES 12-23")
    
    files = list(os.listdir(nt.incoming_dir))
    assert len(files) == 1
    
    with open(os.path.join(nt.incoming_dir, files[0])) as f:
        content = f.read()
        parts = content.split("|")
        assert parts[0] == "CLOSEPOSITION"
        assert "TestAccount" in parts
        assert "ES 12-23" in parts

def test_flatten_everything(nt):
    """Test flattening all positions."""
    nt.flatten_everything()
    
    files = list(os.listdir(nt.incoming_dir))
    assert len(files) == 1
    
    with open(os.path.join(nt.incoming_dir, files[0])) as f:
        content = f.read()
        assert content.startswith("FLATTENEVERYTHING") 