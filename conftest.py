"""Pytest fixtures and configuration."""

import logging
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright

import allure
from config.settings import Settings, get_settings
from core.browser_manager import BrowserManager
from core.logger import setup_logging

setup_logging()

logger = logging.getLogger("russia_tv_tests.conftest")

FAILED_KEY = pytest.StashKey[bool]()


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register custom CLI options."""
    parser.addoption(
        "--update-baselines",
        action="store_true",
        default=False,
        help="Update visual regression baseline screenshots",
    )
    parser.addoption(
        "--tracing",
        action="store_true",
        default=False,
        help="Record Playwright traces for failed E2E tests",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> None:
    """Track test outcome for artifact collection in fixture teardown."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        item.stash[FAILED_KEY] = report.failed


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Provide project settings."""
    return get_settings()


@pytest_asyncio.fixture
async def playwright_instance() -> AsyncGenerator[Playwright, None]:
    """Provide Playwright instance for the test."""
    async with async_playwright() as pw:
        yield pw


@pytest_asyncio.fixture
async def browser(playwright_instance: Playwright) -> AsyncGenerator[Browser, None]:
    """Provide launched browser for the test session.

    Поддерживает chromium, firefox, webkit и yandex (через chromium
    с кастомным executable_path).
    """
    from config.browsers import detect_yandex_browser, launch_browser

    s = get_settings()
    if s.browser == "yandex":
        yandex_path = detect_yandex_browser()
        browser_type = playwright_instance.chromium
        b = await launch_browser(
            browser_type=browser_type,
            headless=s.headless,
            slow_mo=s.slow_mo,
            executable_path=yandex_path,
        )
    else:
        browser_type = getattr(
            playwright_instance, s.browser, playwright_instance.chromium
        )
        b = await launch_browser(
            browser_type=browser_type,
            headless=s.headless,
            slow_mo=s.slow_mo,
        )
    yield b
    await b.close()


@pytest_asyncio.fixture
async def context(
    browser: Browser, request: pytest.FixtureRequest
) -> AsyncGenerator[BrowserContext, None]:
    """Provide fresh browser context with video, tracing on failure."""
    tracing_enabled = request.config.getoption("--tracing")
    ctx = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="reports/videos",
    )
    if tracing_enabled:
        await ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    if tracing_enabled and request.node.stash.get(FAILED_KEY, False):
        trace_path = f"reports/traces/{request.node.name}.zip"
        os.makedirs("reports/traces", exist_ok=True)
        await ctx.tracing.stop(path=trace_path)
        allure.attach.file(
            trace_path, name="trace", attachment_type=allure.attachment_type.ZIP
        )
    await ctx.close()


@pytest_asyncio.fixture
async def mobile_context(
    browser: Browser, request: pytest.FixtureRequest
) -> AsyncGenerator[BrowserContext, None]:
    """Provide fresh mobile browser context with video, tracing on failure."""
    tracing_enabled = request.config.getoption("--tracing")
    ctx = await browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
            "Mobile/15E148 Safari/604.1"
        ),
        is_mobile=True,
        has_touch=True,
        device_scale_factor=3,
        record_video_dir="reports/videos",
    )
    if tracing_enabled:
        await ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    if tracing_enabled and request.node.stash.get(FAILED_KEY, False):
        trace_path = f"reports/traces/{request.node.name}.zip"
        os.makedirs("reports/traces", exist_ok=True)
        await ctx.tracing.stop(path=trace_path)
        allure.attach.file(
            trace_path, name="trace", attachment_type=allure.attachment_type.ZIP
        )
    await ctx.close()


@pytest_asyncio.fixture
async def page(
    context: BrowserContext, request: pytest.FixtureRequest
) -> AsyncGenerator[Page, None]:
    """Provide fresh page; save screenshot + video to Allure on failure."""
    p = await context.new_page()
    yield p
    failed = request.node.stash.get(FAILED_KEY, False)
    if failed:
        os.makedirs("reports/screenshots", exist_ok=True)
        screenshot_path = f"reports/screenshots/{request.node.name}.png"
        try:
            await p.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(
                screenshot_path,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as exc:
            logger.warning("Screenshot failed: %s", exc)
    if p.video:
        try:
            video_path = await p.video.path()
            if video_path and os.path.exists(video_path):
                allure.attach.file(
                    video_path,
                    name="video_recording",
                    attachment_type=allure.attachment_type.WEBM,
                )
        except Exception as exc:
            logger.warning("Video attach failed: %s", exc)
    await p.close()


@pytest_asyncio.fixture
async def mobile_page(
    mobile_context: BrowserContext, request: pytest.FixtureRequest
) -> AsyncGenerator[Page, None]:
    """Provide fresh mobile page; save screenshot + video to Allure on failure."""
    p = await mobile_context.new_page()
    yield p
    failed = request.node.stash.get(FAILED_KEY, False)
    if failed:
        os.makedirs("reports/screenshots", exist_ok=True)
        screenshot_path = f"reports/screenshots/{request.node.name}.png"
        try:
            await p.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(
                screenshot_path,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as exc:
            logger.warning("Screenshot failed: %s", exc)
    if p.video:
        try:
            video_path = await p.video.path()
            if video_path and os.path.exists(video_path):
                allure.attach.file(
                    video_path,
                    name="video_recording",
                    attachment_type=allure.attachment_type.WEBM,
                )
        except Exception as exc:
            logger.warning("Video attach failed: %s", exc)
    await p.close()


@pytest_asyncio.fixture
async def browser_manager(
    playwright_instance: Playwright,
) -> AsyncGenerator[BrowserManager, None]:
    """Provide BrowserManager for direct control."""
    manager = BrowserManager(playwright_instance)
    try:
        yield manager
    finally:
        await manager.close()


SEVERITY_MAP = {
    "smoke": "CRITICAL",
    "accessibility": "MINOR",
    "error_handling": "NORMAL",
    "state_transition": "NORMAL",
    "performance": "NORMAL",
    "visual": "MINOR",
    "responsive": "NORMAL",
    "dark_mode": "NORMAL",
    "cookie": "NORMAL",
    "seo": "NORMAL",
    "footer": "NORMAL",
    "load_more": "NORMAL",
    "empty_state": "NORMAL",
    "keyboard": "NORMAL",
    "channel": "NORMAL",
    "date_picker": "NORMAL",
    "yandex": "NORMAL",
}

FEATURE_MAP = {
    "test_home_page": "Главная страница",
    "test_search_edge_cases": "Поиск",
    "test_state_navigation": "Навигация",
    "test_footer_links": "Футер",
    "test_dark_mode": "Тёмная тема",
    "test_cookie_consent": "Cookie-баннер",
    "test_accessibility": "Доступность",
    "test_error_pages": "Обработка ошибок",
    "test_responsive": "Адаптивный дизайн",
    "test_seo_meta": "SEO",
    "test_schedule_navigation": "Расписание",
    "test_channel_detail": "Страница канала",
    "test_channel_filtering": "Фильтрация каналов",
    "test_load_more": "Пагинация",
    "test_empty_states": "Пустые состояния",
    "test_keyboard_navigation": "Клавиатурная навигация",
    "test_date_picker": "Выбор даты",
    "test_visual_regression": "Визуальная регрессия",
    "test_mobile_home": "Мобильная версия",
    "test_mobile_navigation": "Мобильная навигация",
}


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Dynamically add Allure metadata based on file name and markers."""
    for item in items:
        if not item.nodeid.startswith("tests/e2e/"):
            continue

        # Feature from file name
        module_name = item.module.__name__.split(".")[-1]
        feature = FEATURE_MAP.get(module_name, "E2E Тесты")
        item.add_marker(pytest.mark.allure_test(feature))

        # Story from test docstring or name
        story = item.obj.__doc__ or item.name.replace("test_", "").replace("_", " ")
        story = story.strip().split("\n")[0][:80]

        # Severity from markers
        severity = "NORMAL"
        for marker in item.iter_markers():
            if marker.name in SEVERITY_MAP:
                severity = SEVERITY_MAP[marker.name]
                break

        # Apply via dynamic Allure API if available
        try:
            import allure
            allure.dynamic.feature(feature)
            allure.dynamic.story(story)
            allure.dynamic.severity(getattr(allure.severity_level, severity))
        except Exception:
            pass


@pytest.fixture(autouse=True)
def _env_setup() -> None:
    """Ensure required directories exist before each test."""
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/html-report", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)
    os.makedirs("reports/traces", exist_ok=True)
