"""Schedule page object for russia-tv.online."""

from core.base_page import BasePage


class SchedulePage(BasePage):
    """Schedule page object for TV program schedule view."""

    @property
    def path(self) -> str:
        return "/epg"

    _CHANNEL_LINKS = "a[href*='region=']"
    _DATE_SELECTOR = "input[type='date'], .date-selector"

    async def select_date(self, date_str: str) -> None:
        """Select a date from the date picker if present.

        Args:
            date_str: Date string in YYYY-MM-DD format.
        """
        selector = f"{self._DATE_SELECTOR} select"
        if await self.is_element_visible(selector):
            await self.page.select_option(selector, date_str)

    async def get_channel_links(self) -> list[dict[str, str]]:
        """Get list of channel links on schedule page.

        Returns:
            List of channel data dictionaries.
        """
        items = await self.page.query_selector_all(self._CHANNEL_LINKS)
        channels = []
        for item in items:
            text = await item.inner_text() or ""
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            name = lines[-1] if lines else ""
            href = await item.get_attribute("href") or ""
            channels.append({"name": name, "href": href})
        return channels

    async def get_available_dates(self) -> list[str]:
        """Get list of available date options.

        Returns:
            List of date option values.
        """
        options = await self.page.query_selector_all(
            "input[type='date'], .date-selector option",
        )
        dates = []
        for opt in options:
            value = await opt.get_attribute("value")
            if value:
                dates.append(value)
        return dates
