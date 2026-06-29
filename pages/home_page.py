"""Page Object главной страницы russia-tv.online."""

from core.base_page import BasePage


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
    _EMPTY_STATE = ".empty-state, [data-testid='empty-state'], .no-results"

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

    async def get_visible_channels(self) -> list[dict[str, str]]:
        """Получить список видимых карточек каналов.

        Returns:
            Список словарей с данными каналов.
        """
        cards = await self.page.query_selector_all(self._CHANNEL_CARDS)
        channels = []
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

    async def search(self, query: str) -> None:
        """Ввести поисковый запрос.

        Args:
            query: Текст для ввода в поиск.
        """
        await self.fill(self._SEARCH_INPUT, query)
        await self.page.press(self._SEARCH_INPUT, "Enter")

    async def is_search_visible(self) -> bool:
        """Проверить, видно ли поле поиска.

        Returns:
            True, если поле поиска видно.
        """
        return await self.is_element_visible(self._SEARCH_INPUT)

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

    async def get_footer_links(self) -> list[dict[str, str]]:
        """Получить все ссылки футера с текстом и href.

        Returns:
            Список словарей с ключами 'text' и 'href'.
        """
        links = await self.page.query_selector_all(self._FOOTER_LINKS)
        result = []
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
