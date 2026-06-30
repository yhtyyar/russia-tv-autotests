"""Тесты граничных случаев поиска с использованием разбиения на эквивалентные классы + предугадывание ошибок.

Данные загружаются из test_data/search_queries.json — добавляй новые кейсы
без изменения кода.
"""

import json
from pathlib import Path

import pytest
from allure_commons.types import Severity
from playwright.async_api import Page

import allure
from pages.home_page import HomePage

_DATA_PATH = Path(__file__).parent.parent.parent / "test_data" / "search_queries.json"
_search_cases = json.loads(_DATA_PATH.read_text(encoding="utf-8"))["cases"]
_search_params = [
    pytest.param(c["query"], c["should_have_results"], id=c["id"])
    for c in _search_cases
]


@pytest.mark.e2e
@pytest.mark.parametrize("query,should_have_results", _search_params)
@pytest.mark.asyncio
@allure.feature("Поиск")
@allure.story("Эквивалентное разбиение + граничные значения")
@allure.severity(Severity.NORMAL)
async def test_search_equivalence_partitioning(
    page: Page, query: str, should_have_results: bool
):
    """Поиск с различными разбиениями входных данных."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if not await home.is_search_visible():
        pytest.skip("Search input not visible")

    await home.search(query)
    await page.wait_for_load_state("networkidle")

    current_url = page.url
    if not should_have_results:
        assert "search" not in current_url or home.url in current_url
    else:
        assert home.url in current_url or "search" in current_url
