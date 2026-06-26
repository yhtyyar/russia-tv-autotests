"""Domain-specific exceptions for the test framework."""


class FrameworkError(Exception):
    """Base exception for all framework errors."""

    def __init__(self, message: str) -> None:
        """Initialize with error message.

        Args:
            message: Human-readable error description.
        """
        super().__init__(message)
        self.message = message


class APIError(FrameworkError):
    """Base exception for API-related errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize with message and optional status code.

        Args:
            message: Error description.
            status_code: HTTP status code if applicable.
        """
        super().__init__(message)
        self.status_code = status_code


class ScheduleAPIError(APIError):
    """Error raised by Schedule API operations."""


class ChannelAPIError(APIError):
    """Error raised by Channel API operations."""


class SearchAPIError(APIError):
    """Error raised by Search API operations."""


class BrowserError(FrameworkError):
    """Error raised by browser operations."""


class ValidationError(FrameworkError):
    """Error raised by data validation failures."""
