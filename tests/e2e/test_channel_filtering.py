"""E2E-тесты фильтрации каналов по категориям."""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("фильтрации каналов по категориям")
@allure.story("Выбор категории должен показывать отфильтрованный список каналов")
@allure.severity(Severity.NORMAL)
async def test_filter_by_category_shows_results(page: Page):
    """Выбор категории 'Спорт' должен показывать только каналы этой категории."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    categories = await home.get_visible_categories()
    assert len(categories) > 0, "На главной странице не найдено ни одной категории"
    assert "Спорт" in categories, f"Ожидалась категория 'Спорт', получено: {categories}"

    before = await home.get_visible_channels()

    await home.select_category("Спорт")
    await page.wait_for_timeout(1000)

    after = await home.get_visible_channels()
    assert len(after) > 0, "После выбора категории 'Спорт' список каналов пуст"
    assert len(after) < len(
        before
    ), f"Выбор категории не отфильтровал список: было {len(before)}, стало {len(after)}"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("фильтрации каналов по категориям")
@allure.story("Все кнопки категорий должны быть кликабельными")
@allure.severity(Severity.NORMAL)
async def test_category_filter_clickable(page: Page):
    """Все кнопки категорий должны быть кликабельными."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    buttons = await page.locator("li[data-test='category-button']").all()
    assert len(buttons) > 0, "Кнопки категорий не найдены на странице"
    for btn in buttons:
        assert await btn.is_enabled(), "Кнопка категории не активна (disabled)"
