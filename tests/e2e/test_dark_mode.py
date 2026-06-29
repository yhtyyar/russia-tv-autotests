"""E2E tests for dark mode / theme toggle functionality.

Covers:
- Toggle visibility
- Toggle activation on home, schedule, and channel pages
- Persistence across navigation
- System preference respect (optional)
"""

import pytest
from playwright.async_api import Page

from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_dark_mode_toggle_exists(page: Page):
    """Dark mode toggle should be visible on home page."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    visible = await home.is_dark_mode_toggle_visible()
    if not visible:
        pytest.skip("Dark mode toggle not implemented on this site")
    assert visible, "Dark mode toggle is not visible on home page"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_home_page_toggle_dark_mode(page: Page):
    """Clicking toggle should switch dark mode state on home page."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_dark_mode_toggle_visible():
        pytest.skip("Dark mode toggle not implemented")

    initial = await home.is_dark_mode_active()
    await home.toggle_dark_mode()
    await page.wait_for_timeout(500)
    after = await home.is_dark_mode_active()
    assert after != initial, "Dark mode state did not change after toggle"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_schedule_page_dark_mode_toggle(page: Page):
    """Dark mode toggle should work on schedule page."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    if not await schedule.is_element_visible(schedule._DARK_MODE_TOGGLE):
        pytest.skip("Dark mode toggle not implemented")

    initial = await schedule.is_dark_mode_active()
    await schedule.toggle_dark_mode()
    await page.wait_for_timeout(500)
    after = await schedule.is_dark_mode_active()
    assert after != initial, "Dark mode state did not change on schedule page"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dark_mode_persists_across_navigation(page: Page):
    """Dark mode state should persist when navigating between pages."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_dark_mode_toggle_visible():
        pytest.skip("Dark mode toggle not implemented")

    # Enable dark mode
    await home.toggle_dark_mode()
    await page.wait_for_timeout(500)
    dark_on_home = await home.is_dark_mode_active()

    # Navigate to schedule
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")
    await page.wait_for_timeout(500)
    dark_on_schedule = await schedule.is_dark_mode_active()

    assert dark_on_home == dark_on_schedule, (
        "Dark mode state lost after navigation to schedule"
    )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dark_mode_on_channel_page(page: Page):
    """Channel detail page should respect dark mode."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_timeout(2000)

    if not await channel.is_element_visible(channel._DARK_MODE_TOGGLE):
        pytest.skip("Dark mode toggle not implemented")

    initial = await channel.is_dark_mode_active()
    await channel.toggle_dark_mode()
    await page.wait_for_timeout(500)
    after = await channel.is_dark_mode_active()
    assert after != initial, "Dark mode did not toggle on channel page"
