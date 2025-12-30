"""
Multi-State Analytics Testing
Dynamic, data-driven tests for all analytics indicators across multiple states

Features:
- Automatically discovers and tests all available states
- Dynamically parametrized based on state configuration files
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
class TestMultiStateIndicators:
    """Test analytics indicators across all configured states"""

    @pytest.mark.parametrize(
        "state_key,state_name,section,indicator_key,indicator_name",
        get_multistate_test_params(),
        ids=lambda val: str(val) if not isinstance(val, str) else val.replace('_', '-')
    )
    def test_indicator_loads_for_state(
        self,
        driver,
        state_key,
        state_name,
        section,
        indicator_key,
        indicator_name
    ):
        """
        Test that indicator loads correctly for a specific state

        This test:
        1. Navigates to analytics page
        2. Selects the target state
        3. Selects Map view
        4. Expands the appropriate section
        5. Selects the indicator
        6. Validates that map/chart loads

        Args:
            driver: WebDriver instance
            state_key: State identifier key
            state_name: Human-readable state name
            section: Section name (hazard, exposure, etc.)
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

        # Select a district to enable map rendering
        # Note: This assumes Sivasagar exists for Assam, adjust per state if needed
        # For scalability, this could also be configured per state
        if state_key == "assam":
            analytics_page.select_district("Sivasagar")

        # Expand appropriate section and select indicator
        section_methods = {
            "hazard": {
                "expand": analytics_page.expand_hazard_options,
                "select": analytics_page.select_hazard_option
            },
            "exposure": {
                "expand": analytics_page.expand_exposure_options,
                "select": analytics_page.select_exposure_option
            },
            "vulnerability": {
                "expand": analytics_page.expand_vulnerability_options,
                "select": analytics_page.select_vulnerability_option
            },
            "government_response": {
                "expand": analytics_page.expand_govt_response_options,
                "select": analytics_page.select_govt_response_option
            }
        }

        section_handler = section_methods.get(section)
        assert section_handler, f"❌ Unknown section: {section}"

        # Expand section
        assert section_handler["expand"](), f"❌ Failed to expand {section} for {state_name}"

        # Select indicator
        assert section_handler["select"](indicator_key), \
            f"❌ Failed to select {indicator_name} in {section} for {state_name}"

        # Validate map/visualization loads
        wait = WebDriverWait(driver, 5)
        try:
            map_element = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg"))
            )
            assert map_element is not None, \
                f"❌ Map did not load for {indicator_name} in {state_name}"

            print(f"✅ {state_name} - {section} - {indicator_name}: Map loaded successfully")

        except Exception as e:
            pytest.fail(
                f"❌ Visualization failed to load for {indicator_name} in {state_name}: {e}"
            )

        # Take screenshot for validation
        analytics_page.take_analytics_screenshot(
            f"{state_key}_{section}_{indicator_key}_",
            "validated"
        )


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.smoke
class TestMultiStateBasicFunctionality:
    """Basic smoke tests for multi-state functionality"""

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_state_selection(self, driver, state_key):
        """Test that each state can be selected successfully"""
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        assert common_page.navigate_to_analytics(), f"Failed to navigate to Analytics"
        assert analytics_page.select_state(state_name), f"Failed to select state: {state_name}"

        print(f"✅ Successfully selected state: {state_name}")

    @pytest.mark.parametrize("state_key", config_loader.get_all_states())
    def test_state_has_indicators(self, driver, state_key):
        """Verify each state has configured indicators"""
        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        total_indicators = sum(
            len(section.get("indicators", []))
            for section in state_config.get("sections", {}).values()
        )

        assert total_indicators > 0, \
            f"❌ State {state_name} has no configured indicators"

        print(f"✅ {state_name} has {total_indicators} configured indicators")


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.section_coverage
class TestSectionCoverageByState:
    """Test coverage of all sections for each state"""

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
                "collapse": analytics_page.collapse_hazard_options,
                "select": analytics_page.select_hazard_option
            },
            "exposure": {
                "expand": analytics_page.expand_exposure_options,
                "collapse": analytics_page.collapse_exposure_options,
                "select": analytics_page.select_exposure_option
            },
            "vulnerability": {
                "expand": analytics_page.expand_vulnerability_options,
                "collapse": analytics_page.collapse_vulnerability_options,
                "select": analytics_page.select_vulnerability_option
            },
            "government_response": {
                "expand": analytics_page.expand_govt_response_options,
                "collapse": analytics_page.collapse_govt_response_options,
                "select": analytics_page.select_govt_response_option
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

            indicator_key = indicator.get("key")
            indicator_name = indicator.get("name")

            try:
                assert handler["select"](indicator_key), \
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
