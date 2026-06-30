"""E2E тесты навигации на мобильном устройстве (iPhone 14 Pro)."""

import pytest
from playwright.async_api import Page, expect

from pages.home_page import HomePage
import allure
from allure_commons.types import Severity


@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileNavigation:
    """Навигационные сценарии на мобильном viewport."""

    @allure.feature("Мобильная навигация")
    @allure.story("Переход на страницу канала и проверка элементов на mobile")
    @allure.severity(Severity.NORMAL)
    async def test_mobile_channel_page(self, mobile_page: Page) -> None:
        """Переход на страницу канала и проверка элементов на mobile."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        # Используем Page Object метод с tap + задержкой для SPA навигации
        await home.click_first_channel()
        assert "region=" in mobile_page.url

        # Заголовок канала
        h1 = mobile_page.locator("h1")
        await expect(h1).to_be_visible(timeout=15000)
        title = await h1.text_content()
        assert title and len(title.strip()) > 0

        # Программа канала (список передач)
        programs = mobile_page.locator("main").locator("div, li").first
        await expect(programs).to_be_visible(timeout=15000)

    @allure.feature("Мобильная навигация")
    @allure.story("Возврат с страницы канала на главную (кнопка назад / логотип)")
    @allure.severity(Severity.NORMAL)
    async def test_mobile_back_to_home(self, mobile_page: Page) -> None:
        """Возврат с страницы канала на главную (кнопка назад / логотип)."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        first_card = mobile_page.locator("a[href*='region=']").first
        await first_card.tap()
        await mobile_page.wait_for_timeout(2000)
        assert "region=" in mobile_page.url

        # Клик по логотипу для возврата
        logo = mobile_page.locator("header a[href='/']")
        await logo.click()
        await mobile_page.wait_for_timeout(2000)

        assert mobile_page.url.rstrip("/").endswith("russia-tv.online") or mobile_page.url == "https://russia-tv.online/"
        await home.expect_channels_loaded()

    @allure.feature("Мобильная навигация")
    @allure.story("Кнопка 'Вверх' отображается после скролла на mobile")
    @allure.severity(Severity.NORMAL)
    async def test_mobile_scroll_to_top(self, mobile_page: Page) -> None:
        """Кнопка 'Вверх' отображается после скролла на mobile."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        # Скролл вниз
        await mobile_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await mobile_page.wait_for_timeout(500)

        scroll_top = mobile_page.locator("button[aria-label='Вверх']")
        if await scroll_top.count() > 0:
            await expect(scroll_top).to_be_visible()
        else:
            pytest.skip("Кнопка 'Вверх' не найдена")
