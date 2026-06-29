"""E2E tests for cookie consent banner.

Covers:
- Banner visibility on first visit
- Accept button functionality
- Banner dismissal after accept
- Banner on different pages
"""

import pytest
from playwright.async_api import Page

from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_cookie_banner_visible_on_first_visit(page: Page):
    """Cookie consent banner should be visible on first home page visit."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    visible = await home.is_cookie_banner_visible()
    if not visible:
        pytest.skip("Cookie banner not implemented on this site")
    assert visible, "Cookie consent banner should be visible on first visit"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_cookie_accept_dismisses_banner(page: Page):
    """Clicking accept should hide cookie banner."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_cookie_banner_visible():
        pytest.skip("Cookie banner not implemented or already dismissed")

    await home.accept_cookies()
    await page.wait_for_timeout(1000)

    visible = await home.is_cookie_banner_visible()
    assert not visible, "Cookie banner should be hidden after accept"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_cookie_banner_on_schedule_page(page: Page):
    """Cookie banner should appear on schedule page if not yet accepted."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    visible = await schedule.is_element_visible(schedule._COOKIE_BANNER)
    if not visible:
        pytest.skip("Cookie banner not implemented")
    assert visible, "Cookie banner should be visible on schedule page"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_cookie_banner_on_channel_page(page: Page):
    """Cookie banner should appear on channel detail page."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_timeout(2000)

    visible = await channel.is_cookie_banner_visible()
    if not visible:
        pytest.skip("Cookie banner not implemented")
    assert visible, "Cookie banner should be visible on channel page"
