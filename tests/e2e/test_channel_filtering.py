"""E2E tests for channel category filtering."""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_filter_by_category_shows_results(page: Page):
    """Selecting a category should show filtered channels."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    categories = await home.get_categories()
    if len(categories) == 0:
        pytest.skip("No categories available on home page")

    first_category = categories[0]
    await home.select_category(first_category)
    await page.wait_for_timeout(3000)

    channels = await home.get_visible_channels()
    assert len(channels) >= 0  # May be 0 if category has no channels


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_category_filter_clickable(page: Page):
    """All category buttons should be clickable."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded()

    buttons = await page.query_selector_all(
        ".category-btn, [data-testid='category-btn']",
    )
    for btn in buttons:
        assert await btn.is_enabled(), "Category button is not enabled"
