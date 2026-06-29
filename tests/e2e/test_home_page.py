"""E2E-тесты главной страницы russia-tv.online."""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage
from utils.screenshot_utils import capture_full_page


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_home_page_loads_successfully(page: Page):
    """Главная страница должна загружаться и отображать каналы."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    channels = await home.get_visible_channels()
    assert len(channels) > 0, "No channel cards found on home page"

    categories = await home.get_categories()
    assert len(categories) > 0, "No category filters found"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_has_channel_names(page: Page):
    """Главная страница должна отображать известные названия каналов."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    channels = await home.get_visible_channels()
    names = [c["name"] for c in channels]
    assert any("Первый канал" in n for n in names), f"Expected 'Первый канал' in {names}"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_search_functionality(page: Page):
    """Поиск должен принимать ввод и отправлять запрос."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    await home.search("Первый")
    await page.wait_for_timeout(2000)

    screenshot_path = await capture_full_page(page, "search_results")
    assert screenshot_path is not None


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_screenshot(page: Page):
    """Сделать скриншот главной страницы для визуальной регрессии."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    path = await capture_full_page(page, "home_page")
    assert path.endswith(".png")
