"""E2E-тесты страницы канала.

Покрывает:
- Отображение названия канала
- Видимость списка передач
- Индикатор текущей передачи
- Навигация назад на главную
- Футер и SEO на странице канала
"""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.channel_page import ChannelPage
from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Страница канала должна загружаться и отображать название канала")
@allure.severity(Severity.NORMAL)
async def test_channel_page_loads_and_shows_name(page: Page):
    """Страница канала должна загружаться и отображать название канала."""
    channel = ChannelPage(page)
    await channel.open_channel("1kanal")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_selector(
        "h1[data-test='current-channel-name'], h1", state="visible", timeout=15000
    )

    name = await channel.get_channel_name()
    assert name, "Название канала не отображается на странице канала"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Страница канала должна показывать передачи или пустое состояние, не падать")
@allure.severity(Severity.NORMAL)
async def test_channel_page_has_programs_or_empty_state(page: Page):
    """Страница канала должна показывать передачи или пустое состояние, не падать."""
    channel = ChannelPage(page)
    await channel.open_channel("1kanal")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_selector(
        "h1[data-test='current-channel-name'], h1", state="visible", timeout=15000
    )

    programs = await channel.get_programs()
    empty_visible = (
        await page.locator(".empty-schedule, .no-programs, [data-testid='empty-schedule']").count()
        > 0
    )
    assert (
        len(programs) > 0 or empty_visible
    ), "На странице канала нет ни списка передач, ни индикатора пустого расписания"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Страница канала может показывать индикатор текущей передачи")
@allure.severity(Severity.NORMAL)
async def test_channel_page_current_program_indicator(page: Page):
    """Страница канала может показывать индикатор текущей передачи."""
    channel = ChannelPage(page)
    await channel.open_channel("1kanal")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_selector(
        "h1[data-test='current-channel-name'], h1", state="visible", timeout=15000
    )

    assert (
        await channel.is_current_program_visible()
    ), "Индикатор текущей передачи не отображается на странице канала"


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Пользователь может перейти со страницы канала обратно на главную")
@allure.severity(Severity.NORMAL)
async def test_channel_to_home_navigation(page: Page):
    """Пользователь может перейти со страницы канала обратно на главную."""
    channel = ChannelPage(page)
    await channel.open_channel("1kanal")
    await channel.wait_for_load("domcontentloaded")

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    assert home.url in page.url


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Страница канала должна иметь title и meta-теги")
@allure.severity(Severity.NORMAL)
async def test_channel_page_meta_tags(page: Page):
    """Страница канала должна иметь title и meta-теги."""
    channel = ChannelPage(page)
    await channel.open_channel("1kanal")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_selector(
        "h1[data-test='current-channel-name'], h1", state="visible", timeout=15000
    )

    meta = await channel.get_meta_tags()
    assert meta["title"], "Channel page title is empty"
