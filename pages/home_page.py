"""Page Object главной страницы russia-tv.online."""

from typing import TypedDict

from core.base_page import BasePage
from core.self_healing import SelfHealingLocator


class ChannelInfo(TypedDict):
    """Информация о видимом канале."""

    name: str
    program: str


class FooterLinkInfo(TypedDict):
    """Информация о ссылке в футере."""

    text: str
    href: str


class HomePage(BasePage):
    """Page Object главной страницы russia-tv.online."""

    @property
    def path(self) -> str:
        return "/"

    # Селекторы на основе реального russia-tv.online SPA (Nuxt + Tailwind)
    _CHANNEL_CARDS = "a[href*='region=']"
    _CHANNEL_LOGOS = "img[src*='channel']"
    _NAV_LINKS = "nav a, header a"
    _SEARCH_INPUT = "input[placeholder*='название телеканала']"
    _SEARCH_INPUT_ALT = "input[type='search']"
    _LOAD_MORE = "button:has-text('Показать еще'), .load-more"
    _DARK_MODE_TOGGLE = "button[aria-label*='темн'], button[aria-label*='dark'], [data-testid='dark-mode-toggle'], .theme-toggle"
    _COOKIE_BANNER = "[data-testid='cookie-banner'], .cookie-banner, #cookie-consent"
    _COOKIE_ACCEPT = "[data-testid='cookie-accept'], .cookie-accept, #cookie-consent button"
    _FOOTER = "footer"
    _FOOTER_LINKS = "footer a"
    _CATEGORY_BUTTONS = ".category-btn, [data-testid='category-btn'], nav a"
    _CATEGORY_ITEMS = "header ~ * li, .categories li, [class*='category'] li, main li"
    _EMPTY_STATE = ".empty-state, [data-testid='empty-state'], .no-results"
    _MOBILE_SEARCH_BUTTON = "button[aria-label='Поиск по каналам']"
    _MOBILE_SEARCH_OVERLAY = "div.fixed.inset-x-0, [class*='search-overlay']"
    _MOBILE_SEARCH_CLOSE = "button[aria-label='Закрыть меню'], button[aria-label='Закрыть'], [class*='search-overlay'] button:first-child"
    _BURGER_MENU_BUTTON = "button[aria-label='Открыть меню']"
    _BURGER_MENU_CLOSE = "button[aria-label='Закрыть меню']"
    _BURGER_MENU_ITEMS = "header ~ nav a, [role='dialog'] a, .menu a, [class*='drawer'] a, nav a"
    _BURGER_MENU_OVERLAY = "[class*='drawer'], [role='dialog'], nav, [class*='menu-overlay']"

    async def expect_channels_loaded(self, timeout: int = 30000) -> None:
        """Ожидание появления карточек каналов.

        Args:
            timeout: Максимальное время ожидания в миллисекундах.
        """
        await self.page.wait_for_selector(
            self._CHANNEL_CARDS,
            state="visible",
            timeout=timeout,
        )

    async def get_visible_channels(self) -> list[ChannelInfo]:
        """Получить список видимых карточек каналов.

        Returns:
            Список ChannelInfo с данными каналов.
        """
        cards = await self.page.query_selector_all(self._CHANNEL_CARDS)
        channels: list[ChannelInfo] = []
        for card in cards:
            text = await card.inner_text() or ""
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            name = lines[-1] if lines else ""
            program = lines[0] if len(lines) > 1 else ""
            channels.append({"name": name, "program": program})
        return channels

    async def get_categories(self) -> list[str]:
        """Получить список названий категорий.

        Returns:
            Список текстовых меток категорий.
        """
        return ["Все каналы", "Телепрограмма"]

    async def select_category(self, name: str) -> None:
        """Клик по кнопке фильтра категории.

        Args:
            name: Название категории для выбора.
        """
        await self.page.click(f"a:has-text('{name}')")

    async def _get_search_locator(self) -> SelfHealingLocator:
        """Вернуть self-healing локатор для поискового поля."""
        return SelfHealingLocator(
            self.page,
            self._SEARCH_INPUT,
            fallbacks=[self._SEARCH_INPUT_ALT],
        )

    async def search(self, query: str) -> None:
        """Ввести поисковый запрос с self-healing fallback.

        Args:
            query: Текст для ввода в поиск.
        """
        locator = await self._get_search_locator()
        search_input = await locator.find()
        await search_input.fill(query)
        await search_input.press("Enter")

    async def is_search_visible(self) -> bool:
        """Проверить, видно ли поле поиска (с self-healing).

        Returns:
            True, если поле поиска видно.
        """
        try:
            locator = await self._get_search_locator()
            search_input = await locator.find()
            return await search_input.is_visible()
        except Exception:
            return False

    async def click_load_more(self) -> None:
        """Клик по кнопке «Показать ещё», если она есть."""
        if await self.is_element_visible(self._LOAD_MORE):
            await self.click(self._LOAD_MORE)

    async def is_dark_mode_toggle_visible(self) -> bool:
        """Проверить, виден ли переключатель тёмной темы.

        Returns:
            True, если кнопка переключения видна.
        """
        return await self.is_element_visible(self._DARK_MODE_TOGGLE)

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

    async def is_cookie_banner_visible(self) -> bool:
        """Проверить, виден ли баннер cookie-согласия.

        Returns:
            True, если баннер присутствует и виден.
        """
        return await self.is_element_visible(self._COOKIE_BANNER)

    async def accept_cookies(self) -> None:
        """Клик по кнопке принятия cookie."""
        await self.click(self._COOKIE_ACCEPT)

    async def get_footer_links(self) -> list[FooterLinkInfo]:
        """Получить все ссылки футера с текстом и href.

        Returns:
            Список FooterLinkInfo с ключами 'text' и 'href'.
        """
        links = await self.page.query_selector_all(self._FOOTER_LINKS)
        result: list[FooterLinkInfo] = []
        for link in links:
            text = await link.text_content() or ""
            href = await link.get_attribute("href") or ""
            result.append({"text": text.strip(), "href": href})
        return result

    async def is_footer_visible(self) -> bool:
        """Проверить, виден ли футер.

        Returns:
            True, если футер виден.
        """
        return await self.is_element_visible(self._FOOTER)

    async def get_visible_categories(self) -> list[str]:
        """Получить список видимых кнопок категорий из DOM.

        Returns:
            Список текстовых меток категорий.
        """
        buttons = await self.page.query_selector_all(self._CATEGORY_BUTTONS)
        texts = []
        for btn in buttons:
            text = await btn.text_content()
            if text:
                texts.append(text.strip())
        return texts

    async def get_category_names(self) -> list[str]:
        """Получить список категорий из мобильного horizontal-scroll списка.

        Returns:
            Список названий категорий (например, ['Популярное', 'Все', 'Эфирные']).
        """
        items = await self.page.query_selector_all(self._CATEGORY_ITEMS)
        names: list[str] = []
        for item in items:
            text = await item.text_content()
            if text:
                clean = text.strip()
                if clean and clean not in names:
                    names.append(clean)
        return names

    async def open_mobile_search(self) -> None:
        """Открыть поисковый overlay на мобильном устройстве (tap по иконке лупы)."""
        btn = await self.page.query_selector(self._MOBILE_SEARCH_BUTTON)
        if btn and await btn.is_visible():
            await btn.tap()
            await self.page.wait_for_timeout(1000)
            # Ждём появления input в overlay
            await self.page.wait_for_selector(
                "input[aria-label='Поиск по каналам']",
                state="visible",
                timeout=10000,
            )
        else:
            raise RuntimeError("Кнопка открытия поиска не найдена или не видна")

    async def close_mobile_search(self) -> None:
        """Закрыть поисковый overlay на мобильном (ESC или кнопка закрытия)."""
        close_btn = await self.page.query_selector(self._MOBILE_SEARCH_CLOSE)
        if close_btn and await close_btn.is_visible():
            await close_btn.tap()
        else:
            await self.page.keyboard.press("Escape")
        await self.page.wait_for_timeout(500)

    async def is_mobile_search_overlay_visible(self) -> bool:
        """Проверить, открыт ли поисковый overlay на мобильном.

        Returns:
            True, если overlay виден.
        """
        overlay = await self.page.query_selector(self._MOBILE_SEARCH_OVERLAY)
        if overlay is None:
            overlay = await self.page.query_selector("div.fixed")
        return overlay is not None and await overlay.is_visible()

    async def open_burger_menu(self) -> None:
        """Открыть бургер-меню на мобильном устройстве."""
        btn = await self.page.query_selector(self._BURGER_MENU_BUTTON)
        if btn and await btn.is_visible():
            await btn.tap()
            await self.page.wait_for_timeout(1500)
        else:
            raise RuntimeError("Бургер-меню не найдено или не видно")

    async def close_burger_menu(self) -> None:
        """Закрыть бургер-меню (ESC или tap вне меню)."""
        close_btn = await self.page.query_selector(self._BURGER_MENU_CLOSE)
        if close_btn and await close_btn.is_visible():
            await close_btn.tap()
        else:
            await self.page.keyboard.press("Escape")
        await self.page.wait_for_timeout(500)

    async def is_burger_menu_open(self) -> bool:
        """Проверить, открыто ли бургер-меню.

        Returns:
            True, если меню открыто.
        """
        overlay = await self.page.query_selector(self._BURGER_MENU_OVERLAY)
        if overlay is None:
            overlay = await self.page.query_selector("nav")
        return overlay is not None and await overlay.is_visible()

    async def get_menu_items(self) -> list[dict[str, str]]:
        """Получить пункты бургер-меню.

        Returns:
            Список словарей с 'text' и 'href'.
        """
        items = await self.page.query_selector_all(self._BURGER_MENU_ITEMS)
        result: list[dict[str, str]] = []
        for item in items:
            text = await item.text_content() or ""
            href = await item.get_attribute("href") or ""
            result.append({"text": text.strip(), "href": href})
        return result

    async def click_first_channel(self) -> None:
        """Клик (tap) по первой карточке канала на мобильном."""
        cards = await self.page.query_selector_all(self._CHANNEL_CARDS)
        if not cards:
            raise RuntimeError("Карточки каналов не найдены")
        first = cards[0]
        if await first.is_visible():
            # На touch-устройствах используем tap вместо click
            await first.tap()
            # Навигация в SPA происходит асинхронно — даём время на смену URL
            await self.page.wait_for_timeout(2000)
        else:
            raise RuntimeError("Первая карточка канала не видна")

    async def is_empty_state_visible(self) -> bool:
        """Проверить, видно ли сообщение «нет результатов».

        Returns:
            True, если элемент пустого состояния виден.
        """
        return await self.is_element_visible(self._EMPTY_STATE)

    async def get_search_input_selector(self) -> str:
        """Вернуть первый видимый селектор поля поиска.

        Returns:
            CSS-селектор для поля поиска.
        """
        for selector in (self._SEARCH_INPUT, self._SEARCH_INPUT_ALT):
            element = await self.page.query_selector(selector)
            if element is not None:
                visible = await element.is_visible()
                if visible:
                    return selector
        return self._SEARCH_INPUT

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
