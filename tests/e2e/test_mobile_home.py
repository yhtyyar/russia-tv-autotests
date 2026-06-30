"""E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro).

Покрытие на основе реального анализа DOM russia-tv.online (mobile viewport 390×844):
- Загрузка и viewport
- Header: логотип, поиск (aria-label='Поиск по каналам'), меню (aria-label='Открыть меню')
- Поиск: overlay с input (aria-label='Поиск по каналам')
- Бургер-меню: переключатель aria-label меняется на 'Закрыть меню'
- Категории: horizontal-scroll (Популярное, Все, Эфирные, Фильмы, Детям, Музыка, Развлечения)
- Карточки каналов: ссылки вида /{slug}?region=21
- Cookie: кнопка 'Принять куки'
- 'Загрузить еще...' — подгрузка каналов
- Футер: ссылки (включая внешние на appmetrica.yandex.com, t.me)
"""

import pytest
from playwright.async_api import Page, expect

from pages.home_page import HomePage
import allure
from allure_commons.types import Severity


@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileHomePage:
    """Критические сценарии на мобильном viewport (390×844)."""

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Главная страница корректно загружается на мобильном устройстве")
@allure.severity(Severity.NORMAL)
    async def test_mobile_home_loads(self, mobile_page: Page) -> None:
        """Главная страница корректно загружается на мобильном устройстве."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()
        assert await home.is_footer_visible()

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Header содержит логотип, кнопку поиска и бургер-меню на mobile")
@allure.severity(Severity.NORMAL)
    async def test_mobile_header_elements(self, mobile_page: Page) -> None:
        """Header содержит логотип, кнопку поиска и бургер-меню на mobile."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()
        # Даём время на полную инициализацию JS (Nuxt загружает кнопки динамически)
        await mobile_page.wait_for_timeout(3000)

        header = mobile_page.locator("header")
        await expect(header).to_be_visible()

        logo = mobile_page.locator("header a[href='/']")
        await expect(logo).to_be_visible()

        # Кнопки загружаются динамически — проверяем через expect с таймаутом
        search_btn = mobile_page.locator("button[aria-label='Поиск по каналам']")
        await expect(search_btn).to_be_visible(timeout=10000)

        menu_btn = mobile_page.locator("button[aria-label='Открыть меню']")
        await expect(menu_btn).to_be_visible(timeout=10000)

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Поисковый overlay: открытие, ввод, результаты, закрытие")
@allure.severity(Severity.NORMAL)
    async def test_mobile_search_overlay(self, mobile_page: Page) -> None:
        """Поисковый overlay: открытие, ввод, результаты, закрытие."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        # Открыть overlay поиска
        await home.open_mobile_search()
        assert await home.is_mobile_search_overlay_visible()

        # Ввести запрос в overlay-поле
        search_input = mobile_page.locator(
            "input[aria-label='Поиск по каналам']"
        )
        await expect(search_input).to_be_visible()
        await search_input.fill("Первый")
        await mobile_page.keyboard.press("Enter")
        # networkidle не наступает из-за фоновых запросов метрик/рекламы
        await mobile_page.wait_for_timeout(3000)

        # Проверить результаты
        results = await home.get_visible_channels()
        assert len(results) > 0, "Результаты поиска не отображаются на мобильном"

        # Закрыть overlay
        await home.close_mobile_search()

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Бургер-меню: открытие меняет aria-label кнопки на 'Закрыть меню'")
@allure.severity(Severity.NORMAL)
    async def test_mobile_burger_menu(self, mobile_page: Page) -> None:
        """Бургер-меню: открытие меняет aria-label кнопки на 'Закрыть меню'."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        await home.open_burger_menu()

        # После открытия кнопка меню должна иметь aria-label 'Закрыть меню'
        close_btn = mobile_page.locator("button[aria-label='Закрыть меню']")
        await expect(close_btn).to_be_visible()

        await home.close_burger_menu()
        # После закрытия снова доступна кнопка 'Открыть меню'
        open_btn = mobile_page.locator("button[aria-label='Открыть меню']")
        await expect(open_btn).to_be_visible()

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Категории каналов отображаются на мобильном")
@allure.severity(Severity.NORMAL)
    async def test_mobile_categories(self, mobile_page: Page) -> None:
        """Категории каналов отображаются на мобильном."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        names = await home.get_category_names()
        expected = {"Популярное", "Все", "Эфирные", "Фильмы", "Детям", "Музыка", "Развлечения"}
        found = set(names)
        assert expected & found, f"Категории не найдены: ожидались {expected}, получено {found}"

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Карточки каналов видны на мобильном в вертикальном списке")
@allure.severity(Severity.NORMAL)
    async def test_mobile_channel_cards_visible(self, mobile_page: Page) -> None:
        """Карточки каналов видны на мобильном в вертикальном списке."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        channels = await home.get_visible_channels()
        assert len(channels) > 0, "Карточки каналов не отображаются на мобильном"
        for ch in channels[:3]:
            assert ch["name"], f"Канал без названия: {ch}"

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Клик по карточке канала переходит на страницу канала")
@allure.severity(Severity.NORMAL)
    async def test_mobile_click_channel(self, mobile_page: Page) -> None:
        """Клик по карточке канала переходит на страницу канала."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        # Используем Page Object метод с tap + задержкой для SPA навигации
        await home.click_first_channel()

        # Проверяем, что URL изменился на страницу канала (содержит region=)
        assert "region=" in mobile_page.url
        # Проверяем наличие заголовка на странице канала
        h1 = mobile_page.locator("h1")
        await expect(h1).to_be_visible(timeout=15000)

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Cookie-баннер с кнопкой 'Принять куки' отображается на mobile")
@allure.severity(Severity.NORMAL)
    async def test_mobile_cookie_banner(self, mobile_page: Page) -> None:
        """Cookie-баннер с кнопкой 'Принять куки' отображается на mobile."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        cookie_btn = mobile_page.locator("button[aria-label='Принять куки']")
        await expect(cookie_btn).to_be_visible()

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Кнопка 'Загрузить еще...' подгружает дополнительные каналы")
@allure.severity(Severity.NORMAL)
    async def test_mobile_load_more(self, mobile_page: Page) -> None:
        """Кнопка 'Загрузить еще...' подгружает дополнительные каналы."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        load_more = mobile_page.locator("button:has-text('Загрузить еще')")
        if await load_more.count() > 0 and await load_more.is_visible():
            initial = len(await home.get_visible_channels())
            await load_more.click()
            await mobile_page.wait_for_timeout(2000)
            current = len(await home.get_visible_channels())
            assert current > initial, "Количество каналов не увеличилось после 'Загрузить еще'"
        else:
            pytest.skip("Кнопка 'Загрузить еще' не найдена на странице")

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Футер содержит валидные ссылки на мобильном (включая внешние)")
@allure.severity(Severity.NORMAL)
    async def test_mobile_footer_links(self, mobile_page: Page) -> None:
        """Футер содержит валидные ссылки на мобильном (включая внешние)."""
        home = HomePage(mobile_page)
        await home.goto()
        assert await home.is_footer_visible()
        links = await home.get_footer_links()
        assert len(links) > 0
        for link in links:
            href = link["href"]
            # Допускаем внешние ссылки (appmetrica, t.me) и внутренние
            assert href.startswith("/") or "http" in href or "russia-tv.online" in href

@allure.feature("E2E тесты главной страницы на мобильном устройстве (iPhone 14 Pro)")
@allure.story("Скролл до футера работает корректно на мобильном")
@allure.severity(Severity.NORMAL)
    async def test_mobile_scroll_to_footer(self, mobile_page: Page) -> None:
        """Скролл до футера работает корректно на мобильном."""
        home = HomePage(mobile_page)
        await home.goto()
        await home.expect_channels_loaded()

        footer = mobile_page.locator("footer")
        await footer.scroll_into_view_if_needed()
        await expect(footer).to_be_visible()
