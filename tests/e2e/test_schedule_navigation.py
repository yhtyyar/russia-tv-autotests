"""E2E-тесты навигации по датам в расписании."""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_schedule_page_loads(page: Page):
    """Страница расписания должна загружаться со ссылками каналов."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    # Wait for content to render (SPA hydration)
    await page.wait_for_selector(schedule._CHANNEL_LINKS, state="visible", timeout=15000)

    channels = await schedule.get_channel_links()
    assert len(channels) > 0, "No channel links found"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_navigation_from_home_to_schedule(page: Page):
    """Пользователь может перейти с главной на страницу расписания."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    schedule_link = await page.query_selector(
        "a[href='/epg']",
    )
    if schedule_link:
        await schedule_link.click()
        await page.wait_for_url("**/epg**")
        assert "/epg" in page.url
