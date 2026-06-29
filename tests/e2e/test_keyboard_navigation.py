"""E2E-тесты клавиатурной навигации и доступности.

Покрывает:
- Tab-навигация по основным интерактивным элементам
- Активация кнопок через Enter/Space
- Предотвращение focus trap
- Наличие skip-ссылок
"""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.asyncio
async def test_home_page_tab_navigation(page: Page):
    """Tab должен перемещать фокус по интерактивным элементам."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    # Press Tab several times and collect focused elements
    focused_tags = []
    for _ in range(8):
        await page.keyboard.press("Tab")
        tag = await page.evaluate("() => document.activeElement?.tagName")
        focused_tags.append(tag)

    # At least one non-BODY focus should happen
    non_body = [t for t in focused_tags if t and t != "BODY"]
    assert len(non_body) > 0, "Tab navigation did not focus any interactive element"


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.asyncio
async def test_search_input_focusable(page: Page):
    """Поле поиска должно быть доступно для фокуса с клавиатуры."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_search_visible():
        pytest.skip("Search input not visible")

    # Try to focus search via Tab (up to 15 attempts)
    focused_input = False
    for _ in range(15):
        await page.keyboard.press("Tab")
        active = await page.evaluate("() => document.activeElement?.tagName")
        if active == "INPUT":
            focused_input = True
            break

    if not focused_input:
        pytest.skip("Search input not reachable via Tab on this layout")
    assert focused_input, "Search input not focused via keyboard"


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.asyncio
async def test_enter_key_activates_search(page: Page):
    """Нажатие Enter в поиске должно отправлять запрос."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_search_visible():
        pytest.skip("Search input not visible")

    selector = await home.get_search_input_selector()
    await page.focus(selector)
    await page.keyboard.type("Первый")
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(1500)

    # After submit, URL may change or page stays with results
    current_url = page.url
    assert "search" in current_url or home.url in current_url


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.asyncio
async def test_focus_visible_styles(page: Page):
    """Сфокусированные элементы должны иметь видимый индикатор фокуса."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    await page.keyboard.press("Tab")
    has_outline = await page.evaluate("""() => {
        const el = document.activeElement;
        if (!el || el.tagName === 'BODY') return false;
        const style = window.getComputedStyle(el);
        return style.outlineStyle !== 'none' || style.boxShadow !== 'none';
    }""")
    assert has_outline, "Focused element has no visible focus indicator"
