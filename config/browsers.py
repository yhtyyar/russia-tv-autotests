"""Browser launch configuration helpers."""

from typing import Any

from playwright.async_api import Browser, BrowserType


def get_browser_launch_args(
    headless: bool = True,
    slow_mo: int = 0,
) -> dict[str, Any]:
    """Build Playwright browser launch arguments.

    Args:
        headless: Run browser in headless mode.
        slow_mo: Slow down operations by specified milliseconds.

    Returns:
        Dictionary of launch options for Playwright.
    """
    args = {
        "headless": headless,
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
    }
    if slow_mo > 0:
        args["slow_mo"] = slow_mo
    return args


async def launch_browser(
    browser_type: BrowserType,
    headless: bool = True,
    slow_mo: int = 0,
) -> Browser:
    """Launch a browser instance with project defaults.

    Args:
        browser_type: Playwright BrowserType instance.
        headless: Run browser in headless mode.
        slow_mo: Slow down operations by specified milliseconds.

    Returns:
        Launched Browser instance.
    """
    launch_options = get_browser_launch_args(headless, slow_mo)
    return await browser_type.launch(**launch_options)
