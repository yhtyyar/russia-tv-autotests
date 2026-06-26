"""Navigation component page object."""

from playwright.async_api import Page


class Navigation:
    """Shared navigation component across pages."""

    def __init__(self, page: Page) -> None:
        """Initialize with page instance.

        Args:
            page: Playwright Page.
        """
        self.page = page

    _NAV_BAR = ".navbar, nav, [data-testid='navbar']"
    _HOME_LINK = "a[href='/'], [data-testid='nav-home']"
    _SCHEDULE_LINK = "a[href='/schedule'], [data-testid='nav-schedule']"
    _CATEGORIES_DROPDOWN = ".categories-dropdown, [data-testid='categories-dropdown']"

    async def go_home(self) -> None:
        """Click home navigation link."""
        await self.page.click(self._HOME_LINK)

    async def go_schedule(self) -> None:
        """Click schedule navigation link."""
        await self.page.click(self._SCHEDULE_LINK)

    async def open_categories(self) -> list[str]:
        """Open categories dropdown and return options.

        Returns:
            List of category link texts.
        """
        await self.page.click(self._CATEGORIES_DROPDOWN)
        links = await self.page.query_selector_all(
            f"{self._CATEGORIES_DROPDOWN} a",
        )
        texts = []
        for link in links:
            text = await link.text_content()
            if text:
                texts.append(text.strip())
        return texts
