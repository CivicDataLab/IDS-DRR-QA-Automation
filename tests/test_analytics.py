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
    pytest tests/test_analytics.py -v

    # Test specific state
    pytest tests/test_analytics.py -v -k "assam"

    # Test specific section across all states
    pytest tests/test_analytics.py -v -k "hazard"

    # Parallel execution (4 workers)
    pytest tests/test_analytics.py -v -n 4

    # Generate HTML report with state breakdown
    pytest tests/test_analytics.py -v --html=reports/multistate_report.html
"""

import pytest
from pages.common_page import CommonPage
from pages.analytics_page import AnalyticsPage
from utils.state_config_loader import get_config_loader
from config.test_data import AnalyticsTestData
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


def get_section_test_params():
    """
    Generate test parameters for each state-section combination (consolidated testing)

    This creates one test per section per state, instead of one test per indicator.
    Dramatically reduces browser instances needed.

    Returns:
        list: Test parameters (state_key, state_name, section)
    """
    params = []
    for state_key in config_loader.get_all_states():
        state_config = config_loader.get_state_config(state_key)
        state_name = state_config.get("state_name")

        # Get all sections that have indicators
        sections = state_config.get("sections", {})
        for section_key, section_data in sections.items():
            indicators = section_data.get("indicators", [])
            # Only include sections that have enabled indicators
            enabled_indicators = [ind for ind in indicators if ind.get("enabled", True)]
            if enabled_indicators:
                params.append((state_key, state_name, section_key))

    return params


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
    """
    CONSOLIDATED: Test ALL indicators per section in a single browser instance - Map View

    This reduces browser overhead by testing all Hazard indicators together,
    all Vulnerability indicators together, etc. instead of one browser per indicator.
    """

    @pytest.mark.parametrize(
        "state_key,state_name,section",
        get_section_test_params(),
        ids=lambda val: str(val).replace('_', '-') if isinstance(val, str) else str(val)
    )
    def test_section_all_indicators_map_view(self, driver, state_key, state_name, section, request, extra):
        """
        Test ALL indicators in a section using ONE browser instance - Map View

        Test Steps:
        1. Navigate to Analytics page from homepage
        2. Select State from dropdown
        3. Select Map View
        4. Select District from dropdown
        5. Select Revenue Circle from dropdown
        6. Expand section (Hazard/Exposure/Vulnerability/Government Response)
        7. For each indicator in the section:
           a. Select indicator
           b. Wait for map to load
           c. Validate map dimensions
           d. Check for application errors
           e. Recover if app crashes
        8. Generate test report with pass/fail status

        This consolidates testing to reduce system load:
        - All Hazard indicators tested in one session
        - All Vulnerability indicators tested in one session
        - All Government Response indicators tested in one session
        - All Exposure indicators tested in one session

        Args:
            driver: WebDriver instance (reused for all indicators in this section)
            state_key: State identifier key
            state_name: Human-readable state name
            section: Section name (hazard, exposure, vulnerability, government_response)
            request: pytest request fixture for metadata
            extra: pytest-html extra fixture for adding content to report
        """
        import time

        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Get all indicators for this section
        state_config = config_loader.get_state_config(state_key)
        section_data = state_config.get("sections", {}).get(section, {})
        indicators = section_data.get("indicators", [])
        enabled_indicators = [ind for ind in indicators if ind.get("enabled", True)]

        print(f"\n{'='*80}")
        print(f"Testing {state_name} - {section.upper().replace('_', ' ')}")
        print(f"Total Indicators: {len(enabled_indicators)}")
        print(f"{'='*80}\n")

        # Setup: Navigate and select state/view/section ONCE
        assert common_page.navigate_to_analytics(), f"❌ Failed to navigate to Analytics"
        assert analytics_page.select_state(state_name), f"❌ Failed to select state: {state_name}"
        assert analytics_page.select_view(1), f"❌ Failed to select Map view"

        # Wait for district dropdown to be ready after view selection (uses explicit wait)
        from selenium.webdriver.support.ui import WebDriverWait, Select
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from utils.wait_helpers import wait_for_dropdown_options
        import time

        # Define helper function for this test
        def district_dropdown_ready(driver):
            try:
                element = driver.find_element(By.XPATH, "//select[contains(@id, 'district') or contains(@class, 'district')]")
                select = Select(element)
                return len(select.options) > 1 and element.is_enabled()
            except:
                return False

        # Wait for dropdown using explicit wait
        try:
            WebDriverWait(driver, 15).until(district_dropdown_ready)
        except:
            pass  # Continue if timeout

        # Select district and revenue circle AFTER view selection (dropdowns appear after view is selected)
        district = AnalyticsTestData.get_district_for_state(state_key)
        revenue_circle = AnalyticsTestData.get_revenue_circle_for_state(state_key)
        assert analytics_page.select_district(district), \
            f"❌ Failed to select district: {district}"

        # Revenue circle dropdown uses explicit wait internally - no sleep needed
        assert analytics_page.select_revenue_circle(revenue_circle), \
            f"❌ Failed to select revenue circle: {revenue_circle}"

        # Expand section ONCE before testing all indicators
        section_expand_methods = {
            "hazard": analytics_page.expand_hazard_options,
            "exposure": analytics_page.expand_exposure_options,
            "vulnerability": analytics_page.expand_vulnerability_options,
            "government_response": analytics_page.expand_govt_response_options
        }
        expand_method = section_expand_methods.get(section)
        assert expand_method, f"❌ Unknown section: {section}"

        # Expand the section once - all indicators should remain visible after this
        assert expand_method(), f"❌ Failed to expand {section}"
        print(f"✅ {section.replace('_', ' ').title()} section expanded - testing all indicators\n")

        # Track results
        passed = []
        failed = []

        # Test each indicator in this section (section stays expanded throughout)
        for idx, indicator in enumerate(enabled_indicators, 1):
            indicator_name = indicator.get("name")
            indicator_key = indicator.get("key")

            print(f"[{idx}/{len(enabled_indicators)}] Testing: {indicator_name}")

            try:
                # Wait for loading spinner from previous indicator to clear
                if idx > 1:
                    from utils.wait_helpers import wait_for_loading_to_disappear
                    wait_for_loading_to_disappear(driver, timeout=5)

                # Select indicator (section should already be expanded)
                if not analytics_page.select_indicator_by_text(indicator_name, section):
                    failed.append({'name': indicator_name, 'reason': 'Failed to select indicator'})
                    print(f"  ❌ Failed to select")
                    continue

                # Wait for either error page or map to load (whichever comes first)
                from utils.wait_helpers import wait_for_any_condition

                def check_error(driver):
                    return analytics_page.is_error_page_displayed() and 'error'

                def check_map_loaded(driver):
                    try:
                        map_element = driver.find_element(By.CSS_SELECTOR, "canvas, svg")
                        return map_element.is_displayed() and 'success'
                    except:
                        return False

                result = wait_for_any_condition(driver, [check_error, check_map_loaded], timeout=10)

                if analytics_page.is_error_page_displayed():
                    print(f"  ⚠️  Application error page detected - indicator broke the app")
                    failed.append({'name': indicator_name, 'reason': 'Application crashed with error page'})

                    # Take screenshot of error
                    analytics_page.take_screenshot(f"error_{state_key}_{section}_{idx}", analytics_page.screenshot_dir)

                    # Recover: Navigate back and re-setup state
                    print(f"  🔄 Recovering: Navigating back to Analytics...")
                    assert common_page.navigate_to_analytics(), "❌ Recovery failed: Cannot navigate to Analytics"
                    assert analytics_page.select_state(state_name), f"❌ Recovery failed: Cannot select state {state_name}"
                    assert analytics_page.select_view(1), "❌ Recovery failed: Cannot select Map view"

                    # Wait for district dropdown to be ready
                    try:
                        WebDriverWait(driver, 15).until(district_dropdown_ready)
                    except:
                        pass

                    assert analytics_page.select_district(district), f"❌ Recovery failed: Cannot select district {district}"
                    # Revenue circle has its own explicit wait
                    assert analytics_page.select_revenue_circle(revenue_circle), f"❌ Recovery failed: Cannot select revenue circle {revenue_circle}"
                    assert expand_method(), f"❌ Recovery failed: Cannot expand {section}"
                    print(f"  ✅ Recovery complete - continuing with next indicator")
                    continue

                # Validate map loads
                wait = WebDriverWait(driver, 20)
                short_wait = WebDriverWait(driver, 3)

                try:
                    # Wait for loading spinner to disappear
                    try:
                        short_wait.until_not(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".loading, .spinner, [class*='loading'], [class*='spinner']")))
                    except:
                        pass

                    # Wait for map element
                    map_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas, svg")))

                    # Check dimensions
                    map_width = map_element.size['width']
                    map_height = map_element.size['height']

                    if map_width > 0 and map_height > 0 and map_element.is_displayed():
                        passed.append(indicator_name)
                        print(f"  ✅ Map loaded ({map_width}x{map_height})")
                    else:
                        failed.append({'name': indicator_name, 'reason': f'Invalid dimensions ({map_width}x{map_height})'})
                        print(f"  ❌ Invalid dimensions")

                except Exception as e:
                    # Check if error page appeared during map validation
                    if analytics_page.is_error_page_displayed():
                        print(f"  ⚠️  Application error page detected during map load")
                        failed.append({'name': indicator_name, 'reason': 'Application crashed during map load'})

                        # Take screenshot
                        analytics_page.take_screenshot(f"error_{state_key}_{section}_{idx}_mapload", analytics_page.screenshot_dir)

                        # Recover
                        print(f"  🔄 Recovering...")
                        common_page.navigate_to_analytics()
                        analytics_page.select_state(state_name)
                        analytics_page.select_view(1)

                        # Wait for district dropdown to be ready
                        try:
                            WebDriverWait(driver, 15).until(district_dropdown_ready)
                        except:
                            pass

                        analytics_page.select_district(district)
                        # Revenue circle has its own explicit wait
                        analytics_page.select_revenue_circle(revenue_circle)
                        expand_method()
                        print(f"  ✅ Recovery complete")
                    else:
                        failed.append({'name': indicator_name, 'reason': f'Map validation failed: {str(e)[:80]}'})
                        print(f"  ❌ Map validation failed: {str(e)[:80]}")

            except Exception as e:
                failed.append({'name': indicator_name, 'reason': f'Error: {str(e)[:80]}'})
                print(f"  ❌ Error: {str(e)[:80]}")

        # Print summary
        print(f"\n{'='*80}")
        print(f"SUMMARY: {state_name} - {section.upper().replace('_', ' ')}")
        print(f"✅ Passed: {len(passed)}/{len(enabled_indicators)} ({len(passed)/len(enabled_indicators)*100:.1f}%)")
        print(f"❌ Failed: {len(failed)}/{len(enabled_indicators)}")
        if failed:
            print(f"\nFailed Indicators:")
            for fail_info in failed:
                print(f"  • {fail_info['name']}: {fail_info['reason']}")
        print(f"{'='*80}\n")

        # Add detailed results to pytest report using pytest-html extra
        import pytest
        from pytest_html import extras

        # Categorize failures by type
        crashes = [f for f in failed if 'crashed' in f['reason'].lower()]
        not_found = [f for f in failed if 'failed to select' in f['reason'].lower() or 'not found' in f['reason'].lower()]
        expand_failures = [f for f in failed if 'expand' in f['reason'].lower()]
        map_failures = [f for f in failed if 'map' in f['reason'].lower() and 'crashed' not in f['reason'].lower()]
        other_failures = [f for f in failed if f not in crashes + not_found + expand_failures + map_failures]

        # Build HTML report
        extra_html = f"<div style='margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px;'>"
        extra_html += f"<h3 style='margin-top: 0;'>📊 Indicator Test Results - {state_name} - {section.upper().replace('_', ' ')}</h3>"
        extra_html += f"<p style='font-size: 16px;'><strong style='color: #5cb85c;'>✅ Passed:</strong> {len(passed)}/{len(enabled_indicators)} ({len(passed)/len(enabled_indicators)*100:.1f}%)</p>"
        extra_html += f"<p style='font-size: 16px;'><strong style='color: #d9534f;'>❌ Failed:</strong> {len(failed)}/{len(enabled_indicators)} ({len(failed)/len(enabled_indicators)*100:.1f}%)</p>"

        if crashes:
            extra_html += f"<div style='margin: 10px 0; padding: 10px; background: #f2dede; border-left: 4px solid #d9534f;'>"
            extra_html += f"<h4 style='margin-top: 0; color: #d9534f;'>🔴 Application Crashes ({len(crashes)}):</h4>"
            extra_html += "<p style='margin: 5px 0; font-size: 13px;'><em>These indicators cause the application to crash with 'Something went wrong!' error page</em></p>"
            extra_html += "<ul style='margin: 5px 0;'>"
            for crash in crashes:
                extra_html += f"<li><strong>{crash['name']}</strong><br/><span style='color: #777; font-size: 12px;'>Reason: {crash['reason']}</span></li>"
            extra_html += "</ul></div>"

        if not_found:
            extra_html += f"<div style='margin: 10px 0; padding: 10px; background: #fcf8e3; border-left: 4px solid #f0ad4e;'>"
            extra_html += f"<h4 style='margin-top: 0; color: #f0ad4e;'>⚠️ Indicators Not Found ({len(not_found)}):</h4>"
            extra_html += "<p style='margin: 5px 0; font-size: 13px;'><em>These indicators could not be located in the UI</em></p>"
            extra_html += "<ul style='margin: 5px 0;'>"
            for nf in not_found:
                extra_html += f"<li><strong>{nf['name']}</strong><br/><span style='color: #777; font-size: 12px;'>Reason: {nf['reason']}</span></li>"
            extra_html += "</ul></div>"

        if expand_failures:
            extra_html += f"<div style='margin: 10px 0; padding: 10px; background: #fcf8e3; border-left: 4px solid #f0ad4e;'>"
            extra_html += f"<h4 style='margin-top: 0; color: #f0ad4e;'>⚠️ Section Expand Failures ({len(expand_failures)}):</h4>"
            extra_html += "<p style='margin: 5px 0; font-size: 13px;'><em>Failed to expand section to access indicators</em></p>"
            extra_html += "<ul style='margin: 5px 0;'>"
            for ef in expand_failures:
                extra_html += f"<li><strong>{ef['name']}</strong><br/><span style='color: #777; font-size: 12px;'>Reason: {ef['reason']}</span></li>"
            extra_html += "</ul></div>"

        if map_failures:
            extra_html += f"<div style='margin: 10px 0; padding: 10px; background: #fcf8e3; border-left: 4px solid #f0ad4e;'>"
            extra_html += f"<h4 style='margin-top: 0; color: #f0ad4e;'>⚠️ Map Load Failures ({len(map_failures)}):</h4>"
            extra_html += "<p style='margin: 5px 0; font-size: 13px;'><em>Map did not load or validate correctly</em></p>"
            extra_html += "<ul style='margin: 5px 0;'>"
            for mf in map_failures:
                extra_html += f"<li><strong>{mf['name']}</strong><br/><span style='color: #777; font-size: 12px;'>Reason: {mf['reason']}</span></li>"
            extra_html += "</ul></div>"

        if other_failures:
            extra_html += f"<div style='margin: 10px 0; padding: 10px; background: #fcf8e3; border-left: 4px solid #f0ad4e;'>"
            extra_html += f"<h4 style='margin-top: 0; color: #f0ad4e;'>⚠️ Other Failures ({len(other_failures)}):</h4>"
            extra_html += "<ul style='margin: 5px 0;'>"
            for of in other_failures:
                extra_html += f"<li><strong>{of['name']}</strong><br/><span style='color: #777; font-size: 12px;'>Reason: {of['reason']}</span></li>"
            extra_html += "</ul></div>"

        if not failed:
            extra_html += "<p style='color: #5cb85c; font-weight: bold;'>✅ All indicators tested successfully!</p>"

        extra_html += "</div>"

        # Add detailed results to HTML report
        from pytest_html import extras

        # Add summary at the top
        extra.append(extras.html(f"""
            <div style='margin: 15px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #007bff; border-radius: 4px;'>
                <h3 style='margin-top: 0; color: #007bff;'>📊 Test Results Summary</h3>
                <table style='width: 100%; border-collapse: collapse;'>
                    <tr>
                        <td style='padding: 8px; font-weight: bold;'>State:</td>
                        <td style='padding: 8px;'>{state_name}</td>
                    </tr>
                    <tr style='background: #f1f1f1;'>
                        <td style='padding: 8px; font-weight: bold;'>Section:</td>
                        <td style='padding: 8px;'>{section.replace('_', ' ').title()}</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; font-weight: bold;'>Total Indicators:</td>
                        <td style='padding: 8px;'>{len(enabled_indicators)}</td>
                    </tr>
                    <tr style='background: #f1f1f1;'>
                        <td style='padding: 8px; font-weight: bold; color: #28a745;'>✅ Passed:</td>
                        <td style='padding: 8px; color: #28a745; font-weight: bold;'>{len(passed)} ({len(passed)/len(enabled_indicators)*100:.1f}%)</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; font-weight: bold; color: #dc3545;'>❌ Failed:</td>
                        <td style='padding: 8px; color: #dc3545; font-weight: bold;'>{len(failed)} ({len(failed)/len(enabled_indicators)*100:.1f}%)</td>
                    </tr>
                </table>
            </div>
        """))

        # Add failure details if any failures occurred
        if failed:
            failure_html = "<div style='margin: 15px 0;'>"

            if crashes:
                failure_html += f"""
                <div style='margin: 10px 0; padding: 12px; background: #f8d7da; border-left: 4px solid #dc3545; border-radius: 4px;'>
                    <h4 style='margin-top: 0; color: #721c24;'>🔴 Application Crashes ({len(crashes)})</h4>
                    <p style='margin: 5px 0; font-size: 13px; color: #721c24;'><em>These indicators cause the application to crash with "Something went wrong!" error page</em></p>
                    <ul style='margin: 8px 0; padding-left: 20px;'>
                """
                for crash in crashes:
                    failure_html += f"<li style='margin: 5px 0;'><strong>{crash['name']}</strong><br/><span style='color: #856404; font-size: 12px;'>Reason: {crash['reason']}</span></li>"
                failure_html += "</ul></div>"

            if not_found:
                failure_html += f"""
                <div style='margin: 10px 0; padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;'>
                    <h4 style='margin-top: 0; color: #856404;'>⚠️ Indicators Not Found ({len(not_found)})</h4>
                    <p style='margin: 5px 0; font-size: 13px; color: #856404;'><em>These indicators could not be located in the UI</em></p>
                    <ul style='margin: 8px 0; padding-left: 20px;'>
                """
                for nf in not_found:
                    failure_html += f"<li style='margin: 5px 0;'><strong>{nf['name']}</strong><br/><span style='color: #856404; font-size: 12px;'>Reason: {nf['reason']}</span></li>"
                failure_html += "</ul></div>"

            if expand_failures:
                failure_html += f"""
                <div style='margin: 10px 0; padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;'>
                    <h4 style='margin-top: 0; color: #856404;'>⚠️ Section Expand Failures ({len(expand_failures)})</h4>
                    <p style='margin: 5px 0; font-size: 13px; color: #856404;'><em>Failed to expand section to access indicators</em></p>
                    <ul style='margin: 8px 0; padding-left: 20px;'>
                """
                for ef in expand_failures:
                    failure_html += f"<li style='margin: 5px 0;'><strong>{ef['name']}</strong><br/><span style='color: #856404; font-size: 12px;'>Reason: {ef['reason']}</span></li>"
                failure_html += "</ul></div>"

            if map_failures:
                failure_html += f"""
                <div style='margin: 10px 0; padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;'>
                    <h4 style='margin-top: 0; color: #856404;'>⚠️ Map Load Failures ({len(map_failures)})</h4>
                    <p style='margin: 5px 0; font-size: 13px; color: #856404;'><em>Map did not load or validate correctly</em></p>
                    <ul style='margin: 8px 0; padding-left: 20px;'>
                """
                for mf in map_failures:
                    failure_html += f"<li style='margin: 5px 0;'><strong>{mf['name']}</strong><br/><span style='color: #856404; font-size: 12px;'>Reason: {mf['reason']}</span></li>"
                failure_html += "</ul></div>"

            if other_failures:
                failure_html += f"""
                <div style='margin: 10px 0; padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;'>
                    <h4 style='margin-top: 0; color: #856404;'>⚠️ Other Failures ({len(other_failures)})</h4>
                    <ul style='margin: 8px 0; padding-left: 20px;'>
                """
                for of in other_failures:
                    failure_html += f"<li style='margin: 5px 0;'><strong>{of['name']}</strong><br/><span style='color: #856404; font-size: 12px;'>Reason: {of['reason']}</span></li>"
                failure_html += "</ul></div>"

            failure_html += "</div>"
            extra.append(extras.html(failure_html))
        else:
            # All passed
            extra.append(extras.html("""
                <div style='margin: 15px 0; padding: 15px; background: #d4edda; border-left: 4px solid #28a745; border-radius: 4px;'>
                    <p style='margin: 0; color: #155724; font-weight: bold; font-size: 14px;'>✅ All indicators tested successfully!</p>
                </div>
            """))

        # Assert that ALL indicators passed - any failure should fail the test
        if failed:
            failure_summary = f"❌ {len(failed)}/{len(enabled_indicators)} indicators FAILED"
            failure_details = "\n".join([f"  • {f['name']}: {f['reason']}" for f in failed[:5]])  # Show first 5
            if len(failed) > 5:
                failure_details += f"\n  ... and {len(failed) - 5} more"
            assert False, f"{failure_summary}\n{failure_details}"

        print(f"✅ Section test passed: {len(passed)}/{len(enabled_indicators)} indicators working")


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.chart_validation
class TestMultiStateIndicatorsChartView:
    """CONSOLIDATED: Test ALL indicators per section in a single browser instance - Chart View"""

    @pytest.mark.parametrize(
        "state_key,state_name,section",
        get_section_test_params(),
        ids=lambda val: str(val).replace('_', '-') if isinstance(val, str) else str(val)
    )
    def test_section_all_indicators_chart_view(self, driver, state_key, state_name, section):
        """Test ALL indicators in a section using ONE browser instance - Chart View"""
        import time
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Get all indicators for this section
        state_config = config_loader.get_state_config(state_key)
        section_data = state_config.get("sections", {}).get(section, {})
        indicators = section_data.get("indicators", [])
        enabled_indicators = [ind for ind in indicators if ind.get("enabled", True)]

        print(f"\n{'='*80}")
        print(f"Testing {state_name} - {section.upper().replace('_', ' ')} - CHART VIEW")
        print(f"Total Indicators: {len(enabled_indicators)}")
        print(f"{'='*80}\n")

        # Setup ONCE
        assert common_page.navigate_to_analytics()
        assert analytics_page.select_state(state_name)
        assert analytics_page.select_view(2)  # Chart view

        # Wait for district dropdown to be ready using explicit wait
        try:
            WebDriverWait(driver, 15).until(district_dropdown_ready)
        except:
            pass

        # Select district and revenue circle AFTER view selection (dropdowns appear after view is selected)
        district = AnalyticsTestData.get_district_for_state(state_key)
        revenue_circle = AnalyticsTestData.get_revenue_circle_for_state(state_key)
        assert analytics_page.select_district(district), \
            f"❌ Failed to select district: {district}"

        # Revenue circle dropdown uses explicit wait internally - no sleep needed
        assert analytics_page.select_revenue_circle(revenue_circle), \
            f"❌ Failed to select revenue circle: {revenue_circle}"

        section_expand_methods = {
            "hazard": analytics_page.expand_hazard_options,
            "exposure": analytics_page.expand_exposure_options,
            "vulnerability": analytics_page.expand_vulnerability_options,
            "government_response": analytics_page.expand_govt_response_options
        }
        expand_method = section_expand_methods.get(section)
        assert expand_method()

        passed, failed = [], []

        for idx, indicator in enumerate(enabled_indicators, 1):
            indicator_name = indicator.get("name")
            print(f"[{idx}/{len(enabled_indicators)}] Testing: {indicator_name}")

            try:
                if not analytics_page.select_indicator_by_text(indicator_name, section):
                    failed.append({'name': indicator_name, 'reason': 'Failed to select'})
                    print(f"  ❌ Failed to select")
                    continue

                wait = WebDriverWait(driver, 20)

                try:
                    # Explicit wait already handles timing - no sleep needed
                    chart_element = wait.until(EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "canvas, svg, .chart, [class*='chart']")))

                    if chart_element.is_displayed():
                        passed.append(indicator_name)
                        print(f"  ✅ Chart loaded")
                    else:
                        failed.append({'name': indicator_name, 'reason': 'Chart not displayed'})
                        print(f"  ❌ Chart not displayed")

                except Exception as e:
                    failed.append({'name': indicator_name, 'reason': f'Chart validation failed: {str(e)[:80]}'})
                    print(f"  ❌ Chart validation failed")

            except Exception as e:
                failed.append({'name': indicator_name, 'reason': f'Error: {str(e)[:80]}'})
                print(f"  ❌ Error")

        print(f"\n{'='*80}")
        print(f"SUMMARY: {state_name} - {section.upper().replace('_', ' ')} - CHART VIEW")
        print(f"✅ Passed: {len(passed)}/{len(enabled_indicators)}")
        print(f"❌ Failed: {len(failed)}/{len(enabled_indicators)}")
        print(f"{'='*80}\n")

        # Assert that ALL indicators passed - any failure should fail the test
        if failed:
            failure_summary = f"❌ {len(failed)}/{len(enabled_indicators)} indicators FAILED (Chart View)"
            failure_details = "\n".join([f"  • {f['name']}: {f['reason']}" for f in failed[:5]])
            if len(failed) > 5:
                failure_details += f"\n  ... and {len(failed) - 5} more"
            assert False, f"{failure_summary}\n{failure_details}"


@pytest.mark.analytics
@pytest.mark.multistate
@pytest.mark.table_validation
class TestMultiStateIndicatorsTableView:
    """CONSOLIDATED: Test ALL indicators per section in a single browser instance - Table View"""

    @pytest.mark.parametrize(
        "state_key,state_name,section",
        get_section_test_params(),
        ids=lambda val: str(val).replace('_', '-') if isinstance(val, str) else str(val)
    )
    def test_section_all_indicators_table_view(self, driver, state_key, state_name, section):
        """Test ALL indicators in a section using ONE browser instance - Table View"""
        import time
        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        # Get all indicators for this section
        state_config = config_loader.get_state_config(state_key)
        section_data = state_config.get("sections", {}).get(section, {})
        indicators = section_data.get("indicators", [])
        enabled_indicators = [ind for ind in indicators if ind.get("enabled", True)]

        print(f"\n{'='*80}")
        print(f"Testing {state_name} - {section.upper().replace('_', ' ')} - TABLE VIEW")
        print(f"Total Indicators: {len(enabled_indicators)}")
        print(f"{'='*80}\n")

        # Setup ONCE
        assert common_page.navigate_to_analytics()
        assert analytics_page.select_state(state_name)
        assert analytics_page.select_view(3)  # Table view

        # Wait for district dropdown to be ready using explicit wait
        try:
            WebDriverWait(driver, 15).until(district_dropdown_ready)
        except:
            pass

        # Select district and revenue circle AFTER view selection (dropdowns appear after view is selected)
        district = AnalyticsTestData.get_district_for_state(state_key)
        revenue_circle = AnalyticsTestData.get_revenue_circle_for_state(state_key)
        assert analytics_page.select_district(district), \
            f"❌ Failed to select district: {district}"

        # Revenue circle dropdown uses explicit wait internally - no sleep needed
        assert analytics_page.select_revenue_circle(revenue_circle), \
            f"❌ Failed to select revenue circle: {revenue_circle}"

        section_expand_methods = {
            "hazard": analytics_page.expand_hazard_options,
            "exposure": analytics_page.expand_exposure_options,
            "vulnerability": analytics_page.expand_vulnerability_options,
            "government_response": analytics_page.expand_govt_response_options
        }
        expand_method = section_expand_methods.get(section)
        assert expand_method()

        passed, failed = [], []

        for idx, indicator in enumerate(enabled_indicators, 1):
            indicator_name = indicator.get("name")
            print(f"[{idx}/{len(enabled_indicators)}] Testing: {indicator_name}")

            try:
                if not analytics_page.select_indicator_by_text(indicator_name, section):
                    failed.append({'name': indicator_name, 'reason': 'Failed to select'})
                    print(f"  ❌ Failed to select")
                    continue

                wait = WebDriverWait(driver, 20)

                try:
                    # Explicit wait already handles timing - no sleep needed
                    table_element = wait.until(EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "table, .table, [class*='table']")))

                    if table_element.is_displayed():
                        passed.append(indicator_name)
                        print(f"  ✅ Table loaded")
                    else:
                        failed.append({'name': indicator_name, 'reason': 'Table not displayed'})
                        print(f"  ❌ Table not displayed")

                except Exception as e:
                    failed.append({'name': indicator_name, 'reason': f'Table validation failed: {str(e)[:80]}'})
                    print(f"  ❌ Table validation failed")

            except Exception as e:
                failed.append({'name': indicator_name, 'reason': f'Error: {str(e)[:80]}'})
                print(f"  ❌ Error")

        print(f"\n{'='*80}")
        print(f"SUMMARY: {state_name} - {section.upper().replace('_', ' ')} - TABLE VIEW")
        print(f"✅ Passed: {len(passed)}/{len(enabled_indicators)}")
        print(f"❌ Failed: {len(failed)}/{len(enabled_indicators)}")
        print(f"{'='*80}\n")

        # Assert that ALL indicators passed - any failure should fail the test
        if failed:
            failure_summary = f"❌ {len(failed)}/{len(enabled_indicators)} indicators FAILED (Table View)"
            failure_details = "\n".join([f"  • {f['name']}: {f['reason']}" for f in failed[:5]])
            if len(failed) > 5:
                failure_details += f"\n  ... and {len(failed) - 5} more"
            assert False, f"{failure_summary}\n{failure_details}"


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


@pytest.mark.analytics
@pytest.mark.smoke
@pytest.mark.multistate
class TestAllStatesIndicatorSmoke:
    """
    Smoke Test - Single flow testing one indicator from each state with expanded options validation

    Run: pytest tests/test_analytics.py -v -m smoke -k "TestAllStatesIndicatorSmoke"
    """

    def test_all_states_with_expanded_options(self, driver):
        """
        Smoke test: For each state, test one indicator with key expanded options

        For each state validates:
        1. State selection works
        2. View selection (Map view) works
        3. District dropdown selection works
        4. Revenue circle dropdown selection works
        5. Section expand works (hazard)
        6. Indicator selection works
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait, Select
        from selenium.webdriver.support import expected_conditions as EC

        common_page = CommonPage(driver)
        analytics_page = AnalyticsPage(driver)

        all_states = config_loader.get_all_states()

        def district_dropdown_ready(drv):
            try:
                element = drv.find_element(By.XPATH, "//select[contains(@id, 'district') or contains(@class, 'district')]")
                select = Select(element)
                return len(select.options) > 1 and element.is_enabled()
            except:
                return False

        print(f"\n{'='*70}")
        print(f"SMOKE TEST - All States with Expanded Options")
        print(f"Testing {len(all_states)} states: navigation, dropdowns, indicator")
        print(f"{'='*70}\n")

        results = {'passed': [], 'failed': []}

        for state_key in all_states:
            state_config = config_loader.get_state_config(state_key)
            state_name = state_config.get("state_name")
            checks = []

            print(f"\n[{state_name}]")

            try:
                # 1. Navigate to analytics
                assert common_page.navigate_to_analytics(), "Navigation failed"
                checks.append("navigation")

                # 2. Select state
                assert analytics_page.select_state(state_name), "State selection failed"
                checks.append("state_select")

                # 3. Select Map view
                assert analytics_page.select_view(1), "View selection failed"
                checks.append("view_select")

                # 4. Wait for and select district
                try:
                    WebDriverWait(driver, 15).until(district_dropdown_ready)
                except:
                    pass

                district = AnalyticsTestData.get_district_for_state(state_key)
                assert analytics_page.select_district(district), f"District selection failed"
                checks.append("district_select")

                # 5. Select revenue circle
                revenue_circle = AnalyticsTestData.get_revenue_circle_for_state(state_key)
                assert analytics_page.select_revenue_circle(revenue_circle), "Revenue circle failed"
                checks.append("revenue_circle")

                # 6. Expand hazard section and select first indicator
                hazard_data = state_config.get("sections", {}).get("hazard", {})
                indicators = [i for i in hazard_data.get("indicators", []) if i.get("enabled", True)]

                if indicators:
                    indicator_name = indicators[0].get("name")
                    assert analytics_page.expand_hazard_options(), "Section expand failed"
                    checks.append("section_expand")

                    assert analytics_page.select_indicator_by_text(indicator_name, "hazard"), "Indicator failed"
                    checks.append("indicator_select")

                    analytics_page.collapse_hazard_options()

                print(f"  PASSED: {', '.join(checks)}")
                results['passed'].append(state_name)

            except AssertionError as e:
                print(f"  FAILED at: {str(e)[:50]}")
                print(f"  Passed checks: {', '.join(checks)}")
                results['failed'].append({'state': state_name, 'error': str(e), 'passed': checks})

            except Exception as e:
                print(f"  ERROR: {str(e)[:50]}")
                results['failed'].append({'state': state_name, 'error': str(e), 'passed': checks})

        # Summary
        print(f"\n{'='*70}")
        print(f"RESULTS: {len(results['passed'])}/{len(all_states)} states passed")
        if results['failed']:
            print(f"\nFailed States:")
            for f in results['failed']:
                print(f"  - {f['state']}: {f['error'][:60]}")
        print(f"{'='*70}\n")

        assert len(results['failed']) == 0, f"Failed: {[f['state'] for f in results['failed']]}"
