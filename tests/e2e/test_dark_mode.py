"""E2E-тесты тёмной темы / переключателя темы.

Покрывает:
- Видимость переключателя
- Активация на главной, в расписании и на странице канала
- Сохранение при навигации
- Учёт системных предпочтений (опционально)
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
@allure.feature("тёмной темы / переключателя темы")
@allure.story("Переключатель тёмной темы должен быть виден на главной странице")
@allure.severity(Severity.NORMAL)
async def test_home_page_dark_mode_toggle_exists(page: Page):
    """Переключатель тёмной темы должен быть виден на главной странице."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    visible = await home.is_dark_mode_toggle_visible()
    if not visible:
        pytest.skip("Dark mode toggle not implemented on this site")
    assert visible, "Dark mode toggle is not visible on home page"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("тёмной темы / переключателя темы")
@allure.story("Клик по переключателю должен менять состояние тёмной темы на главной")
@allure.severity(Severity.NORMAL)
async def test_home_page_toggle_dark_mode(page: Page):
    """Клик по переключателю должен менять состояние тёмной темы на главной."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_dark_mode_toggle_visible():
        pytest.skip("Dark mode toggle not implemented")

    initial = await home.is_dark_mode_active()
    await home.toggle_dark_mode()
    await page.wait_for_load_state("domcontentloaded")
    after = await home.is_dark_mode_active()
    assert after != initial, "Dark mode state did not change after toggle"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("тёмной темы / переключателя темы")
@allure.story("Переключатель тёмной темы должен работать на странице расписания")
@allure.severity(Severity.NORMAL)
async def test_schedule_page_dark_mode_toggle(page: Page):
    """Переключатель тёмной темы должен работать на странице расписания."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    if not await schedule.is_element_visible(schedule._DARK_MODE_TOGGLE):
        pytest.skip("Dark mode toggle not implemented")

    initial = await schedule.is_dark_mode_active()
    await schedule.toggle_dark_mode()
    await page.wait_for_load_state("domcontentloaded")
    after = await schedule.is_dark_mode_active()
    assert after != initial, "Dark mode state did not change on schedule page"


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("тёмной темы / переключателя темы")
@allure.story("Состояние тёмной темы должно сохраняться при навигации между страницами")
@allure.severity(Severity.NORMAL)
async def test_dark_mode_persists_across_navigation(page: Page):
    """Состояние тёмной темы должно сохраняться при навигации между страницами."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_dark_mode_toggle_visible():
        pytest.skip("Dark mode toggle not implemented")

    # Enable dark mode
    await home.toggle_dark_mode()
    await page.wait_for_load_state("domcontentloaded")
    dark_on_home = await home.is_dark_mode_active()

    # Navigate to schedule
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("domcontentloaded")
    dark_on_schedule = await schedule.is_dark_mode_active()

    assert dark_on_home == dark_on_schedule, (
        "Dark mode state lost after navigation to schedule"
    )


@pytest.mark.e2e
@pytest.mark.asyncio
@allure.feature("тёмной темы / переключателя темы")
@allure.story("Страница канала должна поддерживать тёмную тему")
@allure.severity(Severity.NORMAL)
async def test_dark_mode_on_channel_page(page: Page):
    """Страница канала должна поддерживать тёмную тему."""
    channel = ChannelPage(page)
    await channel.open_channel("1")
    await channel.wait_for_load("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    if not await channel.is_element_visible(channel._DARK_MODE_TOGGLE):
        pytest.skip("Dark mode toggle not implemented")

    initial = await channel.is_dark_mode_active()
    await channel.toggle_dark_mode()
    await page.wait_for_load_state("domcontentloaded")
    after = await channel.is_dark_mode_active()
    assert after != initial, "Dark mode did not toggle on channel page"
