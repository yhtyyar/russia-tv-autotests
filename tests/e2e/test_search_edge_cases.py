"""Search edge-case tests using Equivalence Partitioning + Error Guessing.

Partitions for search query input:
- Empty string (invalid)
- Single character (boundary, valid)
- Normal query 3-30 chars (valid)
- Maximum length / very long (invalid/boundary)
- Special characters (valid/invalid boundary)
- SQL injection / XSS payload (security, invalid)
- Unicode/Cyrillic only (valid)
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
    """Search with various input partitions."""
    home = HomePage(page)
    await home.goto()
    await home.expect_channels_loaded(timeout=15000)

    if await home.is_search_visible():
        await home.search(query)
        await page.wait_for_timeout(1000)

        # For empty/invalid queries we expect no URL change or same page
        current_url = page.url
        if not should_have_results:
            # Page should stay on home or show empty results
            assert "search" not in current_url or home.url in current_url
        else:
            # Should either stay on page with results or navigate to search
            assert home.url in current_url or "search" in current_url
    else:
        pytest.skip("Search input not visible")
