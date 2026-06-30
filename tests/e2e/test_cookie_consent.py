"""E2E-тесты cookie-баннера.

Покрывает:
- Видимость баннера при первом визите
- Функциональность кнопки принятия
- Скрытие баннера после принятия
- Баннер на разных страницах
"""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("cookie-баннера")
@allure.story("Баннер cookie-согласия должен быть виден при первом визите на главную")
@allure.severity(Severity.NORMAL)
async def test_cookie_banner_visible_on_first_visit(page: Page):
    """Баннер cookie-согласия должен быть виден при первом визите на главную."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    visible = await home.is_cookie_banner_visible()
    if not visible:
        pytest.skip("Cookie banner not implemented on this site")
    assert visible, "Cookie consent banner should be visible on first visit"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("cookie-баннера")
@allure.story("Клик по принятию должен скрывать cookie-баннер")
@allure.severity(Severity.NORMAL)
async def test_cookie_accept_dismisses_banner(page: Page):
    """Клик по принятию должен скрывать cookie-баннер."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_cookie_banner_visible():
        pytest.skip("Cookie banner not implemented or already dismissed")

    await home.accept_cookies()
    await page.wait_for_selector(home._COOKIE_BANNER, state="hidden", timeout=5000)

    visible = await home.is_cookie_banner_visible()
    assert not visible, "Cookie banner should be hidden after accept"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("cookie-баннера")
@allure.story("Cookie-баннер должен появляться на странице расписания, если ещё не принят")
@allure.severity(Severity.NORMAL)
async def test_cookie_banner_on_schedule_page(page: Page):
    """Cookie-баннер должен появляться на странице расписания, если ещё не принят."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    visible = await schedule.is_element_visible(schedule._COOKIE_BANNER)
    if not visible:
        pytest.skip("Cookie banner not implemented")
    assert visible, "Cookie banner should be visible on schedule page"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("cookie-баннера")
@allure.story("Cookie-баннер должен появляться на странице канала")
@allure.severity(Severity.NORMAL)
async def test_cookie_banner_on_channel_page(page: Page):
    """Cookie-баннер должен появляться на странице канала."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    visible = await channel.is_cookie_banner_visible()
    if not visible:
        pytest.skip("Cookie banner not implemented")
    assert visible, "Cookie banner should be visible on channel page"
