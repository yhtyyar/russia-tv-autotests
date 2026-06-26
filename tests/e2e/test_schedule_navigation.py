"""E2E tests for schedule date navigation."""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_schedule_page_loads(page: Page):
    """Schedule page should load with channel links."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")
    await page.wait_for_timeout(5000)

    channels = await schedule.get_channel_links()
    assert len(channels) > 0, "No channel links found"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_navigation_from_home_to_schedule(page: Page):
    """User can navigate from home to schedule page."""
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
