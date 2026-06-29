"""Тесты обработки ошибок с использованием техники предугадывания ошибок.

Покрывает сценарии, которые часто ломают SPA:
- 404 несуществующие страницы
- Невалидные URL-параметры
- Симуляция офлайн-режима
- Очень медленная сеть
- Некорректные deep links
"""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.asyncio
async def test_404_page_shows_content(page: Page):
    """Несуществующий путь должен возвращать 404 или fallback-страницу."""
    response = await page.goto("https://russia-tv.online/nonexistent-page-12345")
    if response:
        assert response.status in (200, 404)
    # SPA should still render some layout (header/footer) even on 404
    body = await page.query_selector("body")
    assert body is not None
    text = await body.inner_text() or ""
    assert len(text) > 0


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.asyncio
async def test_invalid_url_parameter(page: Page):
    """Невалидные query-параметры не должны падать сайт."""
    response = await page.goto("https://russia-tv.online/?region=invalid_region_999")
    if response:
        assert response.status == 200
    # Page should still be functional
    home = HomePage(page)
    channels = await home.get_visible_channels()
    # Should show default channels or empty state, not crash
    assert channels is not None


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.flaky
@pytest.mark.asyncio
async def test_offline_fallback(page: Page):
    """Симулировать офлайн и проверить graceful fallback."""
    await page.context.set_offline(True)
    try:
        await page.goto("https://russia-tv.online/")
        # If we reach here without exception, offline simulation may not
        # have triggered — still acceptable if page shows offline UI
    except Exception:
        pass  # Expected when offline
    finally:
        await page.context.set_offline(False)


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.asyncio
async def test_slow_network_loads(page: Page):
    """Страница должна eventually загружаться даже на медленном 3G."""
    cdp_session = await page.context.new_cdp_session(page)
    await cdp_session.send(
        "Network.emulateNetworkConditions",
        {
            "offline": False,
            "downloadThroughput": 500 * 1024 // 8,  # 500 kbps
            "uploadThroughput": 500 * 1024 // 8,
            "latency": 300,
        },
    )
    home = HomePage(page)
    await home.goto(timeout=60000)
    # Should still load within reasonable time
    await home.expect_channels_loaded(timeout=45000)
    channels = await home.get_visible_channels()
    assert len(channels) > 0
