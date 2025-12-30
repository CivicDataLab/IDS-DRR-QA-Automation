"""
Analytics Page Tests - Comprehensive test coverage including edge cases and negative tests

Run: pytest tests/test_analytics.py -v
"""

import pytest
from pages.common_page import CommonPage
from pages.analytics_page import AnalyticsPage
from config.test_data import AnalyticsTestData


@pytest.mark.analytics
@pytest.mark.smoke
class TestAnalyticsNavigation:
    """Analytics page navigation and accessibility tests"""

    def test_navigate_to_analytics_from_homepage(self, driver):
        """Verify analytics page is accessible from homepage"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_analytics(), "Failed to navigate to Analytics"
        print("✅ Analytics navigation successful")

    def test_analytics_page_header_visible(self, driver):
        """Verify header is visible on analytics page"""
        common_page = CommonPage(driver)
        common_page.navigate_to_analytics()
        assert common_page.is_header_logo_visible(), "Header logo not visible on analytics page"

    def test_analytics_page_footer_visible(self, driver):
        """Verify footer is visible on analytics page"""
        common_page = CommonPage(driver)
        common_page.navigate_to_analytics()
        footer_results = common_page.check_all_footer_elements()
        assert all(footer_results.values()), "Some footer elements not visible"


@pytest.mark.analytics
class TestAnalyticsViewToggle:
    """Tests for Map, Chart, and Table view toggling"""

    @pytest.mark.parametrize("view_index,view_name", [
        (1, "Map"),
        (2, "Chart"),
        (3, "Table")
    ])
    def test_select_view(self, driver, view_index, view_name):
        """Test individual view selection"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        common_page.navigate_to_analytics()
        assert analytics_page.select_view(view_index), f"Failed to select {view_name} view"
        print(f"✅ {view_name} view selected successfully")

    def test_toggle_between_all_views(self, driver):
        """Test toggling between all three views"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        common_page.navigate_to_analytics()

        # Toggle through all views
        for view_index in [1, 2, 3, 1]:  # Test cycling
            assert analytics_page.select_view(view_index), f"Failed to select view {view_index}"

    @pytest.mark.negative
    def test_invalid_view_index(self, driver):
        """Negative test: Invalid view index should fail gracefully"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        common_page.navigate_to_analytics()
        # This should return False or handle error gracefully
        result = analytics_page.select_view(99)
        assert result is False, "Invalid view index should return False"


@pytest.mark.analytics
class TestAnalyticsFilters:
    """Tests for district, revenue circle, and calendar filters"""

    def test_select_district_dropdown(self, driver):
        """Test district selection"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_view(1), "Failed to select Map view"

        assert analytics_page.select_district("Sivasagar"), "Failed to select district"

    def test_select_revenue_circle_dropdown(self, driver):
        """Test revenue circle selection"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_view(1), "Failed to select Map view"
        assert analytics_page.select_district("Sivasagar"), "Failed to select district"

        assert analytics_page.select_revenue_circle("Sibsagar"), "Failed to select revenue circle"

    @pytest.mark.parametrize("month", ["1", "6", "7", "12"])
    def test_select_calendar_months(self, driver, month):
        """Test calendar month selection - boundary values"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        common_page.navigate_to_analytics()
        analytics_page.select_view(1)

        assert analytics_page.open_calendar(), "Failed to open calendar"
        assert analytics_page.select_calendar_month(month), f"Failed to select month {month}"

    @pytest.mark.negative
    def test_select_invalid_month(self, driver):
        """Negative test: Invalid month selection"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        common_page.navigate_to_analytics()
        analytics_page.open_calendar()

        # Invalid month (13)
        result = analytics_page.select_calendar_month("13")
        assert result is False, "Invalid month should return False"

    def test_filter_combination_all_fields(self, driver):
        """Test selecting all filters in combination"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        common_page.navigate_to_analytics()
        analytics_page.select_view(1)

        # Select all filters
        assert analytics_page.select_district("Sivasagar"), "District selection failed"
        assert analytics_page.select_revenue_circle("Sibsagar"), "Revenue circle failed"
        assert analytics_page.open_calendar(), "Calendar open failed"
        assert analytics_page.select_calendar_month("7"), "Month selection failed"

        analytics_page.take_analytics_screenshot("filter_", "all_selected")


@pytest.mark.analytics
class TestHazardOptions:
    """Tests for Hazard section options"""

    def test_expand_hazard_section(self, driver):
        """Test expanding hazard options"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_hazard_options(), "Failed to expand hazard options"

    def test_collapse_hazard_section(self, driver):
        """Test collapsing hazard options"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_hazard_options(), "Failed to expand hazard options"
        assert analytics_page.collapse_hazard_options(), "Failed to collapse hazard options"

    @pytest.mark.parametrize("option", ["monthly_rainfall", "inundation", "elevation"])
    def test_select_hazard_option(self, driver, option):
        """Test individual hazard option selection and validate map loads for monthly_rainfall"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate to analytics page
        navigation_result = common_page.navigate_to_analytics()
        assert navigation_result, "❌ Failed to navigate to Analytics page"
        print(f"✅ Navigated to Analytics page: {driver.current_url}")

        # Select Map view and district for map validation (only for monthly_rainfall to save time)
        if option == "monthly_rainfall":
            assert analytics_page.select_view(1), "❌ Failed to select Map view"
            assert analytics_page.select_district("Sivasagar"), "❌ Failed to select district"

        assert analytics_page.expand_hazard_options(), "❌ Failed to expand hazard options"
        assert analytics_page.select_hazard_option(option), f"Failed to select {option}"

        # Validate map loads specifically for monthly_rainfall indicator
        if option == "monthly_rainfall":
            # Check if map container (canvas or svg) is visible with reduced timeout
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            # Use explicit wait with shorter timeout (3 seconds is sufficient)
            wait = WebDriverWait(driver, 3)
            map_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg")))

            assert map_element is not None, "❌ Map did not load after selecting Total Monthly Rainfall"
            print(f"✅ Map loaded successfully for {option}")

            # Take screenshot for visual validation of district highlighting
            analytics_page.take_analytics_screenshot(
                f"hazard_{option}_",
                "map_with_district_highlighted"
            )

    @pytest.mark.negative
    def test_invalid_hazard_option(self, driver):
        """Negative test: Invalid hazard option"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_hazard_options(), "Failed to expand hazard options"

        result = analytics_page.select_hazard_option("invalid_option")
        assert result is False, "Invalid option should return False"


@pytest.mark.analytics
class TestExposureOptions:
    """Tests for Exposure section options"""

    @pytest.mark.parametrize("option", ["households", "population", "elderly", "children"])
    def test_select_exposure_option(self, driver, option):
        """Test individual exposure option selection"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_exposure_options(), "Failed to expand exposure options"
        assert analytics_page.select_exposure_option(option), f"Failed to select {option}"

    def test_all_exposure_options_sequential(self, driver):
        """Test selecting all exposure options in sequence"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_exposure_options(), "Failed to expand exposure options"

        options = ["households", "population", "elderly", "children"]
        for option in options:
            assert analytics_page.select_exposure_option(option), f"Failed: {option}"


@pytest.mark.analytics
class TestVulnerabilityOptions:
    """Tests for Vulnerability section options"""

    @pytest.mark.parametrize("option", [
        "health_centres", "electricity", "water", "sanitation", "schools",
        "rail", "road", "sown_area", "sex_ratio"
    ])
    def test_vulnerability_infrastructure_options(self, driver, option):
        """Test infrastructure vulnerability options"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_vulnerability_options(), "Failed to expand vulnerability options"
        assert analytics_page.select_vulnerability_option(option), f"Failed: {option}"

    @pytest.mark.parametrize("option", [
        "population_affected", "lives_lost", "crop_affected",
        "embankments_affected", "roads_damaged", "bridges_damaged", "embankments_breached"
    ])
    def test_vulnerability_impact_options(self, driver, option):
        """Test impact vulnerability options"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_vulnerability_options(), "Failed to expand vulnerability options"
        assert analytics_page.select_vulnerability_option(option), f"Failed: {option}"


@pytest.mark.analytics
class TestGovernmentResponse:
    """Tests for Government Response section"""

    @pytest.mark.parametrize("option", ["flood_tenders", "sdrf", "repairs", "immediate", "others", "funds"])
    def test_select_govt_response_option(self, driver, option):
        """Test government response options"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_govt_response_options(), "Failed to expand govt response options"
        assert analytics_page.select_govt_response_option(option), f"Failed: {option}"


@pytest.mark.analytics
@pytest.mark.flow
@pytest.mark.slow
class TestAnalyticsCompleteFlow:
    """Complete end-to-end analytics flow test"""

    def test_complete_analytics_workflow(self, driver):
        """Full analytics workflow with all views and options"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"

        for view_data in AnalyticsTestData.ALL_VIEWS:
            print(f"\n=== Testing {view_data['view_type'].upper()} View ===")

            # Select view and filters
            assert analytics_page.select_view(view_data['view_index'])
            analytics_page.take_analytics_screenshot(view_data['screenshot_prefix'], "initial")

            assert analytics_page.select_district(view_data['district'])
            assert analytics_page.select_revenue_circle(view_data['revenue_circle'])
            assert analytics_page.open_calendar()
            assert analytics_page.select_calendar_month(view_data['calendar_month'])

            # Test Hazard options
            assert analytics_page.expand_hazard_options(view_data['screenshot_prefix'])
            for option in ['monthly_rainfall', 'inundation', 'elevation']:
                assert analytics_page.select_hazard_option(option, view_data['screenshot_prefix'])
            assert analytics_page.collapse_hazard_options()

            # Test Exposure options
            assert analytics_page.expand_exposure_options(view_data['screenshot_prefix'])
            for option in ['households', 'population', 'elderly', 'children']:
                assert analytics_page.select_exposure_option(option, view_data['screenshot_prefix'])
            assert analytics_page.collapse_exposure_options()

            # Test Vulnerability options
            assert analytics_page.expand_vulnerability_options(view_data['screenshot_prefix'])
            vuln_options = [
                'health_centres', 'electricity', 'water', 'sanitation', 'schools',
                'rail', 'road', 'sown_area', 'sex_ratio', 'population_affected',
                'lives_lost', 'crop_affected', 'embankments_affected',
                'roads_damaged', 'bridges_damaged', 'embankments_breached'
            ]
            for option in vuln_options:
                assert analytics_page.select_vulnerability_option(option, view_data['screenshot_prefix'])
            assert analytics_page.collapse_vulnerability_options()

            # Test Government Response options
            assert analytics_page.expand_govt_response_options(view_data['screenshot_prefix'])
            for option in ['flood_tenders', 'sdrf', 'repairs', 'immediate', 'others', 'funds']:
                assert analytics_page.select_govt_response_option(option, view_data['screenshot_prefix'])
            assert analytics_page.collapse_govt_response_options()

            print(f"✅ {view_data['view_type'].upper()} view completed")


@pytest.mark.analytics
@pytest.mark.map
class TestHazardMapValidation:
    """Map-based testing for all Hazard indicators"""

    @pytest.mark.parametrize("option", ["monthly_rainfall", "inundation", "elevation"])
    def test_hazard_indicator_map_loads(self, driver, option):
        """Validate map loads for all hazard indicators with district selection"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate and setup
        assert common_page.navigate_to_analytics(), "❌ Failed to navigate to Analytics page"
        assert analytics_page.select_view(1), "❌ Failed to select Map view"
        assert analytics_page.select_district("Sivasagar"), "❌ Failed to select district"

        # Expand hazard and select option
        assert analytics_page.expand_hazard_options(), "❌ Failed to expand hazard options"
        assert analytics_page.select_hazard_option(option), f"❌ Failed to select {option}"

        # Validate map loads
        wait = WebDriverWait(driver, 5)
        map_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg")))

        assert map_element is not None, f"❌ Map did not load for {option}"
        print(f"✅ Map loaded successfully for hazard indicator: {option}")

        # Take screenshot for visual validation
        analytics_page.take_analytics_screenshot(f"hazard_map_{option}_", "validated")


@pytest.mark.analytics
@pytest.mark.map
class TestExposureMapValidation:
    """Map-based testing for all Exposure indicators"""

    @pytest.mark.parametrize("option", ["households", "population", "elderly", "children"])
    def test_exposure_indicator_map_loads(self, driver, option):
        """Validate map loads for all exposure indicators with district selection"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate and setup
        assert common_page.navigate_to_analytics(), "❌ Failed to navigate to Analytics page"
        assert analytics_page.select_view(1), "❌ Failed to select Map view"
        assert analytics_page.select_district("Sivasagar"), "❌ Failed to select district"

        # Expand exposure and select option
        assert analytics_page.expand_exposure_options(), "❌ Failed to expand exposure options"
        assert analytics_page.select_exposure_option(option), f"❌ Failed to select {option}"

        # Validate map loads
        wait = WebDriverWait(driver, 5)
        map_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg")))

        assert map_element is not None, f"❌ Map did not load for {option}"
        print(f"✅ Map loaded successfully for exposure indicator: {option}")

        # Take screenshot for visual validation
        analytics_page.take_analytics_screenshot(f"exposure_map_{option}_", "validated")


@pytest.mark.analytics
@pytest.mark.map
class TestVulnerabilityMapValidation:
    """Map-based testing for all Vulnerability indicators"""

    @pytest.mark.parametrize("option", [
        "health_centres", "electricity", "water", "sanitation", "schools",
        "rail", "road", "sown_area", "sex_ratio"
    ])
    def test_vulnerability_infrastructure_map_loads(self, driver, option):
        """Validate map loads for vulnerability infrastructure indicators"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate and setup
        assert common_page.navigate_to_analytics(), "❌ Failed to navigate to Analytics page"
        assert analytics_page.select_view(1), "❌ Failed to select Map view"
        assert analytics_page.select_district("Sivasagar"), "❌ Failed to select district"

        # Expand vulnerability and select option
        assert analytics_page.expand_vulnerability_options(), "❌ Failed to expand vulnerability options"
        assert analytics_page.select_vulnerability_option(option), f"❌ Failed to select {option}"

        # Validate map loads
        wait = WebDriverWait(driver, 5)
        map_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg")))

        assert map_element is not None, f"❌ Map did not load for {option}"
        print(f"✅ Map loaded successfully for vulnerability indicator: {option}")

        # Take screenshot for visual validation
        analytics_page.take_analytics_screenshot(f"vulnerability_map_{option}_", "validated")

    @pytest.mark.parametrize("option", [
        "population_affected", "lives_lost", "crop_affected",
        "embankments_affected", "roads_damaged", "bridges_damaged", "embankments_breached"
    ])
    def test_vulnerability_impact_map_loads(self, driver, option):
        """Validate map loads for vulnerability impact indicators"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate and setup
        assert common_page.navigate_to_analytics(), "❌ Failed to navigate to Analytics page"
        assert analytics_page.select_view(1), "❌ Failed to select Map view"
        assert analytics_page.select_district("Sivasagar"), "❌ Failed to select district"

        # Expand vulnerability and select option
        assert analytics_page.expand_vulnerability_options(), "❌ Failed to expand vulnerability options"
        assert analytics_page.select_vulnerability_option(option), f"❌ Failed to select {option}"

        # Validate map loads
        wait = WebDriverWait(driver, 5)
        map_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg")))

        assert map_element is not None, f"❌ Map did not load for {option}"
        print(f"✅ Map loaded successfully for vulnerability indicator: {option}")

        # Take screenshot for visual validation
        analytics_page.take_analytics_screenshot(f"vulnerability_map_{option}_", "validated")


@pytest.mark.analytics
@pytest.mark.map
class TestGovernmentResponseMapValidation:
    """Map-based testing for all Government Response indicators"""

    @pytest.mark.parametrize("option", ["flood_tenders", "sdrf", "repairs", "immediate", "others", "funds"])
    def test_govt_response_indicator_map_loads(self, driver, option):
        """Validate map loads for all government response indicators with district selection"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate and setup
        assert common_page.navigate_to_analytics(), "❌ Failed to navigate to Analytics page"
        assert analytics_page.select_view(1), "❌ Failed to select Map view"
        assert analytics_page.select_district("Sivasagar"), "❌ Failed to select district"

        # Expand government response and select option
        assert analytics_page.expand_govt_response_options(), "❌ Failed to expand govt response options"
        assert analytics_page.select_govt_response_option(option), f"❌ Failed to select {option}"

        # Validate map loads
        wait = WebDriverWait(driver, 5)
        map_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg")))

        assert map_element is not None, f"❌ Map did not load for {option}"
        print(f"✅ Map loaded successfully for government response indicator: {option}")

        # Take screenshot for visual validation
        analytics_page.take_analytics_screenshot(f"govt_response_map_{option}_", "validated")


@pytest.mark.analytics
@pytest.mark.edge_case
class TestAnalyticsEdgeCases:
    """Edge cases and boundary condition tests"""

    def test_rapid_view_switching(self, driver):
        """Edge case: Rapidly switch between views"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"

        # Rapid switching - ensure all view switches succeed
        for iteration in range(3):
            for view_index in [1, 2, 3]:
                assert analytics_page.select_view(view_index), f"Failed to select view {view_index} in iteration {iteration + 1}"

    def test_expand_collapse_all_sections_rapidly(self, driver):
        """Edge case: Rapidly expand/collapse all sections"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"

        # Rapid expand/collapse - ensure all operations succeed
        for iteration in range(2):
            assert analytics_page.expand_hazard_options(), f"Failed to expand hazard in iteration {iteration + 1}"
            assert analytics_page.collapse_hazard_options(), f"Failed to collapse hazard in iteration {iteration + 1}"
            assert analytics_page.expand_exposure_options(), f"Failed to expand exposure in iteration {iteration + 1}"
            assert analytics_page.collapse_exposure_options(), f"Failed to collapse exposure in iteration {iteration + 1}"
            assert analytics_page.expand_vulnerability_options(), f"Failed to expand vulnerability in iteration {iteration + 1}"
            assert analytics_page.collapse_vulnerability_options(), f"Failed to collapse vulnerability in iteration {iteration + 1}"

    def test_select_filters_without_view_selection(self, driver):
        """Edge case: Try filters without selecting view first"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        # Don't select view, try filters directly
        # Should still work or handle gracefully
        result = analytics_page.select_district("Sivasagar")
        assert result is not None, "Filter selection should handle gracefully even without view selection"

    @pytest.mark.negative
    def test_double_expand_same_section(self, driver):
        """Negative test: Double expand same section"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.expand_hazard_options(), "Failed to expand hazard options first time"
        # Second expand should handle gracefully
        result = analytics_page.expand_hazard_options()
        assert result is not None, "Double expand should handle gracefully without errors"
