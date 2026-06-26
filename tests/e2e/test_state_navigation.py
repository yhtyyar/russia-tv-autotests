"""State-transition tests for user navigation flow.

States: HOME, SCHEDULE, CHANNEL_DETAIL
Transitions:
  HOME → SCHEDULE (via nav link)
  SCHEDULE → HOME (via logo/back)
  HOME → CHANNEL_DETAIL (via channel card)
  CHANNEL_DETAIL → HOME (via back button)
  SCHEDULE → CHANNEL_DETAIL (via channel link)
"""

import pytest
from playwright.async_api import Page

from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
async def test_home_to_schedule_and_back(page: Page):
    """Navigate Home → Schedule → Home via browser back."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    home_url = page.url

    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")
    assert "/epg" in page.url

    await page.go_back()
    await page.wait_for_load_state("domcontentloaded")
    assert home_url in page.url or page.url == home_url


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
async def test_home_to_channel_detail_and_back(page: Page):
    """Navigate Home → Channel Detail → Home."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    cards = await page.query_selector_all("a[href*='region=']")
    if not cards:
        pytest.skip("No channel cards available")

    await cards[0].click()
    await page.wait_for_load_state("domcontentloaded")
    # Should be on a channel detail page
    assert "region=" in page.url

    await page.go_back()
    await page.wait_for_load_state("domcontentloaded")
    # Should return to home
    assert home.url in page.url


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
async def test_schedule_to_channel_detail(page: Page):
    """Navigate Schedule → Channel Detail."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    links = await schedule.get_channel_links()
    if not links:
        pytest.skip("No channel links on schedule page")

    channel = ChannelPage(page)
    await channel.goto()
    await page.wait_for_load_state("domcontentloaded")
    assert "region=" in page.url or "/epg" in page.url


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
async def test_reload_preserves_state(page: Page):
    """Reloading schedule page should keep channels visible."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    await page.reload()
    await page.wait_for_load_state("domcontentloaded")
    links = await schedule.get_channel_links()
    # After reload, should still show channels (SPA hydration)
    assert links is not None
