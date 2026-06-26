"""Date formatting and manipulation utilities."""

from datetime import date, datetime, timedelta


def format_schedule_date(value: str) -> str:
    """Convert date keyword or string to ISO date format.

    Args:
        value: One of 'today', 'yesterday', 'tomorrow', or YYYY-MM-DD.

    Returns:
        ISO formatted date string (YYYY-MM-DD).

    Raises:
        ValueError: If value format is not recognized.
    """
    today = date.today()
    match value.lower():
        case "today":
            return today.isoformat()
        case "yesterday":
            return (today - timedelta(days=1)).isoformat()
        case "tomorrow":
            return (today + timedelta(days=1)).isoformat()
        case _:
            try:
                parsed = datetime.strptime(value, "%Y-%m-%d").date()
                return parsed.isoformat()
            except ValueError as exc:
                raise ValueError(
                    f"Invalid date format: {value}. Use 'today', 'yesterday', "
                    f"'tomorrow', or YYYY-MM-DD."
                ) from exc


def get_week_range(ref_date: date | None = None) -> tuple[date, date]:
    """Get start and end dates for a week relative to a date.

    Args:
        ref_date: Reference date (defaults to today).

    Returns:
        Tuple of (week_start, week_end) where end is 6 days after start.
    """
    if ref_date is None:
        ref_date = date.today()
    start = ref_date - timedelta(days=ref_date.weekday())
    end = start + timedelta(days=6)
    return start, end


def parse_time(time_str: str) -> datetime:
    """Parse time string to datetime.

    Args:
        time_str: Time in HH:MM or HH:MM:SS format.

    Returns:
        Datetime object with today's date.
    """
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            parsed = datetime.strptime(time_str, fmt)
            return parsed.replace(
                year=date.today().year,
                month=date.today().month,
                day=date.today().day,
            )
        except ValueError:
            continue
    raise ValueError(f"Invalid time format: {time_str}")
