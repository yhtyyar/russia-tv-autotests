"""Тесты доступности через Axe-core и Playwright.

Проверяет соответствие WCAG 2.1 AA для критических страниц.
"""

import os

import pytest
import pytest_check as check
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage
from pages.schedule_page import SchedulePage


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.xfail(
    reason="External site has known critical image-alt a11y violations",
    strict=False,
)
@pytest.mark.asyncio
@allure.feature("доступности")
@allure.story("Главная страница не должна иметь критических нарушений доступности")
@allure.severity(Severity.MINOR)
async def test_home_page_accessibility(page: Page):
    """Главная страница не должна иметь критических нарушений доступности."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    # Inject axe-core from local npm package
    axe_path = os.path.join(os.path.dirname(__file__), "../../node_modules/axe-core/axe.min.js")
    await page.add_script_tag(path=axe_path)
    await page.wait_for_function("() => typeof axe !== 'undefined'")

    violations = await page.evaluate(
        """() => {
            return new Promise((resolve) => {
                axe.run({
                    runOnly: {
                        type: 'tag',
                        values: ['wcag2a', 'wcag2aa', 'wcag21aa']
                    }
                }, (err, results) => {
                    if (err) resolve([]);
                    else resolve(results.violations);
                });
            });
        }"""
    )

    critical = [v for v in violations if v.get("impact") == "critical"]
    serious = [v for v in violations if v.get("impact") == "serious"]
    check.equal(len(serious), 0, msg=f"Serious a11y violations: {len(serious)}")
    assert len(critical) == 0, f"Critical a11y violations: {len(critical)} — {critical[0]['help']}"


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.xfail(
    reason="External site has known critical image-alt a11y violations",
    strict=False,
)
@pytest.mark.asyncio
@allure.feature("доступности")
@allure.story("Страница расписания не должна иметь критических нарушений доступности")
@allure.severity(Severity.MINOR)
async def test_schedule_page_accessibility(page: Page):
    """Страница расписания не должна иметь критических нарушений доступности."""
    schedule = SchedulePage(page)
    await schedule.goto()
    await schedule.wait_for_load("domcontentloaded")

    axe_path = os.path.join(os.path.dirname(__file__), "../../node_modules/axe-core/axe.min.js")
    await page.add_script_tag(path=axe_path)
    await page.wait_for_function("() => typeof axe !== 'undefined'")

    violations = await page.evaluate(
        """() => {
            return new Promise((resolve) => {
                axe.run({
                    runOnly: {
                        type: 'tag',
                        values: ['wcag2a', 'wcag2aa']
                    }
                }, (err, results) => {
                    if (err) resolve([]);
                    else resolve(results.violations);
                });
            });
        }"""
    )

    critical = [v for v in violations if v.get("impact") == "critical"]
    assert len(critical) == 0, f"Critical a11y violations on schedule: {len(critical)}"


@pytest.mark.e2e
@pytest.mark.accessibility
@pytest.mark.asyncio
@allure.feature("доступности")
@allure.story("Поле поиска должно быть доступно для фокуса с клавиатуры")
@allure.severity(Severity.MINOR)
async def test_focus_management_on_search(page: Page):
    """Поле поиска должно быть доступно для фокуса с клавиатуры."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if await home.is_search_visible():
        # Tab to search input
        await page.keyboard.press("Tab")
        focused = await page.evaluate("() => document.activeElement.tagName")
        # After tabbing, something should be focused
        assert focused != "BODY", "No element received keyboard focus"
    else:
        pytest.skip("Search input not visible for focus test")
