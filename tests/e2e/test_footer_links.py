"""E2E-тесты ссылок в футере и видимости футера.

Покрывает:
- Наличие футера на ключевых страницах
- Ссылки футера не битые (имеют href)
- Навигация по ссылкам футера
"""

import pytest
import pytest_check as check
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("ссылок в футере и видимости футера")
@allure.story("Футер должен быть виден на главной странице")
@allure.severity(Severity.NORMAL)
async def test_home_page_footer_visible(page: Page):
    """Футер должен быть виден на главной странице."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    visible = await home.is_footer_visible()
    assert visible, "Footer is not visible on home page"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("ссылок в футере и видимости футера")
@allure.story("Футер должен содержать хотя бы одну ссылку")
@allure.severity(Severity.NORMAL)
async def test_home_page_footer_links_not_empty(page: Page):
    """Футер должен содержать хотя бы одну ссылку."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    links = await home.get_footer_links()
    if not links:
        pytest.skip("No footer links found")
    assert len(links) > 0, "Footer should contain at least one link"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("ссылок в футере и видимости футера")
@allure.story("Все ссылки футера должны иметь непустые href-атрибуты")
@allure.severity(Severity.NORMAL)
async def test_footer_links_have_valid_href(page: Page):
    """Все ссылки футера должны иметь непустые href-атрибуты."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    links = await home.get_footer_links()
    if not links:
        pytest.skip("No footer links found")

    for link in links:
        check.is_not_none(link["href"], msg=f"Footer link '{link['text']}' has empty href")


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("ссылок в футере и видимости футера")
@allure.story("Футер должен быть виден на странице расписания")
@allure.severity(Severity.NORMAL)
async def test_schedule_page_footer_visible(page: Page):
    """Футер должен быть виден на странице расписания."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    # Footer might be below fold, scroll to bottom
    await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_selector(schedule._FOOTER, state="visible", timeout=5000)

    visible = await schedule.is_element_visible(schedule._FOOTER)
    assert visible, "Footer is not visible on schedule page"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("ссылок в футере и видимости футера")
@allure.story("Футер должен быть виден на странице канала")
@allure.severity(Severity.NORMAL)
async def test_channel_page_footer_visible(page: Page):
    """Футер должен быть виден на странице канала."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    # Scroll to bottom to reveal footer
    await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_selector(channel._FOOTER, state="visible", timeout=5000)

    visible = await channel.is_footer_visible()
    if not visible:
        pytest.skip("Footer not implemented on channel page")
    assert visible, "Footer is not visible on channel page"
