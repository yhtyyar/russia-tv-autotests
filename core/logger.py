"""Настройка логирования для фреймворка автотестов."""

import logging
import os
import sys

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging(level: str | None = None) -> None:
    """Настроить корневое логирование проекта.

    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR).
               По умолчанию берётся из переменной окружения LOG_LEVEL.
    """
    log_level = (level or LOG_LEVEL).upper()
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger("russia_tv_tests")
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))
    root_logger.handlers = [handler]
    root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Получить логгер с префиксом проекта.

    Args:
        name: Имя модуля (__name__).

    Returns:
        Настроенный экземпляр logging.Logger.
    """
    return logging.getLogger(f"russia_tv_tests.{name}")
