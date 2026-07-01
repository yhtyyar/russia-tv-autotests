"""Page Object страницы канала."""

from playwright.async_api import Page

from core.base_page import BasePage

DEFAULT_REGION_ID = 21


class ChannelPage(BasePage):
    """Страница канала с информацией и расписанием.

    Реальная схема URL сайта — ``/{slug}?region={region_id}``
    (например, ``/1kanal?region=21``), а не ``/channel/{id}``.
    """

    def __init__(self, page: Page, slug: str = "", region_id: int = DEFAULT_REGION_ID) -> None:
        """Инициализация page object канала.

        Args:
            page: Экземпляр Playwright Page.
            slug: URL-friendly идентификатор канала (например, '1kanal').
            region_id: ID региона (по умолчанию 21 — проверено на живом сайте).
        """
        super().__init__(page)
        self._slug = slug
        self._region_id = region_id

    @property
    def path(self) -> str:
        return f"/{self._slug}?region={self._region_id}"

    # Проверено на живом сайте (russia-tv.online/1kanal?region=21, 2026-07-01)
    _CHANNEL_NAME = "h1[data-test='current-channel-name'], h1"
    _CURRENT_PROGRAM = "[data-test='current-channel-program-title']"
    _PROGRAM_TIME_ITEMS = "[data-test='epg-program-start']"
    _PROGRAM_TITLE_ITEMS = "[data-test='epg-program-title']"

    async def open_channel(self, slug: str, region_id: int = DEFAULT_REGION_ID) -> None:
        """Перейти на страницу конкретного канала.

        Args:
            slug: URL-friendly идентификатор канала (например, '1kanal').
            region_id: ID региона (по умолчанию 21).
        """
        self._slug = slug
        self._region_id = region_id
        await self.goto()

    async def get_channel_name(self) -> str:
        """Получить отображаемое название канала.

        Returns:
            Текст названия канала.
        """
        return await self.get_text(self._CHANNEL_NAME)

    async def get_programs(self) -> list[dict[str, str]]:
        """Получить список передач канала (время + название) из EPG-блока.

        Returns:
            Список словарей с ключами 'time' и 'title'.
        """
        times = await self.page.locator(self._PROGRAM_TIME_ITEMS).all_inner_texts()
        titles = await self.page.locator(self._PROGRAM_TITLE_ITEMS).all_inner_texts()
        return [
            {"time": time_str.strip(), "title": title.strip()}
            for time_str, title in zip(times, titles, strict=False)
        ]

    async def is_current_program_visible(self) -> bool:
        """Проверить, виден ли индикатор текущей передачи.

        Returns:
            True, если элемент текущей передачи виден.
        """
        return await self.is_element_visible(self._CURRENT_PROGRAM)
