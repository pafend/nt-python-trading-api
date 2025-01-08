"""Tests for the enums."""
import pytest

from nt_trading_api import (
    OrderType, Action, TimeInForce,
    MarketPosition, OrderState, ConnectionState
)
from nt_trading_api.enums import Command

def test_order_type_values():
    """Test OrderType enum values."""
    assert OrderType.MARKET.value == "MARKET"
    assert OrderType.LIMIT.value == "LIMIT"
    assert OrderType.STOPMARKET.value == "STOPMARKET"
    assert OrderType.STOPLIMIT.value == "STOPLIMIT"

def test_action_values():
    """Test Action enum values."""
    assert Action.BUY.value == "BUY"
    assert Action.SELL.value == "SELL"

def test_time_in_force_values():
    """Test TimeInForce enum values."""
    assert TimeInForce.DAY.value == "DAY"
    assert TimeInForce.GTC.value == "GTC"

def test_market_position_values():
    """Test MarketPosition enum values."""
    assert MarketPosition.LONG.value == "LONG"
    assert MarketPosition.SHORT.value == "SHORT"
    assert MarketPosition.FLAT.value == "FLAT"

def test_order_state_values():
    """Test OrderState enum values."""
    assert OrderState.ACCEPTED.value == "Accepted"
    assert OrderState.CANCELLED.value == "Cancelled"
    assert OrderState.FILLED.value == "Filled"
    assert OrderState.INITIALIZED.value == "Initialized"
    assert OrderState.PARTFILLED.value == "PartFilled"
    assert OrderState.REJECTED.value == "Rejected"
    assert OrderState.SUBMITTED.value == "Submitted"
    assert OrderState.WORKING.value == "Working"

def test_connection_state_values():
    """Test ConnectionState enum values."""
    assert ConnectionState.CONNECTED.value == "CONNECTED"
    assert ConnectionState.DISCONNECTED.value == "DISCONNECTED"

def test_command_values():
    """Test Command enum values."""
    assert Command.CANCEL.value == "CANCEL"
    assert Command.CANCELALLORDERS.value == "CANCELALLORDERS"
    assert Command.CHANGE.value == "CHANGE"
    assert Command.CLOSEPOSITION.value == "CLOSEPOSITION"
    assert Command.CLOSESTRATEGY.value == "CLOSESTRATEGY"
    assert Command.FLATTENEVERYTHING.value == "FLATTENEVERYTHING"
    assert Command.PLACE.value == "PLACE"
    assert Command.REVERSEPOSITION.value == "REVERSEPOSITION"

def test_enum_string_comparison():
    """Test that enums can be compared with strings."""
    assert OrderType.MARKET == "MARKET"
    assert Action.BUY == "BUY"
    assert TimeInForce.DAY == "DAY"
    assert MarketPosition.LONG == "LONG"
    assert OrderState.WORKING == "Working"
    assert ConnectionState.CONNECTED == "CONNECTED"
    assert Command.PLACE == "PLACE"

def test_enum_from_string():
    """Test creating enums from strings."""
    assert OrderType("MARKET") == OrderType.MARKET
    assert Action("BUY") == Action.BUY
    assert TimeInForce("DAY") == TimeInForce.DAY
    assert MarketPosition("LONG") == MarketPosition.LONG
    assert OrderState("Working") == OrderState.WORKING
    assert ConnectionState("CONNECTED") == ConnectionState.CONNECTED
    assert Command("PLACE") == Command.PLACE

def test_invalid_enum_values():
    """Test handling invalid enum values."""
    with pytest.raises(ValueError):
        OrderType("INVALID")
    with pytest.raises(ValueError):
        Action("INVALID")
    with pytest.raises(ValueError):
        TimeInForce("INVALID")
    with pytest.raises(ValueError):
        MarketPosition("INVALID")
    with pytest.raises(ValueError):
        OrderState("INVALID")
    with pytest.raises(ValueError):
        ConnectionState("INVALID")
    with pytest.raises(ValueError):
        Command("INVALID") 