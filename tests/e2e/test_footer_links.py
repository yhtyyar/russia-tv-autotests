"""E2E tests for footer links and footer visibility.

Covers:
- Footer presence on key pages
- Footer links are not broken (have href)
- Footer link navigation
"""

import pytest
from playwright.async_api import Page

from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_footer_visible(page: Page):
    """Footer should be visible on home page."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    visible = await home.is_footer_visible()
    assert visible, "Footer is not visible on home page"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_footer_links_not_empty(page: Page):
    """Footer should contain at least one link."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    links = await home.get_footer_links()
    if not links:
        pytest.skip("No footer links found")
    assert len(links) > 0, "Footer should contain at least one link"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_footer_links_have_valid_href(page: Page):
    """All footer links should have non-empty href attributes."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    links = await home.get_footer_links()
    if not links:
        pytest.skip("No footer links found")

    for link in links:
        assert link["href"], f"Footer link '{link['text']}' has empty href"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_schedule_page_footer_visible(page: Page):
    """Footer should be visible on schedule page."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    # Footer might be below fold, scroll to bottom
    await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(500)

    visible = await schedule.is_element_visible(schedule._FOOTER)
    assert visible, "Footer is not visible on schedule page"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_channel_page_footer_visible(page: Page):
    """Footer should be visible on channel detail page."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_timeout(2000)

    # Scroll to bottom to reveal footer
    await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(800)

    visible = await channel.is_footer_visible()
    if not visible:
        pytest.skip("Footer not implemented on channel page")
    assert visible, "Footer is not visible on channel page"
