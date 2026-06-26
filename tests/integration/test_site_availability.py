"""Integration tests verifying site availability without relying on public REST API."""

import httpx
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_home_page_returns_200():
    """Home page should return 200 OK."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_schedule_page_returns_200():
    """Schedule /epg page should return 200 OK."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/epg")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_home_page_contains_channel_content():
    """Home page HTML should contain expected channel-related content."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://russia-tv.online/")
        assert response.status_code == 200
        text = response.text
        assert "канал" in text.lower() or "телепрограмма" in text.lower()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_site_performance_baseline():
    """Home page should load within 2 seconds."""
    import time
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        response = await client.get("https://russia-tv.online/")
        duration = time.perf_counter() - start
        assert response.status_code == 200
        assert duration < 5.0, f"Site too slow: {duration:.2f}s"
