"""Schedule API client."""

from typing import Any

import httpx

from core.base_api import BaseAPI


class ScheduleAPI(BaseAPI):
    """Client for schedule-related API endpoints."""

    async def get_schedule(
        self,
        date: str,
        channel_id: str | None = None,
    ) -> httpx.Response:
        """Fetch TV schedule for a date.

        Args:
            date: Date string (today, yesterday, tomorrow, or YYYY-MM-DD).
            channel_id: Optional specific channel filter.

        Returns:
            HTTP response with schedule data.
        """
        params: dict[str, Any] = {"date": date}
        if channel_id:
            params["channel_id"] = channel_id
        return await self.get("/schedule", params=params)

    async def get_current_broadcasts(self) -> httpx.Response:
        """Fetch currently airing programs.

        Returns:
            HTTP response with current broadcast data.
        """
        return await self.get("/schedule/current")
