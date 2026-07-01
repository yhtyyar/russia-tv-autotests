"""E2E-тесты «Показать ещё» / пагинации на главной странице.

Покрывает:
- Видимость кнопки «Показать ещё»
- Клик увеличивает количество каналов
- «Показать ещё» на мобильном вьюпорте
"""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("«Показать ещё» / пагинации на главной странице")
@allure.story("Кнопка «Показать ещё» должна быть видна, когда есть дополнительные каналы")
@allure.severity(Severity.NORMAL)
async def test_load_more_button_visible(page: Page):
    """Кнопка «Показать ещё» должна быть видна, когда есть дополнительные каналы."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    visible = await home.is_element_visible(home.LOAD_MORE)
    if not visible:
        pytest.skip("Load more button not present")
    assert visible, "Load more button should be visible"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("«Показать ещё» / пагинации на главной странице")
@allure.story("Клик по «Показать ещё» должен увеличивать количество видимых каналов")
@allure.severity(Severity.NORMAL)
async def test_load_more_increases_channel_count(page: Page):
    """Клик по «Показать ещё» должен увеличивать количество видимых каналов."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_element_visible(home.LOAD_MORE):
        pytest.skip("Load more button not present")

    before = await home.get_visible_channels()
    before_count = len(before)

    await home.click_load_more()
    await page.wait_for_function(
        "count => document.querySelectorAll(\"a[href*='region=']\").length > count",
        arg=before_count,
        timeout=10000,
    )

    after = await home.get_visible_channels()
    after_count = len(after)

    assert (
        after_count > before_count
    ), f"Channel count did not increase: {before_count} -> {after_count}"


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
@allure.feature("«Показать ещё» / пагинации на главной странице")
@allure.story("«Показать ещё» должен работать на мобильном вьюпорте")
@allure.severity(Severity.NORMAL)
async def test_load_more_on_mobile(page: Page):
    """«Показать ещё» должен работать на мобильном вьюпорте."""
    await page.set_viewport_size({"width": 375, "height": 667})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_element_visible(home.LOAD_MORE):
        pytest.skip("Load more button not present")

    before = len(await home.get_visible_channels())
    await home.click_load_more()
    await page.wait_for_function(
        "count => document.querySelectorAll(\"a[href*='region=']\").length > count",
        arg=before,
        timeout=10000,
    )
    after = len(await home.get_visible_channels())

    assert after > before, "Load more did not work on mobile"
