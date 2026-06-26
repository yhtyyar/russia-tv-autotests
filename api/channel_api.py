"""Channel API client."""

import httpx

from core.base_api import BaseAPI


class ChannelAPI(BaseAPI):
    """Client for channel-related API endpoints."""

    async def get_channels(self, category: str | None = None) -> httpx.Response:
        """Fetch list of channels.

        Args:
            category: Optional category filter.

        Returns:
            HTTP response with channel list.
        """
        params = {}
        if category:
            params["category"] = category
        return await self.get("/channels", params=params)

    async def get_channel_detail(self, channel_id: str) -> httpx.Response:
        """Fetch single channel details.

        Args:
            channel_id: Channel identifier.

        Returns:
            HTTP response with channel data.
        """
        return await self.get(f"/channels/{channel_id}")
