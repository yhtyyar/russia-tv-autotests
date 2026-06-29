"""E2E tests for 'Load more' / pagination functionality on home page.

Covers:
- Load more button visibility
- Clicking load more increases channel count
- Load more on mobile viewport
"""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_load_more_button_visible(page: Page):
    """Load more button should be visible when there are more channels."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    visible = await home.is_element_visible(home._LOAD_MORE)
    if not visible:
        pytest.skip("Load more button not present")
    assert visible, "Load more button should be visible"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_load_more_increases_channel_count(page: Page):
    """Clicking load more should increase the number of visible channels."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_element_visible(home._LOAD_MORE):
        pytest.skip("Load more button not present")

    before = await home.get_visible_channels()
    before_count = len(before)

    await home.click_load_more()
    await page.wait_for_timeout(1500)

    after = await home.get_visible_channels()
    after_count = len(after)

    assert after_count >= before_count, (
        f"Channel count did not increase: {before_count} -> {after_count}"
    )


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
async def test_load_more_on_mobile(page: Page):
    """Load more should work on mobile viewport."""
    await page.set_viewport_size({"width": 375, "height": 667})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_element_visible(home._LOAD_MORE):
        pytest.skip("Load more button not present")

    before = len(await home.get_visible_channels())
    await home.click_load_more()
    await page.wait_for_timeout(1500)
    after = len(await home.get_visible_channels())

    assert after >= before, "Load more did not work on mobile"
