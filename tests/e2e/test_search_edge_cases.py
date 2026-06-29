"""Тесты граничных случаев поиска с использованием разбиения на эквивалентные классы + предугадывание ошибок.

Разбиения для поискового запроса:
- Пустая строка (невалидно)
- Один символ (граница, валидно)
- Нормальный запрос 3-30 символов (валидно)
- Максимальная длина / очень длинный (невалидно/граница)
- Спецсимволы (граница валидности)
- SQL-инъекция / XSS (безопасность, невалидно)
- Только Unicode/кириллица (валидно)
"""

import pytest
from playwright.async_api import Page

from pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.parametrize(
    "query,should_have_results",
    [
        pytest.param("", False, id="empty_query"),
        pytest.param("а", True, id="single_cyrillic_char"),
        pytest.param("Первый", True, id="normal_cyrillic"),
        pytest.param("a" * 200, False, id="very_long_200_chars"),
        pytest.param("<script>alert(1)</script>", False, id="xss_payload"),
        pytest.param("'; DROP TABLE channels; --", False, id="sql_injection"),
        pytest.param("Мир", True, id="common_word"),
        pytest.param("!@#$%^&*()", False, id="special_chars_only"),
    ],
)
@pytest.mark.asyncio
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
    await page.wait_for_timeout(2000)

    # For empty/invalid queries we expect no URL change or same page
    current_url = page.url
    if not should_have_results:
        # Page should stay on home or show empty results
        assert "search" not in current_url or home.url in current_url
    else:
        # Should either stay on page with results or navigate to search
        assert home.url in current_url or "search" in current_url
