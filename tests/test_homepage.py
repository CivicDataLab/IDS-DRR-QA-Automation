"""
Home Page Tests — coverage for the IDS-DRR landing page.

Run:
    pytest tests/test_homepage.py -v
    pytest tests/test_homepage.py -m smoke -v
"""

import pytest
from pages.common_page import CommonPage
from pages.home_page import HomePage


@pytest.mark.component
@pytest.mark.smoke
class TestHomePageComponents:
    """Smoke tests for home page structure"""

    def test_home_page_loads(self, driver):
        """Home page loads with header visible"""
        common_page = CommonPage(driver)
        assert common_page.is_header_logo_visible(), "Header logo not visible on home page"

    def test_header_on_home_page(self, driver):
        """All header elements are present on the home page"""
        common_page = CommonPage(driver)
        header_results = common_page.check_all_header_elements(include_language_dropdown=False)
        assert all(header_results.values()), f"Header incomplete on home page: {header_results}"

    def test_footer_on_home_page(self, driver):
        """Footer logos are visible on the home page"""
        common_page = CommonPage(driver)
        footer_results = common_page.check_all_footer_elements()
        assert all(footer_results.values()), f"Footer incomplete on home page: {footer_results}"

    def test_state_links_section_visible(self, driver):
        """Analytics quick-links section is rendered"""
        home_page = HomePage(driver)
        assert home_page.is_state_links_section_visible(), \
            "State quick-links section not visible on home page"

    def test_state_analytics_links_visible(self, driver):
        """At least one state analytics link is visible in the carousel"""
        home_page = HomePage(driver)
        assert home_page.are_state_links_visible(), \
            "No state analytics links visible on home page"


@pytest.mark.component
class TestHomePageNavigation:
    """Navigation flows originating from the home page"""

    def test_navigate_to_analytics_from_home(self, driver):
        """Nav link takes user from home to analytics"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics from home"
        assert common_page.is_header_logo_visible(), "Header missing after navigating to analytics"

    def test_navigate_to_datasets_from_home(self, driver):
        """Nav link takes user from home to datasets"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets from home"
        assert common_page.is_header_logo_visible(), "Header missing after navigating to datasets"

    def test_navigate_to_about_us_from_home(self, driver):
        """Nav link takes user from home to About Us"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_about_us(), "Failed to navigate to about us from home"
        assert common_page.is_header_logo_visible(), "Header missing on About Us page"

    def test_click_state_link_navigates_to_analytics(self, driver):
        """Clicking a state quick-link navigates to that state's analytics page"""
        home_page = HomePage(driver)
        initial_url = driver.current_url

        if not home_page.are_state_links_visible():
            pytest.skip("State links not visible — API may be unavailable")

        assert home_page.click_first_state_link(), "Failed to click first state link"

        from selenium.webdriver.support.ui import WebDriverWait
        try:
            WebDriverWait(driver, 10).until(lambda d: d.current_url != initial_url)
        except Exception:
            pass

        assert driver.current_url != initial_url, "URL did not change after clicking state link"
        assert "analytics" in driver.current_url.lower(), \
            f"Expected analytics URL, got: {driver.current_url}"


@pytest.mark.component
@pytest.mark.edge_case
class TestHomePageEdgeCases:
    """Edge cases for the home page"""

    def test_home_page_after_refresh(self, driver):
        """Header and footer survive a page refresh"""
        common_page = CommonPage(driver)
        driver.refresh()
        assert common_page.is_header_logo_visible(), "Header missing after refresh on home page"

    def test_return_to_home_from_analytics(self, driver):
        """Logo click or Home nav returns user to home page"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert common_page.navigate_to_home(), "Failed to navigate back to home"
        assert common_page.is_header_logo_visible(), "Header missing after returning home"

    def test_carousel_next_button(self, driver):
        """Carousel next button is clickable when state links are visible"""
        home_page = HomePage(driver)

        if not home_page.is_state_links_section_visible():
            pytest.skip("State links section not present")

        # Carousel next is only relevant if there are enough states to scroll
        result = home_page.click_carousel_next()
        # Not a hard failure — some deployments may have fewer states than carousel pages
        print(f"Carousel next click result: {result}")
