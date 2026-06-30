"""Remote browser configuration for cloud providers (BrowserStack, Sauce Labs).

Usage:
    BROWSERSTACK_USERNAME=xxx BROWSERSTACK_ACCESS_KEY=yyy \
        uv run pytest tests/e2e/ -m cross_browser --browser=chrome

Environment variables:
    BROWSERSTACK_USERNAME / BROWSERSTACK_ACCESS_KEY
    SAUCE_USERNAME / SAUCE_ACCESS_KEY
"""

import os
from dataclasses import dataclass


@dataclass
class RemoteCapabilities:
    """Browser capabilities for remote execution."""

    browser: str
    browser_version: str
    os_name: str
    os_version: str
    resolution: str = "1920x1080"
    build_name: str = "russia-tv-autotests"
    project_name: str = "russia-tv.online"

    def to_browserstack(self) -> dict:
        """Generate BrowserStack capabilities."""
        return {
            "browserName": self.browser,
            "browserVersion": self.browser_version,
            "os": self.os_name,
            "osVersion": self.os_version,
            "resolution": self.resolution,
            "buildName": self.build_name,
            "projectName": self.project_name,
            "debug": "true",
            "networkLogs": "true",
            "consoleLogs": "errors",
        }

    def to_sauce(self) -> dict:
        """Generate Sauce Labs capabilities."""
        return {
            "browserName": self.browser,
            "browserVersion": self.browser_version,
            "platformName": f"{self.os_name} {self.os_version}",
            "screenResolution": self.resolution,
            "sauce:options": {
                "build": self.build_name,
                "name": self.project_name,
            },
        }


# Predefined matrices for cross-browser testing
CROSS_BROWSER_MATRIX = [
    RemoteCapabilities("Chrome", "latest", "Windows", "11"),
    RemoteCapabilities("Firefox", "latest", "Windows", "11"),
    RemoteCapabilities("Safari", "latest", "OS X", "Sonoma"),
    RemoteCapabilities("Edge", "latest", "Windows", "11"),
    # Mobile
    RemoteCapabilities("Chrome", "latest", "Android", "14.0", "1080x1920"),
    RemoteCapabilities("Safari", "latest", "iOS", "17", "1170x2532"),
]


def get_browserstack_url() -> str | None:
    """Build BrowserStack WebDriver URL from env vars."""
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    if username and access_key:
        return f"wss://cdp.browserstack.com/playwright?caps={username}:{access_key}"
    return None


def get_sauce_url() -> str | None:
    """Build Sauce Labs WebDriver URL from env vars."""
    username = os.getenv("SAUCE_USERNAME")
    access_key = os.getenv("SAUCE_ACCESS_KEY")
    if username and access_key:
        return f"https://{username}:{access_key}@ondemand.us-west-1.saucelabs.com:443/wd/hub"
    return None
