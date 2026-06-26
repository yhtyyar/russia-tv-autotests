"""Category page object for filtered channel listings."""

from core.base_page import BasePage


class CategoryPage(BasePage):
    """Category filtered page showing channels by category."""

    @property
    def path(self) -> str:
        return "/category/{category}"

    _CATEGORY_TITLE = ".category-title, [data-testid='category-title']"
    _CHANNEL_GRID = ".channel-grid, [data-testid='channel-grid']"

    async def open_category(self, category: str) -> None:
        """Navigate to category page.

        Args:
            category: Category slug or name.
        """
        await self.page.goto(
            f"{self.base_url}/category/{category}",
        )

    async def get_category_title(self) -> str:
        """Get displayed category title.

        Returns:
            Category title text.
        """
        return await self.get_text(self._CATEGORY_TITLE)

    async def get_channel_count(self) -> int:
        """Count channels in category grid.

        Returns:
            Number of channel cards.
        """
        channels = await self.page.query_selector_all(
            f"{self._CHANNEL_GRID} .channel-card",
        )
        return len(channels)
