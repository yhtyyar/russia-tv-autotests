"""Self-healing selectors: fallback strategies when primary selector fails.

Usage in Page Object:
    from core.self_healing import SelfHealingLocator

    _SEARCH_INPUT = "input[aria-label='Поиск']"
    _SEARCH_FALLBACKS = [
        "input[type='search']",
        "input[placeholder*='поиск' i]",
        "input[name='q']",
    ]

    async def find_search_input(self) -> Locator:
        return await SelfHealingLocator(
            self.page, self._SEARCH_INPUT, self._SEARCH_FALLBACKS
        ).find()
"""

import logging
from typing import Protocol

from playwright.async_api import Locator, Page

logger = logging.getLogger("russia_tv_tests.self_healing")


class FallbackStrategy(Protocol):
    """Protocol for fallback locator strategies."""

    async def try_find(self, page: Page, selector: str) -> Locator | None:
        """Try to find element using this strategy."""
        ...


class CssPartialMatchFallback:
    """Try partial CSS class match."""

    async def try_find(self, page: Page, selector: str) -> Locator | None:
        if "[" not in selector or "]" not in selector:
            return None
        # Extract attribute name, e.g. aria-label
        attr = selector.split("[")[1].split("=")[0]
        value = selector.split("=")[1].strip("'\"") if "=" in selector else ""
        # Try partial match
        partial = f"[{attr}*='{value}' i]"
        loc = page.locator(partial)
        if await loc.count() > 0:
            return loc.first
        return None


class TextContentFallback:
    """Try finding by text content."""

    async def try_find(self, page: Page, selector: str) -> Locator | None:
        # Extract text from aria-label or button value
        texts = []
        if "aria-label=" in selector:
            text = selector.split("aria-label=")[1].split("]")[0].strip("'\"")
            texts.append(text)
        # Try has-text selector
        for text in texts:
            loc = page.locator(f"*:has-text('{text}')")
            if await loc.count() > 0:
                return loc.first
        return None


class RoleFallback:
    """Try finding by ARIA role."""

    async def try_find(self, page: Page, selector: str) -> Locator | None:
        role_map = {
            "input[type='search']": "searchbox",
            "button": "button",
            "a": "link",
            "nav": "navigation",
        }
        for pattern, role in role_map.items():
            if pattern in selector:
                loc = page.get_by_role(role)
                if await loc.count() > 0:
                    return loc.first
        return None


class SelfHealingLocator:
    """Locator with automatic fallback strategies."""

    DEFAULT_STRATEGIES: list[FallbackStrategy] = [
        CssPartialMatchFallback(),
        TextContentFallback(),
        RoleFallback(),
    ]

    def __init__(
        self,
        page: Page,
        primary: str,
        fallbacks: list[str] | None = None,
        strategies: list[FallbackStrategy] | None = None,
    ) -> None:
        self.page = page
        self.primary = primary
        self.fallbacks = fallbacks or []
        self.strategies = strategies or list(self.DEFAULT_STRATEGIES)

    async def find(self, timeout: int = 5000) -> Locator:
        """Find element, trying fallbacks if primary fails."""
        # Try primary first
        primary_loc = self.page.locator(self.primary)
        try:
            await primary_loc.wait_for(state="attached", timeout=timeout)
            return primary_loc
        except Exception:
            logger.warning("Primary selector failed: %s", self.primary)

        # Try explicit fallback selectors
        for fb in self.fallbacks:
            loc = self.page.locator(fb)
            try:
                await loc.wait_for(state="attached", timeout=timeout)
                logger.info("Healed with fallback selector: %s", fb)
                return loc
            except Exception:
                continue

        # Try dynamic strategies
        for strategy in self.strategies:
            result = await strategy.try_find(self.page, self.primary)
            if result is not None:
                logger.info("Healed with strategy: %s", type(strategy).__name__)
                return result

        # Nothing worked, return primary for proper error
        logger.error("All healing strategies failed for: %s", self.primary)
        return primary_loc
