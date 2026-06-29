"""Page Object компонента навигации."""

from playwright.async_api import Page


class Navigation:
    """Общий компонент навигации на всех страницах."""

    def __init__(self, page: Page) -> None:
        """Инициализация с экземпляром страницы.

        Args:
            page: Playwright Page.
        """
        self.page = page

    _NAV_BAR = ".navbar, nav, [data-testid='navbar']"
    _HOME_LINK = "a[href='/'], [data-testid='nav-home']"
    _SCHEDULE_LINK = "a[href='/schedule'], [data-testid='nav-schedule']"
    _CATEGORIES_DROPDOWN = ".categories-dropdown, [data-testid='categories-dropdown']"

    async def go_home(self) -> None:
        """Клик по ссылке на главную."""
        await self.page.click(self._HOME_LINK)

    async def go_schedule(self) -> None:
        """Клик по ссылке на расписание."""
        await self.page.click(self._SCHEDULE_LINK)

    async def open_categories(self) -> list[str]:
        """Открыть выпадающий список категорий и вернуть варианты.

        Returns:
            Список текстов ссылок категорий.
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
