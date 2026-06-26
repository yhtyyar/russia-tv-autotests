"""Search API client."""

import httpx

from core.base_api import BaseAPI


class SearchAPI(BaseAPI):
    """Client for search API endpoints."""

    async def search(self, query: str, limit: int = 20) -> httpx.Response:
        """Execute search query.

        Args:
            query: Search text.
            limit: Maximum results to return.

        Returns:
            HTTP response with search results.
        """
        return await self.get(
            "/search",
            params={"q": query, "limit": limit},
        )
