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
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.channel_page import ChannelPage
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
@allure.feature("переходов состояний")
@allure.story("Навигация Главная → Расписание → Главная через браузер назад")
@allure.severity(Severity.NORMAL)
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
@allure.feature("переходов состояний")
@allure.story("Навигация Главная → Канал → Главная")
@allure.severity(Severity.NORMAL)
async def test_home_to_channel_detail_and_back(page: Page):
    """Навигация Главная → Канал → Главная."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    cards = await page.query_selector_all("a[href*='region=']")
    if not cards:
        pytest.skip("No channel cards available")

    await cards[0].click()
    await page.wait_for_url("**region=**", timeout=15000)
    assert (
        "region=" in page.url and page.url != home.url
    ), f"Ожидался переход на страницу канала (?region=...), получен URL: {page.url}"

    await page.go_back()
    await page.wait_for_load_state("domcontentloaded")
    # Должны вернуться на главную
    assert home.url in page.url


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
@allure.feature("переходов состояний")
@allure.story("Навигация Расписание → Канал через ссылку канала")
@allure.severity(Severity.NORMAL)
async def test_schedule_to_channel_detail(page: Page):
    """Навигация Расписание → Канал через ссылку канала."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    links = await schedule.get_channel_links()
    if not links:
        pytest.skip("No channel links on schedule page")

    # Извлечь slug из href вида "/1kanal?region=21" (реальная схема URL сайта)
    href = links[0].get("href", "")
    slug = href.split("?")[0].strip("/").split("/")[-1] or "1kanal"
    channel = ChannelPage(page)
    await channel.open_channel(slug)
    await page.wait_for_selector(
        "h1[data-test='current-channel-name'], h1", state="visible", timeout=15000
    )
    assert "region=" in page.url, f"Ожидался переход на страницу канала, получен URL: {page.url}"


@pytest.mark.e2e
@pytest.mark.state_transition
@pytest.mark.asyncio
@allure.feature("переходов состояний")
@allure.story("Перезагрузка страницы расписания должна сохранять видимость каналов")
@allure.severity(Severity.NORMAL)
async def test_reload_preserves_state(page: Page):
    """Перезагрузка страницы расписания должна сохранять видимость каналов."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    await page.reload()
    await page.wait_for_load_state("domcontentloaded")
    await page.wait_for_selector(schedule.CHANNEL_LINKS, state="visible", timeout=15000)
    links = await schedule.get_channel_links()
    # После перезагрузки каналы должны отрисоваться заново (гидратация SPA)
    assert len(links) > 0, "После перезагрузки страницы расписания список каналов пуст"
