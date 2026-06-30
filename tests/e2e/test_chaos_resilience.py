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
    """При блокировке API сайт не должен падать с белым экраном."""
    await page.route("**/api/**", lambda route: route.abort("blockedbyclient"))

    home = HomePage(page)
    await home.goto()
    # SPA should still render layout even if API fails
    body = await page.query_selector("body")
    assert body is not None
    text = await body.inner_text() or ""
    assert len(text) > 0, "Blank page when API is blocked"


@pytest.mark.e2e
@pytest.mark.chaos
@pytest.mark.flaky
@pytest.mark.asyncio
async def test_partial_api_failure(page: Page):
    """50% API-запросов падают — UI должен быть частично функционален."""
    counter = 0

    async def handle_route(route) -> None:  # noqa: ANN001
        nonlocal counter
        counter += 1
        if counter % 2 == 0:
            await route.abort("failed")
        else:
            await route.continue_()

    await page.route("**/api/**", handle_route)

    home = HomePage(page)
    await home.goto()
    body = await page.query_selector("body")
    assert body is not None


@pytest.mark.e2e
@pytest.mark.chaos
@pytest.mark.asyncio
async def test_cdn_blocked_fallback(page: Page):
    """При блокировке CDN-статики (JS/CSS) страница должна отрисоваться."""
    await page.route("**/*.{js,css,png,jpg,jpeg,svg,woff2}", lambda route: route.abort("blockedbyclient"))

    home = HomePage(page)
    await home.goto()
    body = await page.query_selector("body")
    assert body is not None
    text = await body.inner_text() or ""
    # At minimum should show some text, not a blank broken page
    assert len(text) > 0, "Blank page when CDN assets are blocked"


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
        assert channels is not None
    finally:
        await cdp_session.send("Emulation.setCPUThrottlingRate", {"rate": 1})
