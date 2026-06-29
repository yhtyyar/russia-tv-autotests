"""Page Object страницы расписания russia-tv.online."""

from core.base_page import BasePage


class SchedulePage(BasePage):
    """Page Object для просмотра телепрограммы."""

    @property
    def path(self) -> str:
        return "/epg"

    _CHANNEL_LINKS = "a[href*='region=']"
    _DATE_SELECTOR = "input[type='date'], .date-selector"
    _PROGRAM_ITEMS = ".program-item, [data-testid='program-item']"
    _PROGRAM_TIMES = ".program-time, [data-testid='program-time']"
    _EMPTY_SCHEDULE = ".empty-schedule, .no-programs, [data-testid='empty-schedule']"
    _DARK_MODE_TOGGLE = "button[aria-label*='темн'], button[aria-label*='dark'], [data-testid='dark-mode-toggle'], .theme-toggle"
    _FOOTER = "footer"
    _COOKIE_BANNER = "[data-testid='cookie-banner'], .cookie-banner, #cookie-consent"
    _COOKIE_ACCEPT = "[data-testid='cookie-accept'], .cookie-accept, #cookie-consent button"

    async def select_date(self, date_str: str) -> None:
        """Выбрать дату из календаря, если он присутствует.

        Args:
            date_str: Строка даты в формате YYYY-MM-DD.
        """
        selector = f"{self._DATE_SELECTOR} select"
        if await self.is_element_visible(selector):
            await self.page.select_option(selector, date_str)

    async def get_channel_links(self) -> list[dict[str, str]]:
        """Получить список ссылок каналов на странице расписания.

        Returns:
            Список словарей с данными каналов.
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

    async def get_programs(self) -> list[dict[str, str]]:
        """Получить список передач с названием и временем.

        Returns:
            Список словарей с данными передач.
        """
        items = await self.page.query_selector_all(self._PROGRAM_ITEMS)
        programs = []
        for item in items:
            title_el = await item.query_selector(".title, .program-title")
            title = await title_el.text_content() if title_el else ""
            time_el = await item.query_selector(self._PROGRAM_TIMES)
            time_str = await time_el.text_content() if time_el else ""
            programs.append({
                "title": (title or "").strip(),
                "time": (time_str or "").strip(),
            })
        return programs

    async def is_empty_schedule_visible(self) -> bool:
        """Проверить, видно ли сообщение «пустое расписание».

        Returns:
            True, если видно состояние пустого расписания.
        """
        return await self.is_element_visible(self._EMPTY_SCHEDULE)

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

    async def get_available_dates(self) -> list[str]:
        """Получить список доступных вариантов дат.

        Returns:
            Список значений опций дат.
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
