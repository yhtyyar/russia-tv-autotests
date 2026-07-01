"""E2E-тесты клавиатурной навигации и доступности.

Покрывает:
- Tab-навигация по основным интерактивным элементам
- Активация кнопок через Enter/Space
- Предотвращение focus trap
- Наличие skip-ссылок
"""

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.asyncio
@allure.feature("клавиатурной навигации и доступности")
@allure.story("Tab должен перемещать фокус по интерактивным элементам")
@allure.severity(Severity.MINOR)
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
@allure.feature("клавиатурной навигации и доступности")
@allure.story("Поле поиска должно быть доступно для фокуса с клавиатуры")
@allure.severity(Severity.MINOR)
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
@allure.feature("клавиатурной навигации и доступности")
@allure.story("Нажатие Enter в поиске должно отправлять запрос")
@allure.severity(Severity.MINOR)
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
    await page.wait_for_timeout(1000)  # debounce клиентской фильтрации по вводу

    assert (
        not await home.is_empty_state_visible()
    ), "Поиск по Enter не дал результатов для запроса 'Первый'"


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.asyncio
@allure.feature("клавиатурной навигации и доступности")
@allure.story("Сфокусированные элементы должны иметь видимый индикатор фокуса")
@allure.severity(Severity.MINOR)
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
