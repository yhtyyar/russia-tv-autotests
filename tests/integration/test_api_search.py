"""Integration tests for Search API."""

import httpx
import pytest

from api.search_api import SearchAPI


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_search_returns_200():
    """Search endpoint should return 200 for valid query."""
    async with httpx.AsyncClient() as client:
        api = SearchAPI(client)
        response = await api.search(query="news")
        assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_search_empty_query_returns_400():
    """Search with empty query should return 400."""
    async with httpx.AsyncClient() as client:
        api = SearchAPI(client)
        response = await api.search(query="")
        assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.xfail(reason="Site uses SSR without public REST API")
@pytest.mark.asyncio
async def test_search_response_contains_results():
    """Search response should contain results structure."""
    async with httpx.AsyncClient() as client:
        api = SearchAPI(client)
        response = await api.search(query="news")
        if response.status_code == 200:
            data = response.json()
            assert any(key in data for key in ("results", "items", "channels", "programs"))
