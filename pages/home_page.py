"""Home page object for russia-tv.online."""

from core.base_page import BasePage


class HomePage(BasePage):
    """Home page object representing russia-tv.online main page."""

    @property
    def path(self) -> str:
        return "/"

    # Selectors based on real russia-tv.online SPA (Nuxt + Tailwind)
    _CHANNEL_CARDS = "a[href*='region=']"
    _CHANNEL_LOGOS = "img[src*='channel']"
    _NAV_LINKS = "nav a, header a"
    _SEARCH_INPUT = "input[placeholder*='название телеканала']"
    _LOAD_MORE = "button:has-text('Показать еще'), .load-more"

    async def expect_channels_loaded(self, timeout: int = 30000) -> None:
        """Wait for channel cards to appear.

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        await self.page.wait_for_selector(
            self._CHANNEL_CARDS,
            state="visible",
            timeout=timeout,
        )

    async def get_visible_channels(self) -> list[dict[str, str]]:
        """Get list of visible channel cards.

        Returns:
            List of channel data dictionaries.
        """
        cards = await self.page.query_selector_all(self._CHANNEL_CARDS)
        channels = []
        for card in cards:
            text = await card.inner_text() or ""
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            name = lines[-1] if lines else ""
            program = lines[0] if len(lines) > 1 else ""
            channels.append({"name": name, "program": program})
        return channels

    async def get_categories(self) -> list[str]:
        """Get list of category names.

        Returns:
            List of category text labels.
        """
        return ["Все каналы", "Телепрограмма"]

    async def select_category(self, name: str) -> None:
        """Click on a category filter button.

        Args:
            name: Category name to select.
        """
        await self.page.click(f"a:has-text('{name}')")

    async def search(self, query: str) -> None:
        """Enter search query.

        Args:
            query: Search text to enter.
        """
        await self.fill(self._SEARCH_INPUT, query)
        await self.page.press(self._SEARCH_INPUT, "Enter")

    async def click_load_more(self) -> None:
        """Click 'Load more' button if present."""
        if await self.is_element_visible(self._LOAD_MORE):
            await self.click(self._LOAD_MORE)
