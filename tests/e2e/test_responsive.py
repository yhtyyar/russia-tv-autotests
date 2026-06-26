"""E2E responsive design tests for russia-tv.online."""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
async def test_home_page_mobile_viewport(page: Page):
    """Site should render correctly on mobile viewport without horizontal scroll."""
    await page.set_viewport_size({"width": 375, "height": 667})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    channels = await home.get_visible_channels()
    assert len(channels) > 0, "No channels loaded on mobile"

    has_horizontal_scroll = await page.evaluate(
        "() => document.body.scrollWidth > window.innerWidth"
    )
    assert not has_horizontal_scroll, "Horizontal scroll detected on mobile viewport"


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
async def test_home_page_tablet_viewport(page: Page):
    """Site should render correctly on tablet viewport."""
    await page.set_viewport_size({"width": 768, "height": 1024})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    channels = await home.get_visible_channels()
    assert len(channels) > 0, "No channels loaded on tablet"


@pytest.mark.e2e
@pytest.mark.responsive
@pytest.mark.asyncio
async def test_mobile_viewport_no_horizontal_scroll(page: Page):
    """Mobile viewport should not have horizontal scroll after loading."""
    await page.set_viewport_size({"width": 375, "height": 667})

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    has_horizontal_scroll = await page.evaluate(
        "() => document.body.scrollWidth > window.innerWidth"
    )
    assert not has_horizontal_scroll, "Horizontal scroll detected on mobile viewport"
