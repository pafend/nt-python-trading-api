"""Shared test fixtures for the NinjaTrader API test suite."""
import os
import shutil
import tempfile
from pathlib import Path
import pytest

from nt_trading_api import NinjaTrader

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def nt(temp_dir):
    """Create a NinjaTrader instance with a temporary directory."""
    nt = NinjaTrader(documents_dir=temp_dir)
    yield nt
    # Cleanup is handled by __del__ and temp_dir fixture

@pytest.fixture
def mock_order_update(nt):
    """Create a mock order update file."""
    def _create_order_update(order_id: str, state: str, filled: int, avg_price: float):
        path = Path(nt.outgoing_dir) / f"{order_id}.txt"
        with open(path, "w") as f:
            f.write(f"{state};{filled};{avg_price}")
        return path
    return _create_order_update

@pytest.fixture
def mock_position_update(nt):
    """Create a mock position update file."""
    def _create_position_update(instrument: str, account: str, position: str, qty: int, avg_price: float):
        path = Path(nt.outgoing_dir) / f"{instrument}_{account}_Position.txt"
        with open(path, "w") as f:
            f.write(f"{position};{qty};{avg_price}")
        return path
    return _create_position_update

@pytest.fixture
def mock_connection_update(nt):
    """Create a mock connection update file."""
    def _create_connection_update(name: str, state: str):
        path = Path(nt.outgoing_dir) / f"{name}.txt"
        with open(path, "w") as f:
            f.write(state)
        return path
    return _create_connection_update 