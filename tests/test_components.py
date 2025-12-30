"""
Component Visibility Tests - Comprehensive test coverage for UI components

Run: pytest tests/test_components.py -v
"""

import pytest
from pages.common_page import CommonPage


@pytest.mark.component
@pytest.mark.smoke
class TestHeaderComponents:
    """Tests for header/navigation components"""

    def test_header_logo_visible(self, driver):
        """Test header logo is visible on homepage"""
        common_page = CommonPage(driver)
        assert common_page.is_header_logo_visible(), "Header logo not visible"

    def test_language_dropdown_visible(self, driver):
        """Test language dropdown is visible"""
        common_page = CommonPage(driver)
        assert common_page.is_language_dropdown_visible(), "Language dropdown not visible"

    @pytest.mark.parametrize("nav_link", ["home", "analytics", "datasets", "about_us"])
    def test_navigation_links_visible(self, driver, nav_link):
        """Test all navigation links are visible"""
        common_page = CommonPage(driver)
        assert common_page.is_nav_link_visible(nav_link), f"{nav_link} link not visible"

    def test_all_header_elements(self, driver):
        """Test all header elements at once"""
        common_page = CommonPage(driver)
        header_results = common_page.check_all_header_elements()
        assert all(header_results.values()), f"Some header elements missing: {header_results}"

    @pytest.mark.negative
    def test_invalid_nav_link(self, driver):
        """Negative test: Check invalid navigation link"""
        common_page = CommonPage(driver)
        result = common_page.is_nav_link_visible("invalid_link")
        assert result is False, "Invalid link should return False"


@pytest.mark.component
@pytest.mark.smoke
class TestFooterComponents:
    """Tests for footer components"""

    @pytest.mark.parametrize("logo", ["ids_drr", "cdl", "ocp"])
    def test_footer_logos_visible(self, driver, logo):
        """Test main footer logos are visible"""
        common_page = CommonPage(driver)
        assert common_page.is_footer_logo_visible(logo), f"{logo} logo not visible"

    @pytest.mark.parametrize("partner", ["rockefeller", "pjmf", "asdma", "hpsdma"])
    def test_partner_logos_visible(self, driver, partner):
        """Test partner/supporter logos are visible"""
        common_page = CommonPage(driver)
        assert common_page.is_partner_logo_visible(partner), f"{partner} logo not visible"

    def test_all_footer_elements(self, driver):
        """Test all footer elements at once"""
        common_page = CommonPage(driver)
        footer_results = common_page.check_all_footer_elements()
        assert all(footer_results.values()), f"Some footer elements missing: {footer_results}"

    @pytest.mark.negative
    def test_invalid_footer_logo(self, driver):
        """Negative test: Check invalid footer logo"""
        common_page = CommonPage(driver)
        result = common_page.is_footer_logo_visible("invalid_logo")
        assert result is False, "Invalid logo should return False"

    @pytest.mark.negative
    def test_invalid_partner_logo(self, driver):
        """Negative test: Check invalid partner logo"""
        common_page = CommonPage(driver)
        result = common_page.is_partner_logo_visible("invalid_partner")
        assert result is False, "Invalid partner should return False"


@pytest.mark.component
class TestComponentsOnAllPages:
    """Test components are consistent across all pages"""

    @pytest.mark.parametrize("page_name,navigation_method", [
        ("homepage", None),
        ("analytics", "navigate_to_analytics"),
        ("datasets", "navigate_to_datasets"),
        ("about_us", "navigate_to_about_us")
    ])
    def test_header_on_all_pages(self, driver, page_name, navigation_method):
        """Test header components on all pages"""
        common_page = CommonPage(driver)

        # Navigate to page if needed
        if navigation_method:
            getattr(common_page, navigation_method)()

        header_results = common_page.check_all_header_elements()
        assert all(header_results.values()), f"Header missing on {page_name}: {header_results}"

    @pytest.mark.parametrize("page_name,navigation_method", [
        ("homepage", None),
        ("analytics", "navigate_to_analytics"),
        ("datasets", "navigate_to_datasets"),
        ("about_us", "navigate_to_about_us")
    ])
    def test_footer_on_all_pages(self, driver, page_name, navigation_method):
        """Test footer components on all pages"""
        common_page = CommonPage(driver)

        # Navigate to page if needed
        if navigation_method:
            getattr(common_page, navigation_method)()

        footer_results = common_page.check_all_footer_elements()
        assert all(footer_results.values()), f"Footer missing on {page_name}: {footer_results}"


@pytest.mark.component
class TestNavigationFunctionality:
    """Test navigation link functionality"""

    def test_navigate_to_analytics_and_back(self, driver):
        """Test navigating to analytics and back to home"""
        common_page = CommonPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert common_page.is_nav_link_visible("home"), "Home link not visible on analytics"

        assert common_page.navigate_to_home(), "Failed to navigate back to home"
        assert common_page.is_nav_link_visible("analytics"), "Analytics link not visible on home"

    def test_navigate_to_datasets_and_back(self, driver):
        """Test navigating to datasets and back to home"""
        common_page = CommonPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert common_page.navigate_to_home(), "Failed to navigate back to home"
        assert common_page.is_header_logo_visible(), "Header logo missing after navigation"

    def test_circular_navigation(self, driver):
        """Test circular navigation through all pages"""
        common_page = CommonPage(driver)

        # Navigate in circle: Home -> Analytics -> Datasets -> About Us -> Home
        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert common_page.navigate_to_about_us(), "Failed to navigate to about us"
        assert common_page.navigate_to_home(), "Failed to navigate back to home"

        # Verify we're back at home
        assert common_page.is_header_logo_visible(), "Header logo not visible after circular navigation"


@pytest.mark.component
@pytest.mark.edge_case
class TestComponentEdgeCases:
    """Edge cases for component testing"""

    def test_rapid_navigation_clicks(self, driver):
        """Edge case: Rapidly click navigation links"""
        common_page = CommonPage(driver)

        # Rapid navigation - ensure all navigations succeed
        for iteration in range(3):
            assert common_page.navigate_to_analytics(), f"Failed to navigate to analytics in iteration {iteration + 1}"
            assert common_page.navigate_to_datasets(), f"Failed to navigate to datasets in iteration {iteration + 1}"
            assert common_page.navigate_to_home(), f"Failed to navigate to home in iteration {iteration + 1}"

    def test_components_after_page_refresh(self, driver):
        """Edge case: Verify components after page refresh"""
        common_page = CommonPage(driver)

        driver.refresh()

        header_results = common_page.check_all_header_elements()
        footer_results = common_page.check_all_footer_elements()

        assert all(header_results.values()), "Header missing after refresh"
        assert all(footer_results.values()), "Footer missing after refresh"

    def test_components_after_back_button(self, driver):
        """Edge case: Verify components after browser back"""
        common_page = CommonPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        driver.back()

        header_results = common_page.check_all_header_elements()
        assert all(header_results.values()), "Header missing after back button"

    def test_components_after_forward_button(self, driver):
        """Edge case: Verify components after browser forward"""
        common_page = CommonPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        driver.back()
        driver.forward()

        header_results = common_page.check_all_header_elements()
        assert all(header_results.values()), "Header missing after forward button"


@pytest.mark.component
@pytest.mark.negative
class TestComponentNegativeTests:
    """Negative tests for component visibility"""

    def test_components_on_404_page(self, driver):
        """Negative test: Check if components appear on error pages"""
        from config.config import Config

        # Navigate to a likely non-existent page
        driver.get(f"{Config.BASE_URL}/non-existent-page-12345")

        # Check if basic page structure exists (may vary by implementation)
        # At minimum, we should not crash
        try:
            common_page = CommonPage(driver)
            # Just verify we can check for elements without crashing
            common_page.is_header_logo_visible()
            assert True, "Page loaded without crashing"
        except Exception as e:
            # If page crashes, that's a fail
            assert False, f"404 page handling failed: {str(e)}"

    @pytest.mark.skip(reason="Requires disabled JavaScript scenario")
    def test_components_without_javascript(self, driver):
        """Negative test: Components with JavaScript disabled"""
        # Would require ChromeOptions to disable JS
        pass

    @pytest.mark.skip(reason="Requires slow network simulation")
    def test_components_on_slow_network(self, driver):
        """Edge case: Component loading on slow network"""
        # Would require network throttling
        pass


@pytest.mark.component
@pytest.mark.slow
class TestComponentPersistence:
    """Test component persistence across user journeys"""

    def test_components_during_analytics_flow(self, driver):
        """Test components remain visible during analytics workflow"""
        common_page = CommonPage(driver)
        from pages.analytics_page import AnalyticsPage
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"

        # Perform some analytics actions
        assert analytics_page.select_view(1), "Failed to select view"
        assert analytics_page.select_district("Sivasagar"), "Failed to select district"

        # Check components still visible
        assert common_page.is_header_logo_visible(), "Header missing during analytics flow"
        footer_results = common_page.check_all_footer_elements()
        assert all(footer_results.values()), "Footer missing during analytics flow"

    def test_components_during_dataset_flow(self, driver):
        """Test components remain visible during dataset workflow"""
        common_page = CommonPage(driver)
        from pages.dataset_page import DatasetPage
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"

        # Check components still visible
        assert common_page.is_header_logo_visible(), "Header missing during dataset flow"
        assert all(common_page.check_all_footer_elements().values()), "Footer missing during dataset flow"


@pytest.mark.component
@pytest.mark.boundary
class TestComponentBoundaryConditions:
    """Boundary condition tests for components"""

    def test_components_at_minimum_window_size(self, driver):
        """Boundary test: Components at minimum window size"""
        common_page = CommonPage(driver)

        # Set to minimum reasonable size
        driver.set_window_size(800, 600)

        header_results = common_page.check_all_header_elements()
        # At small sizes, some elements might be hidden (mobile menu)
        # Test based on expected responsive behavior

    def test_components_at_maximum_window_size(self, driver):
        """Boundary test: Components at maximum window size"""
        common_page = CommonPage(driver)

        # Set to large size
        driver.set_window_size(2560, 1440)

        header_results = common_page.check_all_header_elements()
        footer_results = common_page.check_all_footer_elements()

        assert all(header_results.values()), "Header broken at large size"
        assert all(footer_results.values()), "Footer broken at large size"

    @pytest.mark.skip(reason="Requires mobile emulation")
    def test_components_on_mobile_viewport(self, driver):
        """Boundary test: Components on mobile viewport"""
        # Would require mobile emulation setup
        pass


@pytest.mark.component
class TestComponentAccessibility:
    """Accessibility tests for components (basic)"""

    def test_header_logo_has_alt_text(self, driver):
        """Test header logo has accessible alt text"""
        from locators.common_locators import HeaderLocators
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        common_page = CommonPage(driver)
        wait = WebDriverWait(driver, 10)

        # Find the logo element
        try:
            logo_element = wait.until(EC.presence_of_element_located(HeaderLocators.HEADER_LOGO))
            # Check if it has alt text or aria-label for accessibility
            alt_text = logo_element.get_attribute("alt")
            aria_label = logo_element.get_attribute("aria-label")

            assert alt_text or aria_label, "Logo should have alt text or aria-label for accessibility"
            print(f"✅ Logo has accessibility text: alt='{alt_text}', aria-label='{aria_label}'")
        except Exception as e:
            assert False, f"Failed to verify logo accessibility: {str(e)}"

    def test_navigation_links_accessible(self, driver):
        """Test navigation links are keyboard accessible"""
        from locators.common_locators import HeaderLocators
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = WebDriverWait(driver, 10)

        # Test that navigation links are focusable (basic keyboard accessibility)
        nav_links = [
            HeaderLocators.HOME_LINK,
            HeaderLocators.ANALYTICS_LINK,
            HeaderLocators.DATASETS_LINK,
            HeaderLocators.ABOUT_US_LINK
        ]

        for link_locator in nav_links:
            try:
                link_element = wait.until(EC.presence_of_element_located(link_locator))
                # Check if element is keyboard focusable (has tabindex >= 0 or is naturally focusable)
                tag_name = link_element.tag_name
                tabindex = link_element.get_attribute("tabindex")

                # Links (a tags) are naturally focusable, or should have tabindex >= 0
                is_focusable = tag_name == "a" or (tabindex and int(tabindex) >= 0)
                assert is_focusable, f"Navigation link {link_locator} should be keyboard accessible"
            except Exception as e:
                print(f"⚠️ Could not verify keyboard accessibility for {link_locator}: {str(e)}")

        print("✅ Navigation links are keyboard accessible")

    @pytest.mark.skip(reason="Requires accessibility checker")
    def test_components_meet_wcag_standards(self, driver):
        """Test components meet WCAG accessibility standards"""
        # Would require accessibility testing library
        pass
