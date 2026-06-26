"""Channel detail page object."""

from core.base_page import BasePage


class ChannelPage(BasePage):
    """Channel detail page showing channel info and schedule."""

    @property
    def path(self) -> str:
        return "/channel/{channel_id}"

    _CHANNEL_NAME = ".channel-title, [data-testid='channel-title']"
    _PROGRAM_LIST = ".program-list, [data-testid='program-list']"
    _CURRENT_PROGRAM = ".current-program, [data-testid='current-program']"

    async def open_channel(self, channel_id: str) -> None:
        """Navigate to a specific channel page.

        Args:
            channel_id: Channel identifier.
        """
        await self.page.goto(f"{self.base_url}/channel/{channel_id}")

    async def get_channel_name(self) -> str:
        """Get displayed channel name.

        Returns:
            Channel title text.
        """
        return await self.get_text(self._CHANNEL_NAME)

    async def get_programs(self) -> list[dict]:
        """Get channel program list.

        Returns:
            List of program data.
        """
        items = await self.page.query_selector_all(
            f"{self._PROGRAM_LIST} .program-item",
        )
        programs = []
        for item in items:
            title_el = await item.query_selector(".title")
            title = await title_el.text_content() if title_el else ""
            time_el = await item.query_selector(".time")
            time_str = await time_el.text_content() if time_el else ""
            programs.append({
                "title": (title or "").strip(),
                "time": (time_str or "").strip(),
            })
        return programs
