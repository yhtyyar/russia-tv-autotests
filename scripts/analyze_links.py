"""Быстрый анализ всех ссылок на главной странице mobile."""

import asyncio

from playwright.async_api import async_playwright

BASE_URL = "https://russia-tv.online/"


async def analyze() -> None:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
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

        await page.goto(BASE_URL, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        print("=== Все ссылки (первые 30) ===")
        links = await page.query_selector_all("a")
        for i, link in enumerate(links[:30]):
            href = await link.get_attribute("href") or ""
            text = (await link.text_content() or "").strip()[:50]
            visible = await link.is_visible()
            print(f"  [{i}] href={href!r:60} text={text!r:40} visible={visible}")

        print("\n=== Все кнопки (первые 20) ===")
        buttons = await page.query_selector_all("button")
        for i, btn in enumerate(buttons[:20]):
            text = (await btn.text_content() or "").strip()[:50]
            aria = await btn.get_attribute("aria-label") or ""
            classes = await btn.get_attribute("class") or ""
            visible = await btn.is_visible()
            print(f"  [{i}] text={text!r:30} aria={aria!r:30} class={classes[:40]!r} visible={visible}")

        print("\n=== Все изображения (первые 20) ===")
        imgs = await page.query_selector_all("img")
        for i, img in enumerate(imgs[:20]):
            src = await img.get_attribute("src") or ""
            alt = await img.get_attribute("alt") or ""
            visible = await img.is_visible()
            print(f"  [{i}] src={src[:60]!r} alt={alt!r} visible={visible}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(analyze())
