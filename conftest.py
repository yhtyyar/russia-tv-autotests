"""Pytest fixtures and configuration."""

import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright

from config.settings import Settings, get_settings
from core.browser_manager import BrowserManager


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
    """Provide launched browser for the test session."""
    from config.browsers import launch_browser

    s = get_settings()
    browser_type = getattr(playwright_instance, s.browser, playwright_instance.chromium)
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
    """Provide fresh browser context for each test with optional tracing."""
    tracing_enabled = request.config.getoption("--tracing")
    ctx = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
    )
    if tracing_enabled:
        await ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    if tracing_enabled and request.node.rep_call.failed:
        trace_path = f"reports/traces/{request.node.name}.zip"
        os.makedirs("reports/traces", exist_ok=True)
        await ctx.tracing.stop(path=trace_path)
    await ctx.close()


@pytest_asyncio.fixture
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """Provide fresh page for each test."""
    p = await context.new_page()
    yield p
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


@pytest.fixture(autouse=True)
def _env_setup() -> None:
    """Ensure required directories exist before each test."""
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/html-report", exist_ok=True)
