"""Утилиты для работы со скриншотами."""

import os
from datetime import datetime

from playwright.async_api import Page

from config.settings import get_settings


def _screenshot_dir() -> str:
    """Вернуть настроенную директорию для скриншотов."""
    return get_settings().screenshot_dir


async def capture_full_page(page: Page, name: str) -> str:
    """Сделать скриншот всей страницы.

    Args:
        page: Playwright Page.
        name: Базовое имя файла скриншота.

    Returns:
        Абсолютный путь к сохранённому скриншоту.
    """
    directory = _screenshot_dir()
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(directory, filename)
    await page.screenshot(path=path, full_page=True)
    return path


async def capture_element(page: Page, selector: str, name: str) -> str:
    """Сделать скриншот конкретного элемента.

    Args:
        page: Playwright Page.
        selector: CSS-селектор элемента.
        name: Базовое имя файла скриншота.

    Returns:
        Абсолютный путь к сохранённому скриншоту.
    """
    directory = _screenshot_dir()
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(directory, filename)
    element = await page.query_selector(selector)
    if element is None:
        raise RuntimeError(f"Element not found: {selector}")
    await element.screenshot(path=path)
    return path
