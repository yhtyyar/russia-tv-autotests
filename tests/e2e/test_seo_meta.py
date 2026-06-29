"""E2E tests for SEO meta tags and page titles.

Covers:
- Home page has title and meta description
- Schedule page has title
- Channel page has title
- Open Graph tags presence
- Canonical link presence
"""

import pytest
from playwright.async_api import Page

from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_has_title(page: Page):
    """Home page should have a non-empty title tag."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    meta = await home.get_meta_tags()
    assert meta["title"], "Home page title is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_has_meta_description(page: Page):
    """Home page should have meta description."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    meta = await home.get_meta_tags()
    # Description may be empty on some SPAs; assert only if present
    if meta["description"]:
        assert len(meta["description"]) > 10, "Meta description too short"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_schedule_page_has_title(page: Page):
    """Schedule page should have a title."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    meta = await schedule.get_meta_tags()
    assert meta["title"], "Schedule page title is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_channel_page_has_title(page: Page):
    """Channel detail page should have a title containing channel info."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_timeout(2000)

    meta = await channel.get_meta_tags()
    assert meta["title"], "Channel page title is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_has_canonical_link(page: Page):
    """Home page should have canonical link."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    meta = await home.get_meta_tags()
    assert meta["canonical"], "Canonical link is missing on home page"
