"""Доменные исключения для тестового фреймворка."""


class FrameworkError(Exception):
    """Базовое исключение для всех ошибок фреймворка."""

    def __init__(self, message: str) -> None:
        """Инициализация с сообщением об ошибке.

        Args:
            message: Человекочитаемое описание ошибки.
        """
        super().__init__(message)
        self.message = message


class APIError(FrameworkError):
    """Базовое исключение для ошибок API."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Инициализация с сообщением и опциональным статус-кодом.

        Args:
            message: Описание ошибки.
            status_code: HTTP статус-код, если применимо.
        """
        super().__init__(message)
        self.status_code = status_code


class ScheduleAPIError(APIError):
    """Ошибка, возникающая при операциях API расписания."""


class ChannelAPIError(APIError):
    """Ошибка, возникающая при операциях API каналов."""


class SearchAPIError(APIError):
    """Ошибка, возникающая при операциях API поиска."""


class BrowserError(FrameworkError):
    """Ошибка, возникающая при операциях браузера."""


class ValidationError(FrameworkError):
    """Ошибка, возникающая при ошибках валидации данных."""
