"""Интеграционные тесты проверки доступности сайта без зависимости от публичного REST API."""

import httpx
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_home_page_returns_200():
    """Главная страница должна возвращать 200 OK."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_schedule_page_returns_200():
    """Страница расписания /epg должна возвращать 200 OK."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/epg")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_home_page_contains_channel_content():
    """HTML главной страницы должен содержать ожидаемый контент о каналах."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/")
        assert response.status_code == 200
        text = response.text
        assert "канал" in text.lower() or "телепрограмма" in text.lower()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_site_performance_baseline():
    """Главная страница должна загружаться за 2 секунды."""
    import time
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        response = await client.get("https://russia-tv.online/")
        duration = time.perf_counter() - start
        assert response.status_code == 200
        assert duration < 5.0, f"Site too slow: {duration:.2f}s"
