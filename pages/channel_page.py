"""Page Object страницы канала."""

from core.base_page import BasePage


class ChannelPage(BasePage):
    """Страница канала с информацией и расписанием."""

    @property
    def path(self) -> str:
        return "/channel/{channel_id}"

    _CHANNEL_NAME = ".channel-title, [data-testid='channel-title'], h1, .channel-header h1"
    _PROGRAM_LIST = ".program-list, [data-testid='program-list']"
    _CURRENT_PROGRAM = ".current-program, [data-testid='current-program']"
    _DARK_MODE_TOGGLE = "button[aria-label*='темн'], button[aria-label*='dark'], [data-testid='dark-mode-toggle'], .theme-toggle"
    _FOOTER = "footer"
    _COOKIE_BANNER = "[data-testid='cookie-banner'], .cookie-banner, #cookie-consent"
    _COOKIE_ACCEPT = "[data-testid='cookie-accept'], .cookie-accept, #cookie-consent button"

    async def open_channel(self, channel_id: str) -> None:
        """Перейти на страницу конкретного канала.

        Args:
            channel_id: Идентификатор канала.
        """
        await self.page.goto(f"{self.base_url}/channel/{channel_id}")

    async def get_channel_name(self) -> str:
        """Получить отображаемое название канала.

        Returns:
            Текст названия канала.
        """
        return await self.get_text(self._CHANNEL_NAME)

    async def get_programs(self) -> list[dict[str, str]]:
        """Получить список передач канала.

        Returns:
            Список данных передач.
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

    async def is_current_program_visible(self) -> bool:
        """Проверить, виден ли индикатор текущей передачи.

        Returns:
            True, если элемент текущей передачи виден.
        """
        return await self.is_element_visible(self._CURRENT_PROGRAM)

    async def toggle_dark_mode(self) -> None:
        """Клик по переключателю тёмной темы."""
        await self.click(self._DARK_MODE_TOGGLE)

    async def is_dark_mode_active(self) -> bool:
        """Проверить, активна ли тёмная тема.

        Returns:
            True, если html или body имеют dark-класс/атрибут.
        """
        return bool(
            await self.page.evaluate(
                "() => document.documentElement.classList.contains('dark') || "
                "document.body.classList.contains('dark') || "
                "document.documentElement.getAttribute('data-theme') === 'dark'"
            )
        )

    async def is_footer_visible(self) -> bool:
        """Проверить, виден ли футер.

        Returns:
            True, если футер виден.
        """
        return await self.is_element_visible(self._FOOTER)

    async def is_cookie_banner_visible(self) -> bool:
        """Проверить, виден ли баннер cookie-согласия.

        Returns:
            True, если баннер присутствует и виден.
        """
        return await self.is_element_visible(self._COOKIE_BANNER)

    async def accept_cookies(self) -> None:
        """Клик по кнопке принятия cookie."""
        await self.click(self._COOKIE_ACCEPT)

    async def get_meta_tags(self) -> dict[str, str]:
        """Извлечь SEO meta-теги из head страницы.

        Returns:
            Словарь с title, description, og:title, og:description, og:image.
        """
        result = await self.page.evaluate("""() => {
            const getMeta = (name) => {
                const el = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`);
                return el ? el.content : "";
            };
            return {
                title: document.title,
                description: getMeta("description"),
                og_title: getMeta("og:title"),
                og_description: getMeta("og:description"),
                og_image: getMeta("og:image"),
                canonical: document.querySelector('link[rel="canonical"]')?.href || ""
            };
        }
        """)
        return dict(result)
