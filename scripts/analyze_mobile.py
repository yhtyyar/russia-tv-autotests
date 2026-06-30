"""Скрипт для анализа мобильной версии russia-tv.online.

Запуск:
    uv run python scripts/analyze_mobile.py
"""

import asyncio
import json

from playwright.async_api import async_playwright

BASE_URL = "https://russia-tv.online/"
VIEWPORT = {"width": 390, "height": 844}


async def analyze() -> None:
    """Проанализировать мобильную версию сайта."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=VIEWPORT,
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                "Mobile/15E148 Safari/604.1"
            ),
            is_mobile=True,
            has_touch=True,
            device_scale_factor=3,
        )
        page = await context.new_page()

        page.set_default_timeout(60000)

        # 1. Главная страница
        print("=== Анализ главной страницы (mobile viewport 390×844) ===")
        await page.goto(BASE_URL, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        await page.screenshot(path="reports/screenshots/mobile_home_full.png", full_page=True)
        print("Скриншот сохранён: reports/screenshots/mobile_home_full.png")

        # Элементы DOM
        selectors = {
            "header": "header",
            "logo": "header img, header a[href='/']",
            "burger_menu_button": "button[aria-label*='меню'], button[aria-label*='menu'], .burger, .hamburger, nav button, header button",
            "search_input": "input[type='search'], input[placeholder*='Поиск'], input[placeholder*='поиск']",
            "search_button": "button[type='submit'], button[aria-label*='Поиск']",
            "channel_cards": "[data-testid='channel-card'], .channel-card, .channel-item, a[href*='/channel/']",
            "cookie_banner": "[data-testid='cookie-banner'], .cookie-banner, .cookie-consent, [class*='cookie']",
            "dark_mode_toggle": "[data-testid='dark-mode-toggle'], button[aria-label*='тёмн'], button[aria-label*='dark']",
            "footer": "footer",
            "footer_links": "footer a",
            "load_more_button": "button:has-text('Показать ещё'), button:has-text('Load more'), [data-testid='load-more']",
            "category_filter": "select, .category-filter, [data-testid='category-filter']",
        }

        results = {}
        for name, sel in selectors.items():
            els = await page.query_selector_all(sel)
            visible = 0
            for el in els:
                if await el.is_visible():
                    visible += 1
            results[name] = {"found": len(els), "visible": visible}
            print(f"  {name}: найдено={len(els)}, видимых={visible}")

        # 2. Анализ бургер-меню (если есть)
        burger = await page.query_selector(
            "button[aria-label*='меню'], button[aria-label*='menu'], .burger, .hamburger, nav button, header button"
        )
        if burger and await burger.is_visible():
            print("\n--- Бургер-меню найдено, кликаем ---")
            await burger.click()
            await asyncio.sleep(1)
            await page.screenshot(path="reports/screenshots/mobile_menu_open.png", full_page=False)
            print("Скриншот меню сохранён: reports/screenshots/mobile_menu_open.png")
            menu_items = await page.query_selector_all("nav a, .menu a, [role='menuitem']")
            print(f"  Пунктов меню: {len(menu_items)}")
            for i, item in enumerate(menu_items[:10]):
                text = await item.text_content()
                href = await item.get_attribute("href")
                print(f"    [{i}] {text.strip()[:40]!r} -> {href}")
            # Закрыть меню
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.5)

        # 3. Анализ поиска
        search_input = await page.query_selector(
            "input[type='search'], input[placeholder*='Поиск'], input[placeholder*='поиск']"
        )
        if search_input:
            print("\n--- Поисковое поле найдено ---")
            print(f"  placeholder: {await search_input.get_attribute('placeholder')}")
            await search_input.fill("Первый")
            await asyncio.sleep(0.5)
            await page.screenshot(path="reports/screenshots/mobile_search_active.png", full_page=False)
            print("Скриншот поиска сохранён: reports/screenshots/mobile_search_active.png")
            # Найти кнопку поиска
            search_btn = await page.query_selector("button[type='submit'], button[aria-label*='Поиск']")
            if search_btn:
                await search_btn.click()
            else:
                await page.keyboard.press("Enter")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path="reports/screenshots/mobile_search_results.png", full_page=True)
            print("Скриншот результатов поиска сохранён: reports/screenshots/mobile_search_results.png")

        # 4. Скролл и проверка футера
        print("\n--- Скролл до футера ---")
        footer = await page.query_selector("footer")
        if footer:
            await footer.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            await page.screenshot(path="reports/screenshots/mobile_footer.png", full_page=False)
            print("Скриншот футера сохранён: reports/screenshots/mobile_footer.png")
            footer_links = await page.query_selector_all("footer a")
            print(f"  Ссылок в футере: {len(footer_links)}")
            for i, link in enumerate(footer_links[:15]):
                text = await link.text_content()
                href = await link.get_attribute("href")
                print(f"    [{i}] {text.strip()[:30]!r} -> {href}")

        # 5. Карточки каналов
        print("\n--- Карточки каналов ---")
        cards = await page.query_selector_all("a[href*='/channel/']")
        print(f"  Найдено карточек: {len(cards)}")
        for i, card in enumerate(cards[:5]):
            text = await card.text_content()
            href = await card.get_attribute("href")
            print(f"    [{i}] {text.strip()[:50]!r} -> {href}")

        # 6. Переключение тёмной темы
        dark_toggle = await page.query_selector(
            "button[aria-label*='тёмн'], button[aria-label*='dark'], [data-testid='dark-mode-toggle']"
        )
        if dark_toggle and await dark_toggle.is_visible():
            print("\n--- Переключение тёмной темы ---")
            await dark_toggle.click()
            await asyncio.sleep(1)
            await page.screenshot(path="reports/screenshots/mobile_dark_mode.png", full_page=False)
            print("Скриншот тёмной темы сохранён: reports/screenshots/mobile_dark_mode.png")

        # 7. Cookie баннер
        cookie = await page.query_selector("[class*='cookie'], .cookie-banner, .cookie-consent")
        if cookie and await cookie.is_visible():
            print("\n--- Cookie баннер ---")
            print(f"  Текст: {(await cookie.text_content())[:200]}")
            await cookie.screenshot(path="reports/screenshots/mobile_cookie_banner.png")
            print("Скриншот cookie баннера сохранён: reports/screenshots/mobile_cookie_banner.png")

        # 8. Анализ schedule страницы
        print("\n=== Анализ страницы расписания (mobile) ===")
        await page.goto(f"{BASE_URL}schedule", wait_until="networkidle")
        await page.screenshot(path="reports/screenshots/mobile_schedule.png", full_page=True)
        print("Скриншот расписания сохранён: reports/screenshots/mobile_schedule.png")

        # Дата-пикер
        date_picker = await page.query_selector("input[type='date'], [data-testid='date-picker']")
        if date_picker:
            print("  Дата-пикер найден")
        else:
            print("  Дата-пикер НЕ найден")

        # 9. Анализ страницы канала
        print("\n=== Анализ страницы канала (mobile) ===")
        channel_links = await page.query_selector_all("a[href*='/channel/']")
        if channel_links:
            first = channel_links[0]
            href = await first.get_attribute("href")
            await page.goto(f"{BASE_URL}{href.lstrip('/')}", wait_until="networkidle")
            await page.screenshot(path="reports/screenshots/mobile_channel_page.png", full_page=True)
            print(f"Скриншот страницы канала сохранён: reports/screenshots/mobile_channel_page.png")

            # Проверка элементов на странице канала
            channel_name = await page.query_selector("h1")
            if channel_name:
                print(f"  Название канала: {(await channel_name.text_content()).strip()[:50]}")

            program_list = await page.query_selector_all("[data-testid='program-item'], .program-item, .program-list > *")
            print(f"  Программ в списке: {len(program_list)}")

        # Сохранить JSON отчёт
        report_path = "reports/mobile_analysis.json"
        import aiofiles
        async with aiofiles.open(report_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(results, ensure_ascii=False, indent=2))
        print(f"\n=== JSON отчёт сохранён: {report_path} ===")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(analyze())
