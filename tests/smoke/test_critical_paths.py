"""Smoke-тесты критических пользовательских путей на russia-tv.online.

Эти тесты проверяют работоспособность сайта на высоком уровне.
Они рассчитаны на быстрый запуск (< 2 минуты суммарно) и используются
как sanity-check перед глубокой регрессией.
"""

import httpx
import pytest
from playwright.async_api import Page

from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_site_responds_200():
    """Главная страница должна возвращать HTTP 200."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/")
        assert response.status_code == 200


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_home_page_loads_channels(page: Page):
    """Главная страница должна загружаться и отображать карточки каналов."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    channels = await home.get_visible_channels()
    assert len(channels) > 0, "No channels rendered on home page"


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_schedule_page_loads(page: Page):
    """Страница расписания (/epg) должна загружаться без ошибок."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")
    assert schedule.url in page.url


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_search_input_exists(page: Page):
    """Поле поиска должно присутствовать и быть интерактивным на главной."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    visible = await home.is_search_visible()
    assert visible, "Search input is not visible"
