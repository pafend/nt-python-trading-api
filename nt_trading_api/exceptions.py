class NinjaTraderError(Exception):
    """Base exception for all NinjaTrader API errors."""
    pass

class ConnectionError(NinjaTraderError):
    """Raised when there is an issue with the NinjaTrader connection."""
    pass

class OrderError(NinjaTraderError):
    """Raised when there is an issue with order placement or modification."""
    pass

class FileSystemError(NinjaTraderError):
    """Raised when there is an issue with the file system operations."""
    pass

class ValidationError(NinjaTraderError):
    """Raised when there is an issue with parameter validation."""
    pass 