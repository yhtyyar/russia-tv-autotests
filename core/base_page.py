"""Base Page Object class for Playwright pages."""

from abc import ABC, abstractmethod

from playwright.async_api import Page

from config.settings import get_settings


class BasePage(ABC):
    """Abstract base class for all page objects.

    Provides common interaction methods and URL handling.
    """

    def __init__(self, page: Page) -> None:
        """Initialize page object.

        Args:
            page: Playwright Page instance.
        """
        self.page = page
        self.settings = get_settings()
        self.base_url = self.settings.base_url.rstrip("/")

    @property
    @abstractmethod
    def path(self) -> str:
        """URL path for the page. Override in subclasses."""

    @property
    def url(self) -> str:
        """Full URL for the page."""
        return f"{self.base_url}{self.path}"

    async def goto(self, **kwargs) -> None:
        """Navigate to the page URL.

        Args:
            **kwargs: Additional arguments passed to page.goto.
        """
        await self.page.goto(self.url, **kwargs)

    async def wait_for_load(self, state: str = "networkidle") -> None:
        """Wait for page to reach desired load state.

        Args:
            state: Load state to wait for (load, domcontentloaded, networkidle).
        """
        await self.page.wait_for_load_state(state)

    async def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible on the page.

        Args:
            selector: CSS or XPath selector.

        Returns:
            True if element is visible, False otherwise.
        """
        element = await self.page.query_selector(selector)
        if element is None:
            return False
        return await element.is_visible()

    async def click(self, selector: str, **kwargs) -> None:
        """Click an element.

        Args:
            selector: CSS or XPath selector.
            **kwargs: Additional arguments passed to page.click.
        """
        await self.page.click(selector, **kwargs)

    async def fill(self, selector: str, value: str) -> None:
        """Fill input field.

        Args:
            selector: CSS or XPath selector for input.
            value: Value to fill.
        """
        await self.page.fill(selector, value)

    async def get_text(self, selector: str) -> str:
        """Get text content of an element.

        Args:
            selector: CSS or XPath selector.

        Returns:
            Element text content.
        """
        element = await self.page.query_selector(selector)
        if element is None:
            return ""
        text = await element.text_content()
        return text or ""

    async def take_screenshot(self, name: str) -> str:
        """Take a screenshot and save to reports directory.

        Args:
            name: Screenshot file name (without extension).

        Returns:
            Path to saved screenshot.
        """
        import os

        path = os.path.join(self.settings.screenshot_dir, f"{name}.png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        await self.page.screenshot(path=path, full_page=True)
        return path
