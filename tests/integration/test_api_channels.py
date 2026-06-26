"""Integration tests for Channel API."""

import httpx
import pytest

from api.channel_api import ChannelAPI


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_channels_returns_200():
    """Channels list endpoint should return 200."""
    async with httpx.AsyncClient() as client:
        api = ChannelAPI(client)
        response = await api.get_channels()
        assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_channels_by_category_returns_200():
    """Channels filtered by category should return 200."""
    async with httpx.AsyncClient() as client:
        api = ChannelAPI(client)
        response = await api.get_channels(category="entertainment")
        assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_get_channel_detail_returns_200_or_404():
    """Channel detail should return 200 or 404 for unknown channel."""
    async with httpx.AsyncClient() as client:
        api = ChannelAPI(client)
        response = await api.get_channel_detail("1")
        assert response.status_code in (200, 404)
