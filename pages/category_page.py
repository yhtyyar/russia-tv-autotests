"""Page Object страницы категории с отфильтрованными каналами."""

from core.base_page import BasePage


class CategoryPage(BasePage):
    """Страница категории с каналами по выбранной категории."""

    @property
    def path(self) -> str:
        return "/category/{category}"

    _CATEGORY_TITLE = ".category-title, [data-testid='category-title']"
    _CHANNEL_GRID = ".channel-grid, [data-testid='channel-grid']"

    async def open_category(self, category: str) -> None:
        """Перейти на страницу категории.

        Args:
            category: Slug или название категории.
        """
        await self.page.goto(
            f"{self.base_url}/category/{category}",
        )

    async def get_category_title(self) -> str:
        """Получить отображаемое название категории.

        Returns:
            Текст названия категории.
        """
        return await self.get_text(self._CATEGORY_TITLE)

    async def get_channel_count(self) -> int:
        """Посчитать каналы в сетке категории.

        Returns:
            Количество карточек каналов.
        """
        channels = await self.page.query_selector_all(
            f"{self._CHANNEL_GRID} .channel-card",
        )
        return len(channels)
