import os
import time
from pathlib import Path
from typing import Optional, Dict, List
from decimal import Decimal
import uuid
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .enums import OrderType, Action, TimeInForce, Command
from .models import Position, Order, Connection

class NinjaTrader:
    def __init__(self, documents_dir: Optional[str] = None):
        """Initialize the NinjaTrader API.
        
        Args:
            documents_dir: Optional path to the Documents directory. If not provided,
                         will use the default Windows Documents location.
        """
        if documents_dir is None:
            documents_dir = os.path.expanduser("~/Documents")
        
        self.nt_dir = Path(documents_dir) / "NinjaTrader 8"
        self.incoming_dir = self.nt_dir / "incoming"
        self.outgoing_dir = self.nt_dir / "outgoing"
        
        # Ensure directories exist
        self.incoming_dir.mkdir(parents=True, exist_ok=True)
        self.outgoing_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize state
        self._positions: Dict[str, Position] = {}
        self._orders: Dict[str, Order] = {}
        self._connections: Dict[str, Connection] = {}
        
        # Setup file monitoring
        self._setup_monitoring()

    def _setup_monitoring(self):
        """Setup file system monitoring for position and order updates."""
        class Handler(FileSystemEventHandler):
            def __init__(self, nt):
                self.nt = nt
                
            def on_modified(self, event):
                if not event.is_directory:
                    self._handle_file_update(event.src_path)
                    
            def _handle_file_update(self, path):
                filename = os.path.basename(path)
                if filename.endswith("_Position.txt"):
                    self._handle_position_update(path)
                elif filename.endswith(".txt"):
                    if "_" not in filename:  # Order update
                        self._handle_order_update(path)
                    else:  # Connection update
                        self._handle_connection_update(path)
        
        self.observer = Observer()
        self.observer.schedule(Handler(self), str(self.outgoing_dir), recursive=False)
        self.observer.start()

    def _write_command(self, command: Command, **params) -> None:
        """Write a command to the incoming directory."""
        # Generate unique filename
        filename = f"{uuid.uuid4()}.txt"
        filepath = self.incoming_dir / filename
        
        # Build command string
        command_parts = [command.value]
        for key, value in params.items():
            if value is not None:
                if isinstance(value, (int, float, Decimal)):
                    command_parts.append(str(value))
                else:
                    command_parts.append(str(value))
            else:
                command_parts.append("")
        
        # Write command
        with open(filepath, "w") as f:
            f.write("|".join(command_parts))

    def place_order(
        self,
        account: str,
        instrument: str,
        action: Action,
        quantity: int,
        order_type: OrderType,
        limit_price: Optional[Decimal] = None,
        stop_price: Optional[Decimal] = None,
        tif: TimeInForce = TimeInForce.DAY,
        oco_id: Optional[str] = None,
        order_id: Optional[str] = None,
        strategy: Optional[str] = None,
        strategy_id: Optional[str] = None,
    ) -> str:
        """Place a new order."""
        if order_id is None:
            order_id = str(uuid.uuid4())
            
        self._write_command(
            Command.PLACE,
            account=account,
            instrument=instrument,
            action=action,
            quantity=quantity,
            order_type=order_type,
            limit_price=limit_price,
            stop_price=stop_price,
            tif=tif,
            oco_id=oco_id,
            order_id=order_id,
            strategy=strategy,
            strategy_id=strategy_id,
        )
        
        return order_id

    def cancel_order(self, order_id: str, strategy_id: Optional[str] = None) -> None:
        """Cancel an order by its ID."""
        self._write_command(Command.CANCEL, order_id=order_id, strategy_id=strategy_id)

    def cancel_all_orders(self) -> None:
        """Cancel all active orders."""
        self._write_command(Command.CANCELALLORDERS)

    def change_order(
        self,
        order_id: str,
        quantity: Optional[int] = None,
        limit_price: Optional[Decimal] = None,
        stop_price: Optional[Decimal] = None,
        strategy_id: Optional[str] = None,
    ) -> None:
        """Change an existing order."""
        self._write_command(
            Command.CHANGE,
            order_id=order_id,
            quantity=quantity if quantity is not None else 0,
            limit_price=limit_price if limit_price is not None else 0,
            stop_price=stop_price if stop_price is not None else 0,
            strategy_id=strategy_id,
        )

    def close_position(self, account: str, instrument: str) -> None:
        """Close a position for the given account and instrument."""
        self._write_command(Command.CLOSEPOSITION, account=account, instrument=instrument)

    def close_strategy(self, strategy_id: str) -> None:
        """Close an ATM Strategy."""
        self._write_command(Command.CLOSESTRATEGY, strategy_id=strategy_id)

    def flatten_everything(self) -> None:
        """Cancel all orders and flatten all positions."""
        self._write_command(Command.FLATTENEVERYTHING)

    def reverse_position(
        self,
        account: str,
        instrument: str,
        quantity: int,
        order_type: OrderType,
        limit_price: Optional[Decimal] = None,
        stop_price: Optional[Decimal] = None,
        tif: TimeInForce = TimeInForce.DAY,
        oco_id: Optional[str] = None,
        order_id: Optional[str] = None,
        strategy: Optional[str] = None,
        strategy_id: Optional[str] = None,
    ) -> str:
        """Reverse an existing position."""
        if order_id is None:
            order_id = str(uuid.uuid4())
            
        self._write_command(
            Command.REVERSEPOSITION,
            account=account,
            instrument=instrument,
            quantity=quantity,
            order_type=order_type,
            limit_price=limit_price,
            stop_price=stop_price,
            tif=tif,
            oco_id=oco_id,
            order_id=order_id,
            strategy=strategy,
            strategy_id=strategy_id,
        )
        
        return order_id

    def get_position(self, instrument: str, account: str) -> Optional[Position]:
        """Get the current position for an instrument and account."""
        key = f"{instrument}_{account}"
        return self._positions.get(key)

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get an order by its ID."""
        return self._orders.get(order_id)

    def get_connection(self, name: str) -> Optional[Connection]:
        """Get a connection by its name."""
        return self._connections.get(name)

    def __del__(self):
        """Cleanup when the object is destroyed."""
        if hasattr(self, "observer"):
            self.observer.stop()
            self.observer.join() 