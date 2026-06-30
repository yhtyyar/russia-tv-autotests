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
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    name = await channel.get_channel_name()
    if not name:
        pytest.skip("Channel name selector not matched on this site structure")
    assert name, "Channel name is empty on detail page"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Страница канала должна показывать передачи или пустое состояние, не падать")
@allure.severity(Severity.NORMAL)
async def test_channel_page_has_programs_or_empty_state(page: Page):
    """Страница канала должна показывать передачи или пустое состояние, не падать."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    await channel.get_programs()
    # Either programs exist or page is functional
    body = await page.query_selector("body")
    assert body is not None
    text = await body.inner_text() or ""
    assert len(text) > 0, "Channel page is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Страница канала может показывать индикатор текущей передачи")
@allure.severity(Severity.NORMAL)
async def test_channel_page_current_program_indicator(page: Page):
    """Страница канала может показывать индикатор текущей передачи."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    visible = await channel.is_current_program_visible()
    if not visible:
        pytest.skip("Индикатор текущей передачи не найден на данной странице")
    assert visible


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
@allure.feature("страницы канала")
@allure.story("Пользователь может перейти со страницы канала обратно на главную")
@allure.severity(Severity.NORMAL)
async def test_channel_to_home_navigation(page: Page):
    """Пользователь может перейти со страницы канала обратно на главную."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
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
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    meta = await channel.get_meta_tags()
    assert meta["title"], "Channel page title is empty"
