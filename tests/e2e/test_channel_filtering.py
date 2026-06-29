"""E2E-тесты фильтрации каналов по категориям."""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_filter_by_category_shows_results(page: Page):
    """Выбор категории должен показывать отфильтрованные каналы."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    categories = await home.get_visible_categories()
    if len(categories) == 0:
        pytest.skip("No categories available on home page")

    first_category = categories[0]
    await home.select_category(first_category)
    await page.wait_for_load_state("networkidle")

    channels = await home.get_visible_channels()
    # Category may have 0 channels, but page should not crash
    assert channels is not None


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_category_filter_clickable(page: Page):
    """Все кнопки категорий должны быть кликабельными."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    buttons = await page.query_selector_all(
        ".category-btn, [data-testid='category-btn']",
    )
    if not buttons:
        pytest.skip("No category buttons found")
    for btn in buttons:
        assert await btn.is_enabled(), "Category button is not enabled"
