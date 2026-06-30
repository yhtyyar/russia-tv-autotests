"""E2E-тесты Web Vitals через Playwright PerformanceObserver.

Бюджеты (Core Web Vitals):
- LCP (Largest Contentful Paint): < 2.5 s
- CLS (Cumulative Layout Shift): < 0.1
- FCP (First Contentful Paint): < 1.8 s
- TTFB (Time to First Byte): < 0.6 s
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage
from pages.schedule_page import SchedulePage

_HISTORY_PATH = Path("reports/performance/history.json")


def _save_vitals(page_name: str, vitals: dict) -> None:
    """Append vitals to performance history JSON."""
    _HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    history: list = []
    if _HISTORY_PATH.exists():
        history = json.loads(_HISTORY_PATH.read_text(encoding="utf-8"))
    # Find today's entry or create new
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = {"timestamp": today, "pages": {page_name: vitals}}
    history.append(entry)
    # Keep last 50 runs
    history = history[-50:]
    _HISTORY_PATH.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


# Thresholds per Google Core Web Vitals
VITALS_BUDGET = {
    "LCP": 2500,   # ms
    "CLS": 0.1,
    "FCP": 1800,   # ms
    "TTFB": 600,   # ms
}


VITALS_SCRIPT = """
() => {
    return new Promise((resolve) => {
        const metrics = {};
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.entryType === "largest-contentful-paint") {
                    metrics.LCP = entry.startTime;
                }
                if (entry.entryType === "layout-shift" && !entry.hadRecentInput) {
                    metrics.CLS = (metrics.CLS || 0) + entry.value;
                }
                if (entry.entryType === "paint" && entry.name === "first-contentful-paint") {
                    metrics.FCP = entry.startTime;
                }
            }
        });
        observer.observe({ type: "largest-contentful-paint", buffered: true });
        observer.observe({ type: "layout-shift", buffered: true });
        observer.observe({ type: "paint", buffered: true });
        setTimeout(() => {
            observer.disconnect();
            // Also grab navigation timing for TTFB
            const nav = performance.getEntriesByType("navigation")[0];
            if (nav) {
                metrics.TTFB = nav.responseStart - nav.startTime;
            }
            resolve(metrics);
        }, 5000);
    });
}
"""


@pytest.mark.e2e
@pytest.mark.performance
@pytest.mark.asyncio
async def test_home_page_web_vitals(page: Page):
    """Главная страница должна укладываться в Core Web Vitals."""
    home = HomePage(page)
    await home.goto(wait_until="networkidle")
    await home.expect_channels_loaded(timeout=15000)

    vitals = await page.evaluate(VITALS_SCRIPT)
    _save_vitals("Главная", vitals)

    assert vitals.get("FCP", float("inf")) < VITALS_BUDGET["FCP"], (
        f"FCP {vitals.get('FCP')}ms exceeds budget {VITALS_BUDGET['FCP']}ms"
    )
    assert vitals.get("LCP", float("inf")) < VITALS_BUDGET["LCP"], (
        f"LCP {vitals.get('LCP')}ms exceeds budget {VITALS_BUDGET['LCP']}ms"
    )
    assert vitals.get("CLS", float("inf")) < VITALS_BUDGET["CLS"], (
        f"CLS {vitals.get('CLS')} exceeds budget {VITALS_BUDGET['CLS']}"
    )
    assert vitals.get("TTFB", float("inf")) < VITALS_BUDGET["TTFB"], (
        f"TTFB {vitals.get('TTFB')}ms exceeds budget {VITALS_BUDGET['TTFB']}ms"
    )


@pytest.mark.e2e
@pytest.mark.performance
@pytest.mark.asyncio
async def test_schedule_page_web_vitals(page: Page):
    """Страница расписания должна укладываться в Core Web Vitals."""
    schedule = SchedulePage(page)
    await schedule.goto(wait_until="networkidle")
    await schedule.wait_for_load("domcontentloaded")

    vitals = await page.evaluate(VITALS_SCRIPT)
    _save_vitals("Расписание", vitals)

    assert vitals.get("FCP", float("inf")) < VITALS_BUDGET["FCP"], (
        f"FCP {vitals.get('FCP')}ms exceeds budget {VITALS_BUDGET['FCP']}ms"
    )
    assert vitals.get("LCP", float("inf")) < VITALS_BUDGET["LCP"], (
        f"LCP {vitals.get('LCP')}ms exceeds budget {VITALS_BUDGET['LCP']}ms"
    )
    assert vitals.get("CLS", float("inf")) < VITALS_BUDGET["CLS"], (
        f"CLS {vitals.get('CLS')} exceeds budget {VITALS_BUDGET['CLS']}"
    )
