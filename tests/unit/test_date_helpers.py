"""Unit tests for date_helpers utilities."""

from datetime import date, timedelta

import pytest

from utils.date_helpers import format_schedule_date, get_week_range, parse_time


class TestFormatScheduleDate:
    """Tests for format_schedule_date function."""

    def test_today_returns_iso_date(self):
        result = format_schedule_date("today")
        assert result == date.today().isoformat()

    def test_yesterday_returns_iso_date(self):
        result = format_schedule_date("yesterday")
        expected = (date.today() - timedelta(days=1)).isoformat()
        assert result == expected

    def test_tomorrow_returns_iso_date(self):
        result = format_schedule_date("tomorrow")
        expected = (date.today() + timedelta(days=1)).isoformat()
        assert result == expected

    def test_iso_date_passthrough(self):
        result = format_schedule_date("2026-06-25")
        assert result == "2026-06-25"

    def test_invalid_date_raises(self):
        with pytest.raises(ValueError):
            format_schedule_date("invalid-date")


class TestGetWeekRange:
    """Tests for get_week_range function."""

    def test_default_returns_7_days(self):
        start, end = get_week_range()
        assert (end - start).days == 6

    def test_specific_date(self):
        ref = date(2026, 6, 25)  # Thursday
        start, end = get_week_range(ref)
        assert start == date(2026, 6, 22)  # Monday
        assert end == date(2026, 6, 28)  # Sunday
        assert (end - start).days == 6


class TestParseTime:
    """Tests for parse_time function."""

    def test_hh_mm_format(self):
        dt = parse_time("14:30")
        assert dt.hour == 14
        assert dt.minute == 30

    def test_hh_mm_ss_format(self):
        dt = parse_time("14:30:45")
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45

    def test_invalid_time_raises(self):
        with pytest.raises(ValueError):
            parse_time("not-a-time")
