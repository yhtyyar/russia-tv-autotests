"""E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)."""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileHomePage:
    """Критические сценарии на мобильном viewport (390×844)."""

    async def test_mobile_home_loads(self, mobile_page: Page) -> None:
        """Главная страница корректно загружается на мобильном устройстве."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()
        assert await home.is_footer_visible()

    async def test_mobile_cookie_banner(self, mobile_page: Page) -> None:
        """Баннер cookie-согласия отображается на мобильном экране."""
        home = HomePage(mobile_page)
        await home.goto()
        assert await home.is_cookie_banner_visible()

    async def test_mobile_search(self, mobile_page: Page) -> None:
        """Поиск каналов работает на мобильном устройстве."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.search("Первый")
        await mobile_page.wait_for_load_state("networkidle")
        results = await home.get_visible_channels()
        assert len(results) > 0, "Результаты поиска не отображаются на мобильном"

    async def test_mobile_dark_mode_toggle(self, mobile_page: Page) -> None:
        """Переключение тёмной темы работает на мобильном."""
        home = HomePage(mobile_page)
        await home.goto()
        initial = await home.is_dark_mode_active()
        await home.toggle_dark_mode()
        await mobile_page.wait_for_load_state("networkidle")
        current = await home.is_dark_mode_active()
        assert current != initial

    async def test_mobile_footer_links(self, mobile_page: Page) -> None:
        """Футер содержит валидные ссылки на мобильном."""
        home = HomePage(mobile_page)
        await home.goto()
        assert await home.is_footer_visible()
        links = await home.get_footer_links()
        assert len(links) > 0
        for link in links:
            assert link["href"].startswith("/") or "russia-tv.online" in link["href"]
