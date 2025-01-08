# NinjaTrader Python Trading API

A Python package that provides a clean and type-safe interface to NinjaTrader's automated trading interface.

## Installation

```bash
pip install nt-trading-api
```

## Quick Start

```python
from nt_trading_api import NinjaTrader, OrderType, Action

# Initialize the API
nt = NinjaTrader()

# Place a market order
nt.place_order(
    account="MyAccount",
    instrument="ES 09-23",
    action=Action.BUY,
    quantity=1,
    order_type=OrderType.MARKET,
    tif="DAY"
)

# Monitor positions
position = nt.get_position("ES 09-23", "MyAccount")
print(f"Current position: {position.market_position}, Quantity: {position.quantity}")

# Close all positions
nt.flatten_everything()
```

## Features

- Type-safe interface with proper Python enums and dataclasses
- Automatic file monitoring for position and order updates
- Clean API for all NinjaTrader commands:
  - Place orders
  - Cancel orders
  - Change orders
  - Close positions
  - Manage ATM strategies
  - Monitor order states
  - Monitor positions
  - Monitor connection status

## Documentation

For detailed documentation, please visit the [documentation site](https://your-docs-site.com).

## Author

Pascal Fend (pascal@pascalfend.de)

## License

MIT License - see the [LICENSE](LICENSE) file for details 