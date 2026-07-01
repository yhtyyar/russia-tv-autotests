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

    assert (
        await home.is_cookie_banner_visible()
    ), "Cookie-баннер не отображается при первом визите на главную"


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

    assert await home.is_cookie_banner_visible(), "Cookie-баннер должен быть виден перед принятием"

    await home.accept_cookies()
    await page.wait_for_selector(home.COOKIE_BANNER, state="hidden", timeout=5000)

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

    assert (
        await schedule.is_cookie_banner_visible()
    ), "Cookie-баннер не отображается на странице расписания"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("cookie-баннера")
@allure.story("Cookie-баннер должен появляться на странице канала")
@allure.severity(Severity.NORMAL)
async def test_cookie_banner_on_channel_page(page: Page):
    """Cookie-баннер должен появляться на странице канала."""
    channel = ChannelPage(page)
    await channel.open_channel("1kanal")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_selector(
        "h1[data-test='current-channel-name'], h1", state="visible", timeout=15000
    )

    assert (
        await channel.is_cookie_banner_visible()
    ), "Cookie-баннер не отображается на странице канала"
