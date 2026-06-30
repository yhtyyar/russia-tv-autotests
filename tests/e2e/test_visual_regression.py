"""Тесты визуальной регрессии с помощью скриншотов Playwright.

Базовые скриншоты хранятся в reports/screenshots/baseline/.
Запускайте с --update-baselines для обновления референсных изображений.
"""

from pathlib import Path

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage
from utils.image_diff import compare_images

BASELINE_DIR = Path("reports/screenshots/baseline")
ACTUAL_DIR = Path("reports/screenshots/actual")
DIFF_DIR = Path("reports/screenshots/diff")

THRESHOLD = 0.2  # Max allowed pixel diff ratio (20%)


def _ensure_dirs() -> None:
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    ACTUAL_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def _setup_visual_dirs() -> None:
    _ensure_dirs()


@pytest.fixture
async def page_mobile(page: Page):
    """Вернуть страницу, настроенную для мобильного вьюпорта."""
    await page.set_viewport_size({"width": 375, "height": 667})
    yield page


@pytest.mark.e2e
@pytest.mark.visual
@pytest.mark.asyncio
@allure.feature("визуальной регрессии с помощью скриншотов Playwright")
@allure.story("Сделать и сравнить скриншот главной страницы на десктопе")
@allure.severity(Severity.MINOR)
async def test_home_page_desktop_baseline(
    page: Page, request: pytest.FixtureRequest
):
    """Сделать и сравнить скриншот главной страницы на десктопе."""
    baseline = BASELINE_DIR / "home_desktop.png"
    actual = ACTUAL_DIR / "home_desktop.png"

    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    # Mask dynamic elements: time, weather, ads, counters, marquees
    mask_selectors = [
        '[class*="time" i]', '[class*="clock" i]', '[class*="weather" i]',
        '[class*="ad" i]', '[class*="banner" i]', '[class*="counter" i]',
        '[class*="marquee" i]', '[class*="ticker" i]', '[id*="ads" i]',
    ]
    mask_locators = [page.locator(sel) for sel in mask_selectors]

    await page.screenshot(
        path=str(actual),
        full_page=True,
        mask=mask_locators,
        animations="disabled",
    )

    if request.config.getoption("--update-baselines"):
        actual.rename(baseline)
        pytest.skip("Baseline updated")

    if not baseline.exists():
        pytest.fail(
            f"Baseline not found: {baseline}. "
            "Run with --update-baselines"
        )

    is_match, diff_ratio = compare_images(baseline, actual, THRESHOLD)
    assert is_match, (
        f"Visual diff ratio {diff_ratio:.2%} exceeds "
        f"threshold {THRESHOLD:.0%}"
    )


@pytest.mark.e2e
@pytest.mark.visual
@pytest.mark.asyncio
@allure.feature("визуальной регрессии с помощью скриншотов Playwright")
@allure.story("Сделать и сравнить скриншот главной страницы на мобильном")
@allure.severity(Severity.MINOR)
async def test_home_page_mobile_baseline(
    page_mobile: Page, request: pytest.FixtureRequest
):
    """Сделать и сравнить скриншот главной страницы на мобильном."""
    baseline = BASELINE_DIR / "home_mobile.png"
    actual = ACTUAL_DIR / "home_mobile.png"

    home = HomePage(page_mobile)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    mask_selectors = [
        '[class*="time" i]', '[class*="clock" i]', '[class*="weather" i]',
        '[class*="ad" i]', '[class*="banner" i]', '[class*="counter" i]',
        '[class*="marquee" i]', '[class*="ticker" i]', '[id*="ads" i]',
    ]
    mask_locators = [page_mobile.locator(sel) for sel in mask_selectors]

    await page_mobile.screenshot(
        path=str(actual),
        full_page=True,
        mask=mask_locators,
        animations="disabled",
    )

    if request.config.getoption("--update-baselines"):
        actual.rename(baseline)
        pytest.skip("Baseline updated")

    if not baseline.exists():
        pytest.fail(
            f"Baseline not found: {baseline}. "
            "Run with --update-baselines"
        )

    is_match, diff_ratio = compare_images(baseline, actual, THRESHOLD)
    assert is_match, (
        f"Visual diff ratio {diff_ratio:.2%} exceeds "
        f"threshold {THRESHOLD:.0%}"
    )
