from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

from .enums import MarketPosition, OrderState, ConnectionState, OrderType, Action, TimeInForce

@dataclass
class Position:
    instrument: str
    account: str
    market_position: MarketPosition
    quantity: int
    average_entry_price: Decimal

    @classmethod
    def from_file_content(cls, instrument: str, account: str, content: str) -> "Position":
        market_position, quantity, avg_price = content.strip().split(";")
        return cls(
            instrument=instrument,
            account=account,
            market_position=MarketPosition(market_position.strip()),
            quantity=int(quantity.strip()),
            average_entry_price=Decimal(avg_price.strip())
        )

@dataclass
class Order:
    order_id: str
    state: OrderState
    filled_amount: int
    average_fill_price: Optional[Decimal]
    
    # Original order parameters
    account: str
    instrument: str
    action: Action
    quantity: int
    order_type: OrderType
    limit_price: Optional[Decimal]
    stop_price: Optional[Decimal]
    tif: TimeInForce
    oco_id: Optional[str]
    strategy: Optional[str]
    strategy_id: Optional[str]

    @classmethod
    def from_file_content(cls, order_id: str, content: str, **kwargs) -> "Order":
        state, filled_amount, avg_price = content.strip().split(";")
        return cls(
            order_id=order_id,
            state=OrderState(state.strip()),
            filled_amount=int(filled_amount.strip()),
            average_fill_price=Decimal(avg_price.strip()) if avg_price.strip() else None,
            **kwargs
        )

@dataclass
class Connection:
    name: str
    state: ConnectionState

    @classmethod
    def from_file_content(cls, name: str, content: str) -> "Connection":
        return cls(
            name=name,
            state=ConnectionState(content.strip())
        ) 