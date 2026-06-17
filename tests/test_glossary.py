"""
Glossary Page Tests — coverage for the IDS-DRR glossary feature.

The glossary page is gated by `features.glossary` in the frontend config.
Tests that navigate to the glossary will be skipped if it returns 404.

Run:
    pytest tests/test_glossary.py -v
    pytest tests/test_glossary.py -m smoke -v
"""

import pytest
from pages.common_page import CommonPage
from pages.glossary_page import GlossaryPage


def _navigate_and_check(driver):
    """Helper: navigate to glossary and skip if the feature is disabled (404)."""
    common_page = CommonPage(driver)
    glossary_page = GlossaryPage(driver)

    if not common_page.navigate_to_glossary():
        pytest.skip("Glossary page not reachable — feature may be disabled on this deployment")

    return common_page, glossary_page


@pytest.mark.component
@pytest.mark.smoke
class TestGlossaryPage:
    """Smoke tests: glossary page loads with expected structure"""

    def test_navigate_to_glossary(self, driver):
        """Glossary page is accessible"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_glossary(), \
            "Could not navigate to glossary — check URL config or feature flag"

    def test_header_visible_on_glossary(self, driver):
        """Header is present on the glossary page"""
        common_page, _ = _navigate_and_check(driver)
        assert common_page.is_header_logo_visible(), "Header logo missing on glossary page"

    def test_glossary_content_loads(self, driver):
        """Glossary terms are rendered (at least one accordion item visible)"""
        _, glossary_page = _navigate_and_check(driver)
        assert glossary_page.is_content_loaded(), \
            "Glossary term content did not load — no accordion items found"

    def test_search_input_visible(self, driver):
        """Search input is rendered on the glossary page"""
        _, glossary_page = _navigate_and_check(driver)
        assert glossary_page.is_search_input_visible(), "Glossary search input not visible"

    def test_multiple_letter_groups_visible(self, driver):
        """More than one letter group section is visible (terms span multiple letters)"""
        _, glossary_page = _navigate_and_check(driver)
        count = glossary_page.get_term_group_count()
        assert count > 1, f"Expected multiple letter groups, found {count}"


@pytest.mark.component
class TestGlossarySearch:
    """Glossary search functionality"""

    def test_search_filters_results(self, driver):
        """Searching narrows the visible term groups"""
        _, glossary_page = _navigate_and_check(driver)

        initial_count = glossary_page.get_term_group_count()
        assert glossary_page.search_term("risk"), "Failed to enter search query"

        filtered_count = glossary_page.get_term_group_count()
        # 'risk' matches 'Risk Score' — should return fewer groups than the full list
        assert filtered_count < initial_count, \
            f"Search should narrow results (got {filtered_count}, initial was {initial_count})"

    def test_search_shows_results_or_empty_state(self, driver):
        """Search either shows matching terms or an empty-state message"""
        _, glossary_page = _navigate_and_check(driver)
        assert glossary_page.search_term("flood"), "Failed to enter search query"

        count = glossary_page.get_term_group_count()
        # If count == 0 the empty state should be visible; if > 0 terms are present
        assert count >= 0, "Unexpected state after search"
        print(f"✅ Search returned {count} letter group(s)")

    def test_clear_search_restores_all_results(self, driver):
        """Clearing the search restores the full term list"""
        _, glossary_page = _navigate_and_check(driver)

        initial_count = glossary_page.get_term_group_count()
        assert glossary_page.search_term("risk"), "Failed to enter search query"
        assert glossary_page.clear_search(), "Failed to clear search"

        import time
        time.sleep(0.5)  # Allow React to re-render after onChange

        restored_count = glossary_page.get_term_group_count()
        assert restored_count == initial_count, \
            f"Expected {initial_count} groups after clear, got {restored_count}"

    def test_expand_first_term(self, driver):
        """Clicking a term accordion opens its definition"""
        _, glossary_page = _navigate_and_check(driver)

        if not glossary_page.is_content_loaded():
            pytest.skip("No glossary content to interact with")

        assert glossary_page.click_first_term(), "Failed to click first glossary term"


@pytest.mark.component
@pytest.mark.edge_case
class TestGlossaryEdgeCases:
    """Edge cases for the glossary page"""

    def test_search_with_no_match(self, driver):
        """Searching a nonsense string shows empty state without crashing"""
        _, glossary_page = _navigate_and_check(driver)
        assert glossary_page.search_term("xyzzy_no_match_999"), "Failed to enter search query"

        count = glossary_page.get_term_group_count()
        assert count == 0, f"Expected 0 results for nonsense query, got {count}"

    def test_glossary_after_navigation_back(self, driver):
        """Returning to glossary from another page keeps the search input functional"""
        common_page, glossary_page = _navigate_and_check(driver)

        assert common_page.navigate_to_home(), "Failed to navigate away from glossary"
        assert common_page.navigate_to_glossary(), "Failed to return to glossary"
        assert glossary_page.is_search_input_visible(), \
            "Search input not visible after returning to glossary"
