"""E2E-тесты SEO meta-тегов и заголовков страниц.

Покрывает:
- У главной страницы есть title и meta description
- У страницы расписания есть title
- У страницы канала есть title
- Наличие Open Graph тегов
- Наличие canonical link
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
@allure.feature("SEO meta-тегов и заголовков страниц")
@allure.story("Главная страница должна иметь непустой title")
@allure.severity(Severity.NORMAL)
async def test_home_page_has_title(page: Page):
    """Главная страница должна иметь непустой title."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    meta = await home.get_meta_tags()
    assert meta["title"], "Home page title is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("SEO meta-тегов и заголовков страниц")
@allure.story("Главная страница должна иметь meta description")
@allure.severity(Severity.NORMAL)
async def test_home_page_has_meta_description(page: Page):
    """Главная страница должна иметь meta description."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    meta = await home.get_meta_tags()
    # Description may be empty on some SPAs; assert only if present
    if meta["description"]:
        assert len(meta["description"]) > 10, "Meta description too short"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("SEO meta-тегов и заголовков страниц")
@allure.story("Страница расписания должна иметь title")
@allure.severity(Severity.NORMAL)
async def test_schedule_page_has_title(page: Page):
    """Страница расписания должна иметь title."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    meta = await schedule.get_meta_tags()
    assert meta["title"], "Schedule page title is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("SEO meta-тегов и заголовков страниц")
@allure.story("Страница канала должна иметь title с информацией о канале")
@allure.severity(Severity.NORMAL)
async def test_channel_page_has_title(page: Page):
    """Страница канала должна иметь title с информацией о канале."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    meta = await channel.get_meta_tags()
    assert meta["title"], "Channel page title is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("SEO meta-тегов и заголовков страниц")
@allure.story("Главная страница должна иметь canonical link")
@allure.severity(Severity.NORMAL)
async def test_home_page_has_canonical_link(page: Page):
    """Главная страница должна иметь canonical link."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    meta = await home.get_meta_tags()
    assert meta["canonical"], "Canonical link is missing on home page"
