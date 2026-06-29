"""Утилиты форматирования и манипуляции датами."""

from datetime import date, datetime, timedelta


def format_schedule_date(value: str) -> str:
    """Преобразовать ключевое слово даты или строку в ISO-формат.

    Args:
        value: Одно из 'today', 'yesterday', 'tomorrow' или YYYY-MM-DD.

    Returns:
        Строка даты в ISO-формате (YYYY-MM-DD).

    Raises:
        ValueError: Если формат значения не распознан.
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
                    f"Неверный формат даты: {value}. Используйте 'today', 'yesterday', "
                    f"'tomorrow' или YYYY-MM-DD."
                ) from exc


def get_week_range(ref_date: date | None = None) -> tuple[date, date]:
    """Получить начальную и конечную даты недели относительно даты.

    Args:
        ref_date: Опорная дата (по умолчанию сегодня).

    Returns:
        Кортеж (week_start, week_end), где end — через 6 дней после start.
    """
    if ref_date is None:
        ref_date = date.today()
    start = ref_date - timedelta(days=ref_date.weekday())
    end = start + timedelta(days=6)
    return start, end


def parse_time(time_str: str) -> datetime:
    """Разобрать строку времени в datetime.

    Args:
        time_str: Время в формате HH:MM или HH:MM:SS.

    Returns:
        Объект datetime с сегодняшней датой.
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
    raise ValueError(f"Неверный формат времени: {time_str}")
