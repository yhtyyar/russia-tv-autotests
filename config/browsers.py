"""Хелперы конфигурации запуска браузера."""

import logging
import os
import platform
from typing import Any

from playwright.async_api import Browser, BrowserType

logger = logging.getLogger("russia_tv_tests.browsers")


_YANDEX_PATHS = {
    "Linux": [
        "/usr/bin/yandex-browser",
        "/usr/bin/yandex-browser-stable",
        "/usr/bin/yandex-browser-beta",
        "/snap/bin/yandex-browser",
    ],
    "Windows": [
        r"C:\Program Files\Yandex\YandexBrowser\Application\browser.exe",
        r"C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe",
    ],
    "Darwin": [
        "/Applications/Yandex Browser.app/Contents/MacOS/Yandex Browser",
    ],
}


def detect_yandex_browser() -> str | None:
    """Найти путь к исполняемому файлу Яндекс Браузера.

    Returns:
        Абсолютный путь к исполняемому файлу или None.
    """
    system = platform.system()
    paths = _YANDEX_PATHS.get(system, [])
    for path in paths:
        if os.path.isfile(path):
            logger.info("Найден Яндекс Браузер: %s", path)
            return path
    logger.warning("Яндекс Браузер не найден в стандартных путях (%s)", system)
    return None


def get_browser_launch_args(
    headless: bool = True,
    slow_mo: int = 0,
    executable_path: str | None = None,
) -> dict[str, Any]:
    """Сформировать аргументы запуска браузера Playwright.

    Args:
        headless: Запускать браузер в headless-режиме.
        slow_mo: Замедлить операции на указанное количество миллисекунд.
        executable_path: Путь к кастомному исполняемому файлу браузера.

    Returns:
        Словарь опций запуска для Playwright.
    """
    args: dict[str, Any] = {
        "headless": headless,
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
    }
    if executable_path:
        args["executable_path"] = executable_path
    if slow_mo > 0:
        args["slow_mo"] = slow_mo
    return args


async def launch_browser(
    browser_type: BrowserType,
    headless: bool = True,
    slow_mo: int = 0,
    executable_path: str | None = None,
) -> Browser:
    """Запустить экземпляр браузера с дефолтами проекта.

    Args:
        browser_type: Экземпляр Playwright BrowserType.
        headless: Запускать браузер в headless-режиме.
        slow_mo: Замедлить операции на указанное количество миллисекунд.
        executable_path: Путь к кастомному исполняемому файлу браузера.

    Returns:
        Запущенный экземпляр Browser.
    """
    launch_options = get_browser_launch_args(headless, slow_mo, executable_path)
    return await browser_type.launch(**launch_options)
