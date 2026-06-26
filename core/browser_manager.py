"""Browser lifecycle management for Playwright."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from playwright.async_api import Browser, BrowserContext, Page, Playwright

from config.browsers import launch_browser
from config.settings import get_settings


class BrowserManager:
    """Manages Playwright browser instances, contexts and pages."""

    def __init__(self, playwright: Playwright) -> None:
        """Initialize with Playwright instance.

        Args:
            playwright: Playwright async instance.
        """
        self.playwright = playwright
        self.settings = get_settings()
        self._browser: Browser | None = None

    async def launch(self) -> Browser:
        """Launch configured browser.

        Returns:
            Launched Browser instance.
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

    async def new_context(self, **kwargs) -> BrowserContext:
        """Create new browser context.

        Args:
            **kwargs: Context creation options.

        Returns:
            New BrowserContext.
        """
        if self._browser is None:
            await self.launch()
        assert self._browser is not None
        return await self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="reports/videos" if kwargs.pop("record_video", False) else None,
            **kwargs,
        )

    async def new_page(self, **kwargs) -> Page:
        """Create new page in fresh context.

        Args:
            **kwargs: Page creation options.

        Returns:
            New Page.
        """
        context = await self.new_context(**kwargs)
        return await context.new_page()

    async def close(self) -> None:
        """Close browser instance if open."""
        if self._browser is not None:
            await self._browser.close()
            self._browser = None


@asynccontextmanager
async def managed_browser(
    playwright: Playwright,
) -> AsyncGenerator[BrowserManager, None]:
    """Context manager for browser lifecycle.

    Args:
        playwright: Playwright async instance.

    Yields:
        BrowserManager ready for use.
    """
    manager = BrowserManager(playwright)
    try:
        yield manager
    finally:
        await manager.close()


@asynccontextmanager
async def managed_page(
    playwright: Playwright,
    **kwargs,
) -> AsyncGenerator[Page, None]:
    """Context manager for a single page lifecycle.

    Args:
        playwright: Playwright async instance.
        **kwargs: Options passed to new_page.

    Yields:
        Ready Playwright Page.
    """
    async with managed_browser(playwright) as manager:
        page = await manager.new_page(**kwargs)
        try:
            yield page
        finally:
            await page.close()
