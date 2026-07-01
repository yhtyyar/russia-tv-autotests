"""Chaos-инжиниринг: проверка отказоустойчивости UI при сбоях сети/API.

Сценарии:
- Блокировка API-запросов (page.route → abort)
- Частичный офлайн (50% запросов падают)
- CPU throttling через CDP
- Блокировка CDN/статики
"""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.chaos
@pytest.mark.asyncio
async def test_api_blocked_graceful_fallback(page: Page):
    """При блокировке фоновых API-запросов список каналов должен остаться видимым.

    Основной список каналов рендерится на сервере (SSR), поэтому блокировка
    клиентских API-вызовов (реклама, метрики) не должна ломать контент.
    """

    async def block_api(route) -> None:
        await route.abort("blockedbyclient")

    await page.route("**/api/**", block_api)

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    channels = await home.get_visible_channels()
    assert len(channels) > 0, "Список каналов пуст при заблокированных API-запросах"


@pytest.mark.e2e
@pytest.mark.chaos
@pytest.mark.flaky
@pytest.mark.asyncio
async def test_partial_api_failure(page: Page):
    """50% API-запросов падают — UI должен быть частично функционален."""
    counter = 0

    async def handle_route(route) -> None:
        nonlocal counter
        counter += 1
        if counter % 2 == 0:
            await route.abort("failed")
        else:
            await route.continue_()

    await page.route("**/api/**", handle_route)

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    channels = await home.get_visible_channels()
    assert len(channels) > 0, "Список каналов пуст при частичном сбое API-запросов"


@pytest.mark.e2e
@pytest.mark.chaos
@pytest.mark.asyncio
async def test_cdn_blocked_fallback(page: Page):
    """При блокировке CDN-статики (JS/CSS) SSR-разметка с каналами должна остаться видимой."""
    await page.route(
        "**/*.{js,css,png,jpg,jpeg,svg,woff2}", lambda route: route.abort("blockedbyclient")
    )

    home = HomePage(page)
    await home.goto()
    channels = await home.get_visible_channels()
    assert len(channels) > 0, "Список каналов пуст при заблокированных JS/CSS/изображениях"


@pytest.mark.e2e
@pytest.mark.chaos
@pytest.mark.flaky
@pytest.mark.asyncio
async def test_cpu_throttling_does_not_crash(page: Page):
    """При CPU throttling в 4x страница не должна падать с ошибкой."""
    cdp_session = await page.context.new_cdp_session(page)
    await cdp_session.send("Emulation.setCPUThrottlingRate", {"rate": 4})
    try:
        home = HomePage(page)
        await home.goto()
        await home.expect_channels_loaded(timeout=45000)
        channels = await home.get_visible_channels()
        assert len(channels) > 0, "Список каналов пуст при 4x CPU throttling"
    finally:
        await cdp_session.send("Emulation.setCPUThrottlingRate", {"rate": 1})
