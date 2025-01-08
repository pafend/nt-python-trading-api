from enum import Enum, auto

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOPMARKET = "STOPMARKET"
    STOPLIMIT = "STOPLIMIT"

class Action(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class TimeInForce(str, Enum):
    DAY = "DAY"
    GTC = "GTC"

class MarketPosition(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    FLAT = "FLAT"

class OrderState(str, Enum):
    ACCEPTED = "Accepted"
    CANCELLED = "Cancelled"
    FILLED = "Filled"
    INITIALIZED = "Initialized"
    PARTFILLED = "PartFilled"
    REJECTED = "Rejected"
    SUBMITTED = "Submitted"
    WORKING = "Working"

class ConnectionState(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"

class Command(str, Enum):
    CANCEL = "CANCEL"
    CANCELALLORDERS = "CANCELALLORDERS"
    CHANGE = "CHANGE"
    CLOSEPOSITION = "CLOSEPOSITION"
    CLOSESTRATEGY = "CLOSESTRATEGY"
    FLATTENEVERYTHING = "FLATTENEVERYTHING"
    PLACE = "PLACE"
    REVERSEPOSITION = "REVERSEPOSITION" 