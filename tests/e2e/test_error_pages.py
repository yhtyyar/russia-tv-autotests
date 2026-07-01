"""Тесты обработки ошибок с использованием техники предугадывания ошибок.

Покрывает сценарии, которые часто ломают SPA:
- 404 несуществующие страницы
- Невалидные URL-параметры
- Симуляция офлайн-режима
- Очень медленная сеть
- Некорректные deep links
"""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.asyncio
@allure.feature("обработки ошибок")
@allure.story("Несуществующий путь должен возвращать 404 или fallback-страницу")
@allure.severity(Severity.NORMAL)
async def test_404_page_shows_content(page: Page):
    """Несуществующий путь должен возвращать 404 или fallback-страницу."""
    response = await page.goto("https://russia-tv.online/nonexistent-page-12345")
    assert response is not None and response.status in (
        200,
        404,
    ), f"Ожидался статус 200 или 404, получен: {response.status if response else None}"
    text = await page.locator("body").inner_text()
    assert (
        "не найдена" in text.lower() or "404" in text
    ), f"Ожидалось сообщение о том, что страница не найдена, получено: {text[:200]!r}"


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.asyncio
@allure.feature("обработки ошибок")
@allure.story("Невалидные query-параметры не должны падать сайт")
@allure.severity(Severity.NORMAL)
async def test_invalid_url_parameter(page: Page):
    """Невалидные query-параметры не должны падать сайт."""
    response = await page.goto("https://russia-tv.online/?region=invalid_region_999")
    assert response is not None and response.status == 200
    home = HomePage(page)
    await home.expect_channels_loaded(timeout=15000)
    channels = await home.get_visible_channels()
    # Невалидный регион должен приводить к fallback на регион по умолчанию,
    # а не к пустой странице.
    assert len(channels) > 0, "Список каналов пуст при невалидном параметре region"


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.flaky
@pytest.mark.asyncio
@allure.feature("обработки ошибок")
@allure.story("Симулировать офлайн и проверить graceful fallback")
@allure.severity(Severity.NORMAL)
async def test_offline_fallback(page: Page):
    """В офлайн-режиме навигация должна завершаться сетевой ошибкой, а не зависать.

    Проверено вручную: у сайта нет service worker/precache для полностью
    офлайн-режима, поэтому ожидаемое поведение браузера — явная ошибка
    net::ERR_INTERNET_DISCONNECTED, а не бесконечное ожидание или краш.
    """
    await page.context.set_offline(True)
    try:
        with pytest.raises(Exception, match="ERR_INTERNET_DISCONNECTED"):
            await page.goto("https://russia-tv.online/", timeout=15000)
    finally:
        await page.context.set_offline(False)

    # После возврата в онлайн сайт должен снова нормально загружаться
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)
    channels = await home.get_visible_channels()
    assert len(channels) > 0, "Список каналов пуст после возврата из офлайн-режима"


@pytest.mark.e2e
@pytest.mark.error_handling
@pytest.mark.asyncio
@allure.feature("обработки ошибок")
@allure.story("Страница должна eventually загружаться даже на медленном 3G")
@allure.severity(Severity.NORMAL)
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
