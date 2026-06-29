"""Базовый класс Page Object для страниц Playwright."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Literal

from playwright.async_api import Page

from config.settings import get_settings
from core.logger import get_logger

logger = get_logger(__name__)


class BasePage(ABC):
    """Абстрактный базовый класс для всех page objects.

    Предоставляет общие методы взаимодействия и работу с URL.
    """

    def __init__(self, page: Page) -> None:
        """Инициализация page object.

        Args:
            page: Экземпляр Playwright Page.
        """
        self.page = page
        self.settings = get_settings()
        self.base_url = self.settings.base_url.rstrip("/")

    @property
    @abstractmethod
    def path(self) -> str:
        """URL-путь страницы. Переопределяется в подклассах."""

    @property
    def url(self) -> str:
        """Полный URL страницы."""
        return f"{self.base_url}{self.path}"

    async def goto(self, **kwargs: Any) -> None:
        """Навигация на URL страницы с retry при сетевых ошибках.

        Args:
            **kwargs: Дополнительные аргументы, передаваемые в page.goto.
        """
        logger.info("Navigating to %s", self.url)
        last_err = None
        for attempt in range(1, 4):
            try:
                await self.page.goto(self.url, **kwargs)
                logger.info("Loaded %s", self.url)
                return
            except Exception as exc:
                last_err = exc
                if "ERR_NETWORK_CHANGED" in str(exc) and attempt < 3:
                    await asyncio.sleep(0.5)
                    continue
                raise
        if last_err:
            raise last_err

    async def wait_for_load(
        self, state: Literal["load", "domcontentloaded", "networkidle"] = "networkidle"
    ) -> None:
        """Ожидание достижения страницей нужного состояния загрузки.

        Args:
            state: Состояние загрузки для ожидания (load, domcontentloaded, networkidle).
        """
        await self.page.wait_for_load_state(state)

    async def is_element_visible(self, selector: str) -> bool:
        """Проверить, виден ли элемент на странице.

        Args:
            selector: CSS или XPath селектор.

        Returns:
            True, если элемент виден, иначе False.
        """
        element = await self.page.query_selector(selector)
        if element is None:
            return False
        return await element.is_visible()

    async def click(self, selector: str, **kwargs: Any) -> None:
        """Клик по элементу.

        Args:
            selector: CSS или XPath селектор.
            **kwargs: Дополнительные аргументы, передаваемые в page.click.
        """
        logger.debug("Clicking selector: %s", selector)
        await self.page.click(selector, **kwargs)

    async def fill(self, selector: str, value: str) -> None:
        """Заполнить поле ввода.

        Args:
            selector: CSS или XPath селектор для input.
            value: Значение для заполнения.
        """
        logger.debug("Filling selector %s with value %r", selector, value)
        await self.page.fill(selector, value)

    async def get_text(self, selector: str) -> str:
        """Получить текстовое содержимое элемента.

        Args:
            selector: CSS или XPath селектор.

        Returns:
            Текстовое содержимое элемента.
        """
        element = await self.page.query_selector(selector)
        if element is None:
            return ""
        text = await element.text_content()
        return text or ""

    async def take_screenshot(self, name: str) -> str:
        """Сделать скриншот и сохранить в директорию reports.

        Args:
            name: Имя файла скриншота (без расширения).

        Returns:
            Путь к сохранённому скриншоту.
        """
        import os

        path = os.path.join(self.settings.screenshot_dir, f"{name}.png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        await self.page.screenshot(path=path, full_page=True)
        return path
