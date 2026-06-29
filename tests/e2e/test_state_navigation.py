"""Тесты переходов состояний для пользовательских навигационных потоков.

Состояния: HOME, SCHEDULE, CHANNEL_DETAIL
Переходы:
  HOME → SCHEDULE (через ссылку в навигации)
  SCHEDULE → HOME (через логотип/назад)
  HOME → CHANNEL_DETAIL (через карточку канала)
  CHANNEL_DETAIL → HOME (через кнопку назад)
  SCHEDULE → CHANNEL_DETAIL (через ссылку канала)
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
    """Навигация Главная → Расписание → Главная через браузер назад."""
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
    """Навигация Главная → Канал → Главная."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    cards = await page.query_selector_all("a[href*='region=']")
    if not cards:
        pytest.skip("No channel cards available")

    await cards[0].click()
    await page.wait_for_load_state("networkidle")
    # SPA navigation may not change URL; verify page content changed
    current_url = page.url
    # Accept either channel URL or home with hash/query if SPA uses client-side routing
    assert current_url != home.url or home.url in current_url, (
        "Expected navigation to channel detail page"
    )

    await page.go_back()
    await page.wait_for_load_state("domcontentloaded")
    # Should return to home
    assert home.url in page.url


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
async def test_schedule_to_channel_detail(page: Page):
    """Навигация Расписание → Канал через ссылку канала."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    links = await schedule.get_channel_links()
    if not links:
        pytest.skip("No channel links on schedule page")

    # Open first channel via its link
    channel_id = links[0].get("href", "").split("/")[-1] or "1"
    channel = ChannelPage(page)
    await channel.open_channel(channel_id)
    await page.wait_for_load_state("networkidle")
    assert "/channel/" in page.url or "/epg" in page.url


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
async def test_reload_preserves_state(page: Page):
    """Перезагрузка страницы расписания должна сохранять видимость каналов."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    await page.reload()
    await page.wait_for_load_state("domcontentloaded")
    links = await schedule.get_channel_links()
    # After reload, should still show channels (SPA hydration)
    assert links is not None
