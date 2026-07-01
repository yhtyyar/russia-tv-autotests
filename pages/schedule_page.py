"""Page Object страницы расписания russia-tv.online."""

import contextlib

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from core.base_page import BasePage


class SchedulePage(BasePage):
    """Page Object для просмотра телепрограммы."""

    @property
    def path(self) -> str:
        return "/epg"

    CHANNEL_LINKS = "a[href*='region=']"
    DATE_SELECTOR = "input[type='date'], .date-selector"
    _PROGRAM_ITEMS = ".program-item, [data-testid='program-item']"
    _PROGRAM_TIMES = ".program-time, [data-testid='program-time']"
    _EMPTY_SCHEDULE = ".empty-schedule, .no-programs, [data-testid='empty-schedule']"

    async def select_date(self, date_str: str) -> None:
        """Выбрать дату в date picker, если он присутствует на странице.

        Поддерживает нативный ``<input type="date">`` (приоритетно) и
        кастомный виджет на основе ``<select>`` внутри ``.date-selector``.

        Args:
            date_str: Дата в формате YYYY-MM-DD.

        Raises:
            NotImplementedError: если на странице нет ни нативного
                input[type=date], ни поддерживаемого кастомного виджета.
                Проверено вручную на живом сайте (2026-07-01, /epg и
                страница канала) — date picker сейчас отсутствует вовсе.
        """
        date_input = self.page.locator("input[type='date']")
        if await date_input.count() > 0 and await date_input.first.is_visible():
            await date_input.first.fill(date_str)
            # SPA может не достигать networkidle из-за фоновых запросов
            with contextlib.suppress(PlaywrightTimeoutError):
                await self.page.wait_for_load_state("networkidle", timeout=5000)
            return

        select = self.page.locator(".date-selector select")
        if await select.count() > 0 and await select.first.is_visible():
            await select.first.select_option(date_str)
            return

        raise NotImplementedError(
            "Date picker не найден на странице расписания — виджет выбора "
            "даты отсутствует на текущей версии сайта (см. CLAUDE.md)"
        )

    async def get_channel_links(self) -> list[dict[str, str]]:
        """Получить список ссылок каналов на странице расписания.

        Returns:
            Список словарей с данными каналов.
        """
        items = await self.page.query_selector_all(self.CHANNEL_LINKS)
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
            programs.append(
                {
                    "title": (title or "").strip(),
                    "time": (time_str or "").strip(),
                }
            )
        return programs

    async def is_empty_schedule_visible(self) -> bool:
        """Проверить, видно ли сообщение «пустое расписание».

        Returns:
            True, если видно состояние пустого расписания.
        """
        return await self.is_element_visible(self._EMPTY_SCHEDULE)

    async def get_available_dates(self) -> list[str]:
        """Получить список доступных дат из кастомного date picker.

        Returns:
            Список значений опций дат. Пустой список, если используется
            нативный input[type=date] (у него нет фиксированного набора
            вариантов) или date picker отсутствует на странице.
        """
        options = await self.page.query_selector_all(".date-selector option")
        dates = []
        for opt in options:
            value = await opt.get_attribute("value")
            if value:
                dates.append(value)
        return dates
