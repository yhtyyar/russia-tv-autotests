"""E2E-тесты адаптивного дизайна для russia-tv.online."""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
@allure.feature("адаптивного дизайна")
@allure.story("Сайт должен корректно отображаться на мобильном вьюпорте без горизонтального ...")
@allure.severity(Severity.NORMAL)
async def test_home_page_mobile_viewport(page: Page):
    """Сайт должен корректно отображаться на мобильном вьюпорте без горизонтального скролла."""
    await page.set_viewport_size({"width": 375, "height": 667})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    channels = await home.get_visible_channels()
    assert len(channels) > 0, "No channels loaded on mobile"

    has_horizontal_scroll = await page.evaluate(
        "() => document.body.scrollWidth > window.innerWidth"
    )
    assert not has_horizontal_scroll, "Horizontal scroll detected on mobile viewport"


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
@allure.feature("адаптивного дизайна")
@allure.story("Сайт должен корректно отображаться на планшетном вьюпорте")
@allure.severity(Severity.NORMAL)
async def test_home_page_tablet_viewport(page: Page):
    """Сайт должен корректно отображаться на планшетном вьюпорте."""
    await page.set_viewport_size({"width": 768, "height": 1024})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    channels = await home.get_visible_channels()
    assert len(channels) > 0, "No channels loaded on tablet"


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
@allure.feature("адаптивного дизайна")
@allure.story("Мобильный вьюпорт не должен иметь горизонтального скролла после загрузки")
@allure.severity(Severity.NORMAL)
async def test_mobile_viewport_no_horizontal_scroll(page: Page):
    """Мобильный вьюпорт не должен иметь горизонтального скролла после загрузки."""
    await page.set_viewport_size({"width": 375, "height": 667})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    has_horizontal_scroll = await page.evaluate(
        "() => document.body.scrollWidth > window.innerWidth"
    )
    assert not has_horizontal_scroll, "Horizontal scroll detected on mobile viewport"
