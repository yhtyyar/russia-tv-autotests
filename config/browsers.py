"""Хелперы конфигурации запуска браузера."""

from typing import Any

from playwright.async_api import Browser, BrowserType


def get_browser_launch_args(
    headless: bool = True,
    slow_mo: int = 0,
) -> dict[str, Any]:
    """Сформировать аргументы запуска браузера Playwright.

    Args:
        headless: Запускать браузер в headless-режиме.
        slow_mo: Замедлить операции на указанное количество миллисекунд.

    Returns:
        Словарь опций запуска для Playwright.
    """
    args = {
        "headless": headless,
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
    }
    if slow_mo > 0:
        args["slow_mo"] = slow_mo
    return args


async def launch_browser(
    browser_type: BrowserType,
    headless: bool = True,
    slow_mo: int = 0,
) -> Browser:
    """Запустить экземпляр браузера с дефолтами проекта.

    Args:
        browser_type: Экземпляр Playwright BrowserType.
        headless: Запускать браузер в headless-режиме.
        slow_mo: Замедлить операции на указанное количество миллисекунд.

    Returns:
        Запущенный экземпляр Browser.
    """
    launch_options = get_browser_launch_args(headless, slow_mo)
    return await browser_type.launch(**launch_options)
