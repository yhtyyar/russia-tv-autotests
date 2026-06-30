"""Расширенный анализ мобильной версии russia-tv.online."""

import asyncio
import json

from playwright.async_api import async_playwright

BASE_URL = "https://russia-tv.online/"
VIEWPORT = {"width": 390, "height": 844}


async def dump_elements(page, selector: str, label: str, max_items: int = 10) -> None:
    """Вывести информацию об элементах по селектору."""
    els = await page.query_selector_all(selector)
    print(f"\n--- {label} ({len(els)} шт.) ---")
    for i, el in enumerate(els[:max_items]):
        tag = await el.evaluate("e => e.tagName")
        text = (await el.text_content() or "").strip()[:60]
        classes = await el.get_attribute("class") or ""
        testid = await el.get_attribute("data-testid") or ""
        href = await el.get_attribute("href") or ""
        visible = await el.is_visible()
        print(f"  [{i}] <{tag}> class='{classes[:50]}' data-testid='{testid}' text='{text}' href='{href}' visible={visible}")


async def analyze() -> None:
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

        print("=== Главная страница (mobile viewport 390×844) ===")
        await page.goto(BASE_URL, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # 1. Структура header
        await dump_elements(page, "header *", "Header content", 20)

        # 2. Все кнопки
        await dump_elements(page, "button", "All buttons", 15)

        # 3. Все ссылки
        await dump_elements(page, "a", "All links", 20)

        # 4. Все input
        await dump_elements(page, "input, textarea", "All inputs", 10)

        # 5. Карточки каналов - ищем по ссылкам на /channel/
        await dump_elements(page, "a[href*='/channel/']", "Channel card links", 20)

        # 6. Основной контент
        await dump_elements(page, "main *", "Main content elements", 20)

        # 7. Footer
        await dump_elements(page, "footer *", "Footer elements", 15)

        # 8. Cookie баннер (любые элементы с cookie в классе/id)
        cookie_el = await page.query_selector("[class*='cookie'], [id*='cookie'], [class*='consent'], [id*='consent']")
        if cookie_el:
            print("\n--- Cookie баннер ---")
            print(await cookie_el.inner_html())
        else:
            print("\n--- Cookie баннер: НЕ НАЙДЕН ---")

        # 9. Бургер-меню - клик и дамп
        burger = await page.query_selector("button[class*='burger'], button[class*='menu'], header button, [aria-label*='меню'], [aria-label*='menu']")
        if burger:
            print("\n--- Клик по бургер-меню ---")
            await burger.click()
            await asyncio.sleep(1)
            await dump_elements(page, "nav a, [role='dialog'] a, .menu a", "Menu items after click", 20)
            # Закрыть
            await page.keyboard.press("Escape")

        # 10. Клик по поиску
        search_btn = await page.query_selector("button[class*='search'], button[aria-label*='Поиск'], button[aria-label*='search']")
        if search_btn:
            print("\n--- Клик по кнопке поиска ---")
            await search_btn.click()
            await asyncio.sleep(1)
            await dump_elements(page, "input", "Inputs after search click", 5)

        # 11. Дамп HTML body (сокращённый)
        body_html = await page.content()
        print(f"\n=== Размер HTML: {len(body_html)} символов ===")
        # Сохранить полный HTML
        import aiofiles
        async with aiofiles.open("reports/mobile_body.html", "w", encoding="utf-8") as f:
            await f.write(body_html)
        print("HTML сохранён в reports/mobile_body.html")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(analyze())
