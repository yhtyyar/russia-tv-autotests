"""E2E-тесты пустых состояний и сценариев «нет результатов».

Покрывает:
- Поиск по несуществующему запросу показывает пустое состояние
- Невалидная категория показывает пустое состояние или fallback
- Канал без передач
"""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("пустых состояний и сценариев «нет результатов»")
@allure.story("Поиск по бессмысленному запросу должен показывать пустое состояние или остава...")
@allure.severity(Severity.NORMAL)
async def test_search_no_results_shows_empty_state(page: Page):
    """Поиск по бессмысленному запросу должен показывать пустое состояние или оставаться на странице."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_search_visible():
        pytest.skip("Search not visible")

    await home.search("xyznonexistent12345")
    await page.wait_for_selector(home.EMPTY_STATE, state="visible", timeout=10000)
    assert (
        await home.is_empty_state_visible()
    ), "Индикатор пустого результата поиска не отображается для несуществующего запроса"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("пустых состояний и сценариев «нет результатов»")
@allure.story("Переход на несуществующую категорию не должен падать")
@allure.severity(Severity.NORMAL)
async def test_invalid_category_url_loads_without_crash(page: Page):
    """Переход на несуществующую категорию не должен падать."""
    response = await page.goto("https://russia-tv.online/category/nonexistent-xyz")
    assert response is not None and response.status in (200, 404)

    text = await page.locator("body").inner_text()
    assert (
        "не найдена" in text.lower() or "404" in text
    ), f"Ожидалась страница 404 для несуществующей категории, получено: {text[:200]!r}"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("пустых состояний и сценариев «нет результатов»")
@allure.story("Страница расписания должна загружаться даже без доступных передач")
@allure.severity(Severity.NORMAL)
async def test_schedule_page_empty_state_not_crashing(page: Page):
    """Страница расписания должна загружаться даже без доступных передач."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    programs = await schedule.get_programs()
    empty_visible = await schedule.is_empty_schedule_visible()
    channels = await schedule.get_channel_links()
    assert programs or empty_visible or channels, (
        "Страница расписания не показывает ни передачи, ни каналы, "
        "ни индикатор пустого состояния"
    )


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("пустых состояний и сценариев «нет результатов»")
@allure.story("Страница канала должна загружаться даже с пустым списком передач")
@allure.severity(Severity.NORMAL)
async def test_channel_page_empty_programs_not_crashing(page: Page):
    """Страница канала должна загружаться даже с пустым списком передач."""
    channel = ChannelPage(page)
    await channel.open_channel("999999")
    await channel.wait_for_load("domcontentloaded")

    text = await page.locator("body").inner_text()
    assert (
        "не найдена" in text.lower() or "404" in text
    ), f"Ожидалась страница 404 для несуществующего канала, получен текст: {text[:200]!r}"
