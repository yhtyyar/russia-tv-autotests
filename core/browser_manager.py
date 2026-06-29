"""Управление жизненным циклом браузера Playwright."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from playwright.async_api import Browser, BrowserContext, Page, Playwright

from config.browsers import launch_browser
from config.settings import get_settings


class BrowserManager:
    """Управляет экземплярами Playwright: браузерами, контекстами и страницами."""

    def __init__(self, playwright: Playwright) -> None:
        """Инициализация с экземпляром Playwright.

        Args:
            playwright: Асинхронный экземпляр Playwright.
        """
        self.playwright = playwright
        self.settings = get_settings()
        self._browser: Browser | None = None

    async def launch(self) -> Browser:
        """Запуск настроенного браузера.

        Returns:
            Запущенный экземпляр Browser.
        """
        browser_type = getattr(
            self.playwright,
            self.settings.browser,
            self.playwright.chromium,
        )
        self._browser = await launch_browser(
            browser_type=browser_type,
            headless=self.settings.headless,
            slow_mo=self.settings.slow_mo,
        )
        return self._browser

    async def new_context(self, **kwargs: Any) -> BrowserContext:
        """Создать новый контекст браузера.

        Args:
            **kwargs: Опции создания контекста.

        Returns:
            Новый BrowserContext.

        Raises:
            RuntimeError: Если браузер не удалось запустить.
        """
        if self._browser is None:
            await self.launch()
        if self._browser is None:
            raise RuntimeError("Browser failed to launch")
        return await self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="reports/videos" if kwargs.pop("record_video", False) else None,
            **kwargs,
        )

    async def new_page(self, **kwargs: Any) -> Page:
        """Создать новую страницу в свежем контексте.

        Args:
            **kwargs: Опции создания страницы.

        Returns:
            Новая Page.
        """
        context = await self.new_context(**kwargs)
        return await context.new_page()

    async def close(self) -> None:
        """Закрыть экземпляр браузера, если он открыт."""
        if self._browser is not None:
            await self._browser.close()
            self._browser = None


@asynccontextmanager
async def managed_browser(
    playwright: Playwright,
) -> AsyncGenerator[BrowserManager, None]:
    """Контекстный менеджер жизненного цикла браузера.

    Args:
        playwright: Асинхронный экземпляр Playwright.

    Yields:
        BrowserManager, готовый к использованию.
    """
    manager = BrowserManager(playwright)
    try:
        yield manager
    finally:
        await manager.close()


@asynccontextmanager
async def managed_page(
    playwright: Playwright,
    **kwargs: Any,
) -> AsyncGenerator[Page, None]:
    """Контекстный менеджер жизненного цикла одной страницы.

    Args:
        playwright: Асинхронный экземпляр Playwright.
        **kwargs: Опции, передаваемые в new_page.

    Yields:
        Готовая страница Playwright.
    """
    async with managed_browser(playwright) as manager:
        page = await manager.new_page(**kwargs)
        try:
            yield page
        finally:
            await page.close()
