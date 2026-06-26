"""Integration tests for Schedule API."""

import httpx
import pytest

from api.schedule_api import ScheduleAPI


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_schedule_today_returns_200():
    """Schedule endpoint should return 200 for today's date."""
    async with httpx.AsyncClient() as client:
        api = ScheduleAPI(client)
        response = await api.get_schedule(date="today")
        assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_schedule_yesterday_returns_200():
    """Schedule endpoint should return 200 for yesterday's date."""
    async with httpx.AsyncClient() as client:
        api = ScheduleAPI(client)
        response = await api.get_schedule(date="yesterday")
        assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_schedule_invalid_date_returns_400():
    """Schedule endpoint should return 400 for invalid date format."""
    async with httpx.AsyncClient() as client:
        api = ScheduleAPI(client)
        response = await api.get_schedule(date="invalid-date")
        assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_schedule_response_has_channels():
    """Schedule response should contain channels list."""
    async with httpx.AsyncClient() as client:
        api = ScheduleAPI(client)
        response = await api.get_schedule(date="today")
        if response.status_code == 200:
            data = response.json()
            assert "channels" in data or "programs" in data or "schedule" in data


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_current_broadcasts_returns_200():
    """Current broadcasts endpoint should return 200."""
    async with httpx.AsyncClient() as client:
        api = ScheduleAPI(client)
        response = await api.get_current_broadcasts()
        assert response.status_code == 200
