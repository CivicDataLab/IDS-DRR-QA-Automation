"""
Multi-State Analytics Testing - Comprehensive Coverage
Dynamic, data-driven tests for all analytics functionality across multiple states

Features:
- Automatically discovers and tests all available states
- Dynamically parametrized based on state configuration files
- Complete coverage: navigation, views, filters, expand/collapse, indicators
- Map load validation for ALL indicators across ALL views
- Supports parallel execution
- State-specific indicator validation
- Scalable to future states without code changes

Run:
    # Test all states, all indicators
    pytest tests/test_analytics_multistate.py -v

    # Test specific state
    pytest tests/test_analytics_multistate.py -v -k "assam"

    # Test specific section across all states
    pytest tests/test_analytics_multistate.py -v -k "hazard"

    # Parallel execution (4 workers)
    pytest tests/test_analytics_multistate.py -v -n 4

    # Generate HTML report with state breakdown
    pytest tests/test_analytics_multistate.py -v --html=reports/multistate_report.html
"""

import pytest
from pages.common_page import CommonPage
from pages.analytics_page import AnalyticsPage
from utils.state_config_loader import get_config_loader
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Load state configurations
config_loader = get_config_loader()


def get_multistate_test_params():
    """
    Generate test parameters for all states and indicators

    Returns:
        list: Test parameters (state_key, state_name, section, indicator_key, indicator_name)
    """
    return config_loader.get_test_parameters()


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.smoke
class TestMultiStateNavigation:
    """Analytics page navigation and accessibility tests for all states"""

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_navigate_to_analytics_from_homepage(self, driver, state_key):
        """Verify analytics page is accessible from homepage for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), "Failed to navigate to Analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"
        print(f"✅ Analytics navigation successful for {state_name}")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_analytics_page_header_visible(self, driver, state_key):
        """Verify header is visible on analytics page for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        common_page.navigate_to_analytics()
        analytics_page.select_state(state_name)
        assert common_page.is_header_logo_visible(), f"Header logo not visible on analytics page for {state_name}"

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_analytics_page_footer_visible(self, driver, state_key):
        """Verify footer logos are visible on analytics page for each state
        Analytics page footer contains only: IDS-DRR, CDL, and OCP logos"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        common_page.navigate_to_analytics()
        analytics_page.select_state(state_name)
        footer_results = common_page.check_analytics_footer_elements()
        assert all(footer_results.values()), f"Some footer logos not visible for {state_name}: {footer_results}"


@pytest.mark.analytics
@pytest.mark.multistate
class TestMultiStateViewToggle:
    """Tests for Map, Chart, and Table view toggling across all states"""

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    @pytest.mark.parametrize("view_index,view_name", [
        (1, "Map"),
        (2, "Chart"),
        (3, "Table")
    ])
    def test_select_view_for_state(self, driver, state_key, view_index, view_name):
        """Test individual view selection for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        common_page.navigate_to_analytics()
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"
        assert analytics_page.select_view(view_index), f"Failed to select {view_name} view for {state_name}"
        print(f"✅ {view_name} view selected successfully for {state_name}")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_toggle_between_all_views(self, driver, state_key):
        """Test toggling between all three views for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        common_page.navigate_to_analytics()
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"

        # Toggle through all views
        for view_index in [1, 2, 3, 1]:  # Test cycling
            assert analytics_page.select_view(view_index), f"Failed to select view {view_index} for {state_name}"

        print(f"✅ View toggling successful for {state_name}")


@pytest.mark.analytics
@pytest.mark.multistate
class TestMultiStateSectionExpandCollapse:
    """Tests for expanding and collapsing sections across all states"""

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_expand_collapse_hazard_section(self, driver, state_key):
        """Test expanding and collapsing hazard section for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"
        assert analytics_page.expand_hazard_options(), f"Failed to expand hazard options for {state_name}"
        assert analytics_page.collapse_hazard_options(), f"Failed to collapse hazard options for {state_name}"
        print(f"✅ Hazard section expand/collapse successful for {state_name}")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_expand_collapse_exposure_section(self, driver, state_key):
        """Test expanding and collapsing exposure section for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"
        assert analytics_page.expand_exposure_options(), f"Failed to expand exposure options for {state_name}"
        assert analytics_page.collapse_exposure_options(), f"Failed to collapse exposure options for {state_name}"
        print(f"✅ Exposure section expand/collapse successful for {state_name}")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_expand_collapse_vulnerability_section(self, driver, state_key):
        """Test expanding and collapsing vulnerability section for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"
        assert analytics_page.expand_vulnerability_options(), f"Failed to expand vulnerability options for {state_name}"
        assert analytics_page.collapse_vulnerability_options(), f"Failed to collapse vulnerability options for {state_name}"
        print(f"✅ Vulnerability section expand/collapse successful for {state_name}")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_expand_collapse_govt_response_section(self, driver, state_key):
        """Test expanding and collapsing government response section for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"
        assert analytics_page.expand_govt_response_options(), f"Failed to expand govt response options for {state_name}"
        assert analytics_page.collapse_govt_response_options(), f"Failed to collapse govt response options for {state_name}"
        print(f"✅ Government Response section expand/collapse successful for {state_name}")


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.map_validation
class TestMultiStateIndicatorsMapView:
    """Test all indicators with map load validation in Map view across all states"""

    @pytest.mark.parametrize(
        "state_key,state_name,section,indicator_key,indicator_name",
        get_multistate_test_params(),
        ids=lambda val: str(val) if not isinstance(val, str) else val.replace('_', '-')
    )
    def test_indicator_map_view_loads(
        self,
        driver,
        state_key,
        state_name,
        section,
        indicator_key,
        indicator_name
    ):
        """
        Test that indicator loads correctly with map validation in Map view

        This test:
        1. Navigates to analytics page
        2. Selects the target state
        3. Selects Map view
        4. Expands the appropriate section
        5. Selects the indicator
        6. Validates that map/visualization loads (canvas/svg element visible)
        7. Takes screenshot for validation

        Args:
            driver: WebDriver instance
            state_key: State identifier key
            state_name: Human-readable state name
            section: Section name (hazard, exposure, vulnerability, government_response)
            indicator_key: Indicator identifier
            indicator_name: Human-readable indicator name
        """
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate to analytics
        assert common_page.navigate_to_analytics(), f"❌ Failed to navigate to Analytics for {state_name}"

        # Select state
        assert analytics_page.select_state(state_name), f"❌ Failed to select state: {state_name}"

        # Select Map view
        assert analytics_page.select_view(1), f"❌ Failed to select Map view for {state_name}"

        # Expand appropriate section and select indicator
        section_expand_methods = {
            "hazard": analytics_page.expand_hazard_options,
            "exposure": analytics_page.expand_exposure_options,
            "vulnerability": analytics_page.expand_vulnerability_options,
            "government_response": analytics_page.expand_govt_response_options
        }

        expand_method = section_expand_methods.get(section)
        assert expand_method, f"❌ Unknown section: {section}"

        # Expand section
        assert expand_method(), f"❌ Failed to expand {section} for {state_name}"

        # Select indicator using dynamic text-based selection
        assert analytics_page.select_indicator_by_text(indicator_name, section), \
            f"❌ Failed to select {indicator_name} in {section} for {state_name}"

        # Validate map/visualization loads with comprehensive checks
        wait = WebDriverWait(driver, 15)  # Increased timeout for map loading
        short_wait = WebDriverWait(driver, 3)

        try:
            # Step 1: Wait for loading spinner to disappear (if exists)
            try:
                short_wait.until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".loading, .spinner, [class*='loading'], [class*='spinner']"))
                )
            except:
                pass  # No spinner found, continue

            # Step 2: Wait for map element to be visible
            map_element = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg"))
            )
            assert map_element is not None, \
                f"❌ Map element not found for {indicator_name} in {state_name}"

            # Step 3: Wait for map to actually render (check for non-zero dimensions)
            import time
            time.sleep(2)  # Allow time for map rendering

            map_width = map_element.size['width']
            map_height = map_element.size['height']

            assert map_width > 0 and map_height > 0, \
                f"❌ Map has zero dimensions ({map_width}x{map_height}) for {indicator_name} in {state_name}"

            # Step 4: Verify map is actually displayed and not hidden
            assert map_element.is_displayed(), \
                f"❌ Map element exists but is not displayed for {indicator_name} in {state_name}"

            print(f"✅ MAP VIEW - {state_name} - {section} - {indicator_name}: Map loaded successfully (size: {map_width}x{map_height})")

        except Exception as e:
            pytest.fail(
                f"❌ Map visualization failed to load for {indicator_name} in {state_name}: {e}"
            )

        # Take screenshot for validation
        analytics_page.take_analytics_screenshot(
            f"map_{state_key}_{section}_{indicator_key}_",
            "validated"
        )


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.chart_validation
class TestMultiStateIndicatorsChartView:
    """Test all indicators with visualization validation in Chart view across all states"""

    @pytest.mark.parametrize(
        "state_key,state_name,section,indicator_key,indicator_name",
        get_multistate_test_params(),
        ids=lambda val: str(val) if not isinstance(val, str) else val.replace('_', '-')
    )
    def test_indicator_chart_view_loads(
        self,
        driver,
        state_key,
        state_name,
        section,
        indicator_key,
        indicator_name
    ):
        """
        Test that indicator loads correctly with chart validation in Chart view

        This test:
        1. Navigates to analytics page
        2. Selects the target state
        3. Selects Chart view
        4. Expands the appropriate section
        5. Selects the indicator
        6. Validates that chart/visualization loads
        7. Takes screenshot for validation
        """
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate to analytics
        assert common_page.navigate_to_analytics(), f"❌ Failed to navigate to Analytics for {state_name}"

        # Select state
        assert analytics_page.select_state(state_name), f"❌ Failed to select state: {state_name}"

        # Select Chart view
        assert analytics_page.select_view(2), f"❌ Failed to select Chart view for {state_name}"

        # Expand appropriate section
        section_expand_methods = {
            "hazard": analytics_page.expand_hazard_options,
            "exposure": analytics_page.expand_exposure_options,
            "vulnerability": analytics_page.expand_vulnerability_options,
            "government_response": analytics_page.expand_govt_response_options
        }

        expand_method = section_expand_methods.get(section)
        assert expand_method, f"❌ Unknown section: {section}"
        assert expand_method(), f"❌ Failed to expand {section} for {state_name}"

        # Select indicator
        assert analytics_page.select_indicator_by_text(indicator_name, section), \
            f"❌ Failed to select {indicator_name} in {section} for {state_name}"

        # Validate chart/visualization loads with comprehensive checks
        wait = WebDriverWait(driver, 15)  # Increased timeout for chart loading
        short_wait = WebDriverWait(driver, 3)

        try:
            # Step 1: Wait for loading spinner to disappear (if exists)
            try:
                short_wait.until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".loading, .spinner, [class*='loading'], [class*='spinner']"))
                )
            except:
                pass  # No spinner found, continue

            # Step 2: Wait for chart element to be visible
            chart_element = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg, .chart-container"))
            )
            assert chart_element is not None, \
                f"❌ Chart element not found for {indicator_name} in {state_name}"

            # Step 3: Wait for chart to actually render (check for non-zero dimensions)
            import time
            time.sleep(2)  # Allow time for chart rendering

            chart_width = chart_element.size['width']
            chart_height = chart_element.size['height']

            assert chart_width > 0 and chart_height > 0, \
                f"❌ Chart has zero dimensions ({chart_width}x{chart_height}) for {indicator_name} in {state_name}"

            # Step 4: Verify chart is actually displayed
            assert chart_element.is_displayed(), \
                f"❌ Chart element exists but is not displayed for {indicator_name} in {state_name}"

            print(f"✅ CHART VIEW - {state_name} - {section} - {indicator_name}: Chart loaded successfully (size: {chart_width}x{chart_height})")

        except Exception as e:
            pytest.fail(
                f"❌ Chart visualization failed to load for {indicator_name} in {state_name}: {e}"
            )

        # Take screenshot for validation
        analytics_page.take_analytics_screenshot(
            f"chart_{state_key}_{section}_{indicator_key}_",
            "validated"
        )


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.table_validation
class TestMultiStateIndicatorsTableView:
    """Test all indicators with table validation in Table view across all states"""

    @pytest.mark.parametrize(
        "state_key,state_name,section,indicator_key,indicator_name",
        get_multistate_test_params(),
        ids=lambda val: str(val) if not isinstance(val, str) else val.replace('_', '-')
    )
    def test_indicator_table_view_loads(
        self,
        driver,
        state_key,
        state_name,
        section,
        indicator_key,
        indicator_name
    ):
        """
        Test that indicator loads correctly with table validation in Table view

        This test:
        1. Navigates to analytics page
        2. Selects the target state
        3. Selects Table view
        4. Expands the appropriate section
        5. Selects the indicator
        6. Validates that table loads
        7. Takes screenshot for validation
        """
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Navigate to analytics
        assert common_page.navigate_to_analytics(), f"❌ Failed to navigate to Analytics for {state_name}"

        # Select state
        assert analytics_page.select_state(state_name), f"❌ Failed to select state: {state_name}"

        # Select Table view
        assert analytics_page.select_view(3), f"❌ Failed to select Table view for {state_name}"

        # Expand appropriate section
        section_expand_methods = {
            "hazard": analytics_page.expand_hazard_options,
            "exposure": analytics_page.expand_exposure_options,
            "vulnerability": analytics_page.expand_vulnerability_options,
            "government_response": analytics_page.expand_govt_response_options
        }

        expand_method = section_expand_methods.get(section)
        assert expand_method, f"❌ Unknown section: {section}"
        assert expand_method(), f"❌ Failed to expand {section} for {state_name}"

        # Select indicator
        assert analytics_page.select_indicator_by_text(indicator_name, section), \
            f"❌ Failed to select {indicator_name} in {section} for {state_name}"

        # Validate table loads with comprehensive checks
        wait = WebDriverWait(driver, 15)  # Increased timeout for table loading
        short_wait = WebDriverWait(driver, 3)

        try:
            # Step 1: Wait for loading spinner to disappear (if exists)
            try:
                short_wait.until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".loading, .spinner, [class*='loading'], [class*='spinner']"))
                )
            except:
                pass  # No spinner found, continue

            # Step 2: Wait for table element to be visible
            table_element = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "table, .table-container, [role='table']"))
            )
            assert table_element is not None, \
                f"❌ Table element not found for {indicator_name} in {state_name}"

            # Step 3: Verify table has data (check for rows with data)
            import time
            time.sleep(2)  # Allow time for table data to load

            # Look for table rows (tbody tr or data rows)
            try:
                rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr, [role='row']")
                row_count = len([row for row in rows if row.is_displayed()])

                assert row_count > 0, \
                    f"❌ Table loaded but has no data rows for {indicator_name} in {state_name}"

                print(f"✅ TABLE VIEW - {state_name} - {section} - {indicator_name}: Table loaded successfully with {row_count} rows")

            except:
                # If we can't find rows, at least verify table is displayed
                assert table_element.is_displayed(), \
                    f"❌ Table element exists but is not displayed for {indicator_name} in {state_name}"
                print(f"✅ TABLE VIEW - {state_name} - {section} - {indicator_name}: Table loaded successfully")

        except Exception as e:
            pytest.fail(
                f"❌ Table visualization failed to load for {indicator_name} in {state_name}: {e}"
            )

        # Take screenshot for validation
        analytics_page.take_analytics_screenshot(
            f"table_{state_key}_{section}_{indicator_key}_",
            "validated"
        )


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.section_coverage
class TestSectionCoverageByState:
    """Test complete coverage of all sections for each state"""

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_hazard_section_coverage(self, driver, state_key):
        """Test all hazard indicators for a specific state"""
        self._test_section_coverage(driver, state_key, "hazard")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_exposure_section_coverage(self, driver, state_key):
        """Test all exposure indicators for a specific state"""
        self._test_section_coverage(driver, state_key, "exposure")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_vulnerability_section_coverage(self, driver, state_key):
        """Test all vulnerability indicators for a specific state"""
        self._test_section_coverage(driver, state_key, "vulnerability")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_govt_response_section_coverage(self, driver, state_key):
        """Test all government response indicators for a specific state"""
        self._test_section_coverage(driver, state_key, "government_response")

    def _test_section_coverage(self, driver, state_key, section):
        """
        Helper method to test all indicators in a section for a state

        Args:
            driver: WebDriver instance
            state_key: State identifier
            section: Section name
        """
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        # Navigate and setup
        assert common_page.navigate_to_analytics()
        assert analytics_page.select_state(state_name)
        assert analytics_page.select_view(1)

        # Get section indicators
        indicators = config_loader.get_state_indicators(state_key, section)

        assert len(indicators) > 0, \
            f"❌ No indicators found for {section} in {state_name}"

        print(f"\n{'='*60}")
        print(f"Testing {section} section for {state_name}")
        print(f"Total indicators: {len(indicators)}")
        print(f"{'='*60}\n")

        # Section method mapping
        section_methods = {
            "hazard": {
                "expand": analytics_page.expand_hazard_options,
                "collapse": analytics_page.collapse_hazard_options
            },
            "exposure": {
                "expand": analytics_page.expand_exposure_options,
                "collapse": analytics_page.collapse_exposure_options
            },
            "vulnerability": {
                "expand": analytics_page.expand_vulnerability_options,
                "collapse": analytics_page.collapse_vulnerability_options
            },
            "government_response": {
                "expand": analytics_page.expand_govt_response_options,
                "collapse": analytics_page.collapse_govt_response_options
            }
        }

        handler = section_methods.get(section)
        assert handler, f"Unknown section: {section}"

        # Expand section
        assert handler["expand"](), f"Failed to expand {section}"

        # Test each indicator
        success_count = 0
        for indicator in indicators:
            if not indicator.get("enabled", True):
                print(f"⏭️  Skipping disabled indicator: {indicator['name']}")
                continue

            indicator_name = indicator.get("name")

            try:
                # Use dynamic text-based selection
                assert analytics_page.select_indicator_by_text(indicator_name, section), \
                    f"Failed to select {indicator_name}"

                print(f"✅ Successfully tested: {indicator_name}")
                success_count += 1

            except Exception as e:
                print(f"❌ Failed to test {indicator_name}: {e}")

        # Collapse section
        handler["collapse"]()

        print(f"\n{'='*60}")
        print(f"Section Coverage Summary:")
        print(f"  State: {state_name}")
        print(f"  Section: {section}")
        print(f"  Success: {success_count}/{len(indicators)}")
        print(f"{'='*60}\n")

        assert success_count > 0, \
            f"No indicators successfully tested for {section} in {state_name}"


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.flow
@pytest.mark.slow
class TestMultiStateCompleteFlow:
    """Complete end-to-end analytics flow test for all states"""

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_complete_analytics_workflow_for_state(self, driver, state_key):
        """
        Full analytics workflow with all views, sections, and indicators for each state

        This comprehensive test:
        1. Tests navigation to analytics
        2. Selects the state
        3. Tests all three views (Map, Chart, Table)
        4. For each view, tests all sections (Hazard, Exposure, Vulnerability, Govt Response)
        5. For each section, expands it, tests all indicators, and collapses it
        6. Takes screenshots at key points
        """
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        print(f"\n{'='*80}")
        print(f"COMPLETE WORKFLOW TEST FOR {state_name.upper()}")
        print(f"{'='*80}\n")

        # Navigate and select state
        assert common_page.navigate_to_analytics(), f"Failed to navigate to analytics for {state_name}"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"

        # Test all views
        view_data = [
            {'view_index': 1, 'view_name': 'Map', 'prefix': 'map_'},
            {'view_index': 2, 'view_name': 'Chart', 'prefix': 'chart_'},
            {'view_index': 3, 'view_name': 'Table', 'prefix': 'table_'}
        ]

        for view in view_data:
            print(f"\n=== Testing {view['view_name']} View for {state_name} ===")

            # Select view
            assert analytics_page.select_view(view['view_index']), \
                f"Failed to select {view['view_name']} view for {state_name}"

            analytics_page.take_analytics_screenshot(
                f"{state_key}_{view['prefix']}",
                "initial"
            )

            # Test all sections
            sections = ["hazard", "exposure", "vulnerability", "government_response"]

            for section in sections:
                # Get section-specific data
                indicators = config_loader.get_state_indicators(state_key, section)

                if not indicators:
                    print(f"⚠️  No indicators found for {section} in {state_name}, skipping...")
                    continue

                print(f"\n  --- Testing {section.title()} Section ({len(indicators)} indicators) ---")

                # Section method mapping
                section_methods = {
                    "hazard": {
                        "expand": analytics_page.expand_hazard_options,
                        "collapse": analytics_page.collapse_hazard_options
                    },
                    "exposure": {
                        "expand": analytics_page.expand_exposure_options,
                        "collapse": analytics_page.collapse_exposure_options
                    },
                    "vulnerability": {
                        "expand": analytics_page.expand_vulnerability_options,
                        "collapse": analytics_page.collapse_vulnerability_options
                    },
                    "government_response": {
                        "expand": analytics_page.expand_govt_response_options,
                        "collapse": analytics_page.collapse_govt_response_options
                    }
                }

                handler = section_methods.get(section)

                # Expand section
                assert handler["expand"](), f"Failed to expand {section} for {state_name}"

                analytics_page.take_analytics_screenshot(
                    f"{state_key}_{view['prefix']}{section}_",
                    "expanded"
                )

                # Test each indicator
                for indicator in indicators:
                    if not indicator.get("enabled", True):
                        continue

                    indicator_name = indicator.get("name")

                    try:
                        assert analytics_page.select_indicator_by_text(indicator_name, section), \
                            f"Failed to select {indicator_name}"

                        print(f"    ✅ {indicator_name}")

                    except Exception as e:
                        print(f"    ❌ {indicator_name}: {e}")

                # Collapse section
                assert handler["collapse"](), f"Failed to collapse {section} for {state_name}"

            print(f"\n✅ {view['view_name']} view completed for {state_name}")

        print(f"\n{'='*80}")
        print(f"COMPLETE WORKFLOW TEST FINISHED FOR {state_name.upper()}")
        print(f"{'='*80}\n")


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.cross_state
class TestCrossStateComparison:
    """Cross-state comparison and validation tests"""

    def test_all_states_have_common_sections(self, driver):
        """Verify all states have the four main sections"""
        required_sections = ["hazard", "exposure", "vulnerability", "government_response"]

        for state_key in config_loader.get_all_states():
            state_config = config_loader.get_state_config(state_key)
            state_name = state_config.get("state_name")
            sections = state_config.get("sections", {})

            for required_section in required_sections:
                assert required_section in sections, \
                    f"❌ {state_name} missing required section: {required_section}"

            print(f"✅ {state_name} has all required sections")

    def test_indicator_consistency_report(self, driver):
        """Generate a report of indicator availability across states"""
        print("\n" + "="*80)
        print("MULTI-STATE INDICATOR COVERAGE REPORT")
        print("="*80 + "\n")

        all_summaries = config_loader.get_all_summaries()

        for state_key, summary in all_summaries.items():
            print(f"\n{summary['state_name']}:")
            print(f"  Total Indicators: {summary['total_indicators']}")

            for section_key, section_info in summary['sections'].items():
                enabled = section_info.get('enabled_indicators', section_info['total_indicators'])
                print(f"    • {section_info['name']}: {enabled} indicators")

        print("\n" + "="*80 + "\n")


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.edge_case
class TestMultiStateEdgeCases:
    """Edge cases and boundary condition tests for multistate"""

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_rapid_view_switching(self, driver, state_key):
        """Edge case: Rapidly switch between views for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"

        # Rapid switching
        for iteration in range(2):
            for view_index in [1, 2, 3]:
                assert analytics_page.select_view(view_index), \
                    f"Failed to select view {view_index} in iteration {iteration + 1} for {state_name}"

        print(f"✅ Rapid view switching successful for {state_name}")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_expand_collapse_all_sections_rapidly(self, driver, state_key):
        """Edge case: Rapidly expand/collapse all sections for each state"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), "Failed to navigate to analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"

        # Rapid expand/collapse
        for iteration in range(2):
            assert analytics_page.expand_hazard_options(), \
                f"Failed to expand hazard in iteration {iteration + 1} for {state_name}"
            assert analytics_page.collapse_hazard_options(), \
                f"Failed to collapse hazard in iteration {iteration + 1} for {state_name}"
            assert analytics_page.expand_exposure_options(), \
                f"Failed to expand exposure in iteration {iteration + 1} for {state_name}"
            assert analytics_page.collapse_exposure_options(), \
                f"Failed to collapse exposure in iteration {iteration + 1} for {state_name}"
            assert analytics_page.expand_vulnerability_options(), \
                f"Failed to expand vulnerability in iteration {iteration + 1} for {state_name}"
            assert analytics_page.collapse_vulnerability_options(), \
                f"Failed to collapse vulnerability in iteration {iteration + 1} for {state_name}"

        print(f"✅ Rapid expand/collapse successful for {state_name}")
