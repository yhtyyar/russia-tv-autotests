"""Unit tests for core exceptions."""

from core.exceptions import (
    APIError,
    BrowserError,
    ChannelAPIError,
    FrameworkError,
    ScheduleAPIError,
    SearchAPIError,
    ValidationError,
)


class TestFrameworkError:
    def test_framework_error_message(self):
        exc = FrameworkError("something went wrong")
        assert str(exc) == "something went wrong"
        assert exc.message == "something went wrong"


class TestAPIError:
    def test_api_error_with_status_code(self):
        exc = APIError("not found", status_code=404)
        assert str(exc) == "not found"
        assert exc.status_code == 404

    def test_api_error_without_status_code(self):
        exc = APIError("timeout")
        assert exc.status_code is None


class TestDomainAPIErrors:
    def test_schedule_api_error_is_api_error(self):
        exc = ScheduleAPIError("schedule fail", 500)
        assert isinstance(exc, APIError)
        assert exc.status_code == 500

    def test_channel_api_error_is_api_error(self):
        exc = ChannelAPIError("channel fail", 503)
        assert isinstance(exc, APIError)

    def test_search_api_error_is_api_error(self):
        exc = SearchAPIError("search fail")
        assert isinstance(exc, APIError)


class TestBrowserError:
    def test_browser_error_message(self):
        exc = BrowserError("browser crashed")
        assert isinstance(exc, FrameworkError)
        assert "browser crashed" in str(exc)


class TestValidationError:
    def test_validation_error_message(self):
        exc = ValidationError("invalid date")
        assert isinstance(exc, FrameworkError)
        assert "invalid date" in str(exc)
