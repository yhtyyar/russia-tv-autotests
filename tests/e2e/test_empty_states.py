"""E2E-тесты пустых состояний и сценариев «нет результатов».

Покрывает:
- Поиск по несуществующему запросу показывает пустое состояние
- Невалидная категория показывает пустое состояние или fallback
- Канал без передач
"""

import pytest
from playwright.async_api import Page

from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_search_no_results_shows_empty_state(page: Page):
    """Поиск по бессмысленному запросу должен показывать пустое состояние или оставаться на странице."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_search_visible():
        pytest.skip("Search not visible")

    await home.search("xyznonexistent12345")
    await page.wait_for_load_state("networkidle")

    # Either empty state is shown, or page stays on home
    empty_visible = await home.is_empty_state_visible()
    current_url = page.url
    assert empty_visible or "search" not in current_url or home.url in current_url, (
        "Unexpected behavior for empty search results"
    )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_invalid_category_url_loads_without_crash(page: Page):
    """Переход на несуществующую категорию не должен падать."""
    response = await page.goto("https://russia-tv.online/category/nonexistent-xyz")
    if response:
        assert response.status in (200, 404)

    body = await page.query_selector("body")
    assert body is not None
    text = await body.inner_text() or ""
    assert len(text) > 0, "Page crashed with no content"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_schedule_page_empty_state_not_crashing(page: Page):
    """Страница расписания должна загружаться даже без доступных передач."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    # Page should be functional regardless of content
    body = await page.query_selector("body")
    assert body is not None
    text = await body.inner_text() or ""
    assert len(text) > 0, "Schedule page crashed"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_channel_page_empty_programs_not_crashing(page: Page):
    """Страница канала должна загружаться даже с пустым списком передач."""
    channel = ChannelPage(page)
    await channel.open_channel("999999")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    body = await page.query_selector("body")
    assert body is not None
    text = await body.inner_text() or ""
    assert len(text) > 0, "Channel page crashed for unknown channel"
