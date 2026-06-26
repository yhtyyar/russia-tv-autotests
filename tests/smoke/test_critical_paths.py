"""Smoke tests for critical user paths on russia-tv.online.

These tests validate that the site is functional at a high level.
They are designed to run fast (< 2 minutes total) and be used
as a sanity check before deeper regression runs.
"""

import httpx
import pytest
from playwright.async_api import Page

from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_site_responds_200():
    """Home page must return HTTP 200."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/")
        assert response.status_code == 200


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_home_page_loads_channels(page: Page):
    """Home page must load and display channel cards."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    channels = await home.get_visible_channels()
    assert len(channels) > 0, "No channels rendered on home page"


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_schedule_page_loads(page: Page):
    """Schedule (/epg) page must load without errors."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")
    assert schedule.url in page.url


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_search_input_exists(page: Page):
    """Search input must be present and interactable on home page."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    visible = await home.is_search_visible()
    assert visible, "Search input is not visible"
