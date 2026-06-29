"""Тесты performance budget с использованием анализа граничных значений.

Бюджеты производительности (время загрузки страницы):
- Mobile 3G: < 5s (TTFB + render)
- Desktop WiFi: < 2s
- First Contentful Paint: < 1.5s
"""

import httpx
import pytest

BASE_URL = "https://russia-tv.online/"


@pytest.mark.integration
@pytest.mark.performance
@pytest.mark.asyncio
async def test_homepage_load_time_desktop():
    """Главная страница должна загружаться за 2 секунды на десктопе."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(BASE_URL)
        assert response.status_code == 200
        # httpx total time includes connection + TTFB + download
        total_time = response.elapsed.total_seconds()
        assert total_time < 2.0, (
            f"Home page load time {total_time:.2f}s exceeds 2s budget"
        )


@pytest.mark.integration
@pytest.mark.performance
@pytest.mark.asyncio
async def test_schedule_page_load_time():
    """Страница расписания должна загружаться за 2.5 секунды."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{BASE_URL}epg")
        assert response.status_code == 200
        total_time = response.elapsed.total_seconds()
        assert total_time < 2.5, (
            f"Schedule page load time {total_time:.2f}s exceeds 2.5s budget"
        )


@pytest.mark.integration
@pytest.mark.performance
@pytest.mark.asyncio
async def test_api_response_time_budget():
    """Внутренние API-эндпоинты должны отвечать за 1 секунду."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(f"{BASE_URL}api/channels")
        # May return 404 if no public API, but should be fast
        total_time = response.elapsed.total_seconds()
        assert total_time < 1.0, (
            f"API response time {total_time:.2f}s exceeds 1s budget"
        )


@pytest.mark.integration
@pytest.mark.performance
@pytest.mark.asyncio
async def test_assets_cache_headers():
    """Статические ассеты должны иметь cache-заголовки для производительности."""
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL)
        assert response.status_code == 200
        # Check for common cache-related headers
        cache_control = response.headers.get("cache-control", "")
        etag = response.headers.get("etag")
        assert cache_control or etag, (
            "No cache headers found for static content"
        )
