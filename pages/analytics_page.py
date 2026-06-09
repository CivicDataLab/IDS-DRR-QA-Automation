from pages.base_page import BasePage
from locators.analytics_locators import (
    AnalyticsPageLocators,
    HazardLocators,
    ExposureLocators,
    VulnerabilityLocators,
    GovtResponseLocators
)
from config.config import Config


class AnalyticsPage(BasePage):
    """Page Object for Analytics page"""

    def __init__(self, driver):
        super().__init__(driver)
        self.screenshot_dir = Config.ANALYTICS_SCREENSHOTS_DIR

    def is_error_page_displayed(self):
        """
        Check if the error page 'Something went wrong!' is displayed

        Returns:
            bool: True if error page is shown, False otherwise
        """
        from selenium.webdriver.common.by import By
        try:
            # Check for common error messages
            error_indicators = [
                "//h1[contains(text(), 'Something went wrong')]",
                "//h2[contains(text(), 'Something went wrong')]",
                "//div[contains(text(), 'Something went wrong')]",
                "//button[contains(text(), 'Try again')]",
                "//*[contains(@class, 'error-page')]",
                "//*[contains(@class, 'error-boundary')]"
            ]

            for xpath in error_indicators:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements and elements[0].is_displayed():
                    return True

            return False
        except Exception:
            return False

    def _wait_for_page_load_complete(self, timeout=30):
        """Wait for page to complete loading - checks for loading spinners"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        import time

        try:
            # Wait for common loading indicators to disappear
            loading_selectors = [
                "//div[contains(text(), 'Loading')]",
                "//*[contains(@class, 'loading')]",
                "//*[contains(@class, 'spinner')]",
                "//div[contains(@class, 'loader')]"
            ]

            for selector in loading_selectors:
                try:
                    WebDriverWait(self.driver, 2).until_not(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                except TimeoutException:
                    # Loading indicator not found or already gone
                    pass

            # Wait for document ready state instead of fixed sleep
            from utils.wait_helpers import wait_for_document_ready
            wait_for_document_ready(self.driver, timeout=5)
            return True
        except Exception as e:
            print(f"⚠️  Warning during load wait: {e}")
            return True  # Don't fail the test if we can't detect loading

    def select_state(self, state_name):
        """
        Select a state from the sidebar - handles both dropdown and list item approaches

        Args:
            state_name: Name of the state to select (e.g., "Assam", "Himachal pradesh")

        Returns:
            bool: Success status
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait, Select
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import (
            NoSuchElementException,
            StaleElementReferenceException,
            ElementNotInteractableException,
            TimeoutException
        )
        import time

        # First, wait for any existing page loads to complete
        self._wait_for_page_load_complete()

        max_retries = 3

        for attempt in range(max_retries):
            try:
                wait = WebDriverWait(self.driver, 15)

                # APPROACH 1: Try to find <select> dropdown with name="State"
                try:
                    select_element = wait.until(
                        EC.presence_of_element_located((By.NAME, "State"))
                    )
                    select = Select(select_element)
                    available_options = [opt.text.strip() for opt in select.options]
                    print(f"📋 Found <select> dropdown with states: {', '.join(available_options[:5])}...")

                    # Check if already selected
                    current_selection = select.first_selected_option.text.strip()
                    if current_selection.lower() == state_name.lower():
                        print(f"ℹ️  State '{state_name}' is already selected, skipping re-selection")
                        self._wait_for_page_load_complete()
                        return True

                    # Try exact match first
                    selected = False
                    try:
                        select.select_by_visible_text(state_name)
                        selected = True
                        print(f"✅ Selected state: {state_name}")
                    except NoSuchElementException:
                        # Try case-insensitive match
                        for option in select.options:
                            if option.text.strip().lower() == state_name.lower():
                                select.select_by_visible_text(option.text.strip())
                                selected = True
                                print(f"✅ Selected state: {option.text.strip()}")
                                break

                    if selected:
                        # Wait for page to reload after state change
                        self._wait_for_page_load_complete()
                        return True
                    else:
                        print(f"❌ State '{state_name}' not found in dropdown options: {available_options}")
                        return False

                except TimeoutException:
                    # APPROACH 2: Fallback to sidebar list item approach
                    print(f"⚠️  <select> dropdown not found, trying sidebar list item approach...")

                    # Use case-insensitive XPath for sidebar list items
                    state_xpath = f"//li[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{state_name.lower()}')]"

                    state_element = wait.until(
                        EC.presence_of_element_located((By.XPATH, state_xpath))
                    )

                    # Scroll into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", state_element)
                    # Click the state
                    success = self.click((By.XPATH, state_xpath), f"State: {state_name}")
                    if success:
                        # Wait for page to reload after state change
                        self._wait_for_page_load_complete()
                        print(f"✅ Selected state: {state_name}")
                        return True
                    else:
                        self._capture_failure_screenshot(f"state_click_failed_{state_name}")
                        return False

            except (StaleElementReferenceException, ElementNotInteractableException) as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  State selection failed ({type(e).__name__}), retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Failed to select state {state_name} after {max_retries} attempts: {e}")
                    self._capture_failure_screenshot(f"state_selection_error_{state_name}")
                    return False
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Attempt {attempt + 1} failed: {type(e).__name__}: {e}")
                    print(f"⚠️  Retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Failed to select state {state_name}: {type(e).__name__}: {e}")
                    self._capture_failure_screenshot(f"state_selection_exception_{state_name}")
                    return False

        return False

    def _capture_failure_screenshot(self, filename):
        """Capture screenshot on failure for debugging"""
        try:
            import os
            screenshot_path = os.path.join(self.screenshot_dir, f"{filename}.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Failure screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"⚠️  Could not save failure screenshot: {e}")

    def get_current_state(self):
        """
        Get the currently selected state

        Returns:
            str: Current state name or None
        """
        from selenium.webdriver.common.by import By

        try:
            # Find the active/selected state in the sidebar
            active_state_xpath = "//li[contains(@class, 'selected') or contains(@class, 'active')]"
            element = self.find_element((By.XPATH, active_state_xpath))

            if element:
                return element.text.strip()

        except Exception as e:
            print(f"⚠️  Could not determine current state: {e}")

        return None

    def select_view(self, view_index):
        """
        Select analytics view (1=Map, 2=Chart, 3=Table)

        Args:
            view_index: View index (1, 2, or 3)

        Returns:
            bool: Success status (False if invalid index)
        """
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Validate view_index
        if view_index not in [1, 2, 3]:
            print(f"❌ Invalid view index: {view_index}. Must be 1, 2, or 3")
            return False

        locator = AnalyticsPageLocators.get_view_button(view_index)
        view_names = {1: "Map View", 2: "Chart View", 3: "Table View"}

        # Retry logic for stale elements
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = self.click(locator, view_names.get(view_index, f"View {view_index}"))
                if result:
                    return True
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element encountered, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Failed after {max_retries} attempts due to stale elements")
                    return False

        return False

    def wait_for_district_dropdown(self, timeout=20):
        """
        Wait for the district dropdown to appear and have selectable options.

        This is called after selecting a view (Chart/Table/Map) because the district
        dropdown is only rendered once a view is active. Uses the actual DISTRICT_SELECT
        locator so the wait is consistent with the selection step.

        Returns:
            bool: True if dropdown is ready, False if timed out
        """
        from utils.wait_helpers import wait_for_dropdown_options
        print(f"⏳ Waiting for district dropdown to be ready...")
        ready = wait_for_dropdown_options(
            self.driver,
            AnalyticsPageLocators.DISTRICT_SELECT,
            timeout=timeout,
            min_options=1
        )
        if ready:
            print(f"✅ District dropdown ready")
        else:
            print(f"⚠️ District dropdown did not populate within {timeout}s")
        return ready

    def select_district(self, district_name):
        """Select district from dropdown and wait for revenue circle dropdown to be ready"""
        from utils.wait_helpers import wait_for_dropdown_options, wait_for_dropdown_option_text

        # Wait for district dropdown to have options before attempting selection.
        # The dropdown is dynamically rendered after view selection, so we must
        # wait for it explicitly — page load complete alone is not sufficient.
        self.wait_for_district_dropdown(timeout=20)

        # Guard against stale options from a previously-selected state (browser is
        # reused across states): wait until THIS district has actually loaded.
        wait_for_dropdown_option_text(
            self.driver, AnalyticsPageLocators.DISTRICT_SELECT, district_name, timeout=20
        )

        success = self.select_dropdown_by_text(
            AnalyticsPageLocators.DISTRICT_SELECT,
            district_name,
            "District Dropdown"
        )
        if success:
            print(f"Selected district: {district_name}")
            # Wait for revenue circle dropdown to populate (triggered by district onChange)
            print(f"⏳ Waiting for revenue circle/block dropdown to become ready...")
            wait_for_dropdown_options(
                self.driver,
                AnalyticsPageLocators.REVENUE_CIRCLE_SELECT,
                timeout=20,
                min_options=1
            )
        return success

    def select_revenue_circle(self, revenue_circle_name):
        """
        Select revenue circle/block from dropdown with explicit wait for options to populate.

        The revenue circle dropdown is dependent on district selection and requires time
        to fetch and populate options. This method waits explicitly for the dropdown to
        have more than just the placeholder option before attempting selection.

        Args:
            revenue_circle_name: Name of revenue circle/block to select

        Returns:
            bool: True if successful, False otherwise
        """
        from selenium.webdriver.support.ui import Select
        from utils.wait_helpers import wait_for_dropdown_options, wait_for_dropdown_option_text

        # Wait for page load to complete
        self._wait_for_page_load_complete()

        # Double-check dropdown has options (should already be populated from select_district)
        print(f"✅ Verifying revenue circle/block dropdown has options...")
        if wait_for_dropdown_options(self.driver, AnalyticsPageLocators.REVENUE_CIRCLE_SELECT, timeout=5):
            print(f"✅ Dropdown ready for selection")
        else:
            print(f"⚠️ Timeout waiting for dropdown to populate")
            try:
                element = self.find_element(AnalyticsPageLocators.REVENUE_CIRCLE_SELECT)
                if element:
                    select = Select(element)
                    available = [opt.text for opt in select.options]
                    print(f"   Available options: {available}")
            except Exception:
                pass
            return False

        # Guard against stale revenue circles from the previous district/state:
        # wait until THIS revenue circle has loaded before selecting.
        wait_for_dropdown_option_text(
            self.driver, AnalyticsPageLocators.REVENUE_CIRCLE_SELECT, revenue_circle_name, timeout=20
        )

        success = self.select_dropdown_by_text(
            AnalyticsPageLocators.REVENUE_CIRCLE_SELECT,
            revenue_circle_name,
            "Revenue Circle Dropdown"
        )
        if success:
            print(f"Selected revenue circle: {revenue_circle_name}")
        return success

    def open_calendar(self):
        """Open calendar picker"""
        return self.click(AnalyticsPageLocators.CALENDAR_BUTTON, "Calendar Button")

    def select_calendar_month(self, month):
        """
        Select month from calendar

        Args:
            month: Month value (as string)

        Returns:
            bool: Success status
        """
        locator = AnalyticsPageLocators.get_calendar_month(month)
        return self.click(locator, f"Calendar Month {month}")

    def take_analytics_screenshot(self, filename_prefix, description=""):
        """
        Take screenshot with analytics directory

        Args:
            filename_prefix: Prefix for filename
            description: Optional description for filename
        """
        filename = f"{filename_prefix}{description}.png" if description else f"{filename_prefix}.png"
        return self.take_screenshot(filename, self.screenshot_dir)

    # Hazard Section Methods
    def expand_hazard_options(self, screenshot_prefix=None):
        """Expand Hazard options section (only if not already expanded)"""
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

        # Check if already expanded to avoid collapsing it
        try:
            parent_element = self.find_element(HazardLocators.EXPAND_COLLAPSE, use_healing=False)
            if parent_element:
                aria_expanded = parent_element.get_attribute('aria-expanded')
                if aria_expanded == 'true':
                    print("✅ Hazard section already expanded")
                    return True
        except Exception:
            pass

        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = self.interact_with_option(
                    HazardLocators.EXPAND_COLLAPSE,
                    "Hazard Options",
                    f"{screenshot_prefix}hazard_show_options" if screenshot_prefix else None,
                    self.screenshot_dir
                )
                if result:
                    return True
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element in expand_hazard_options, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    return False
        return False

    def collapse_hazard_options(self):
        """Collapse Hazard options section with enhanced fallback logic"""
        import time
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

        # Wait for page to be ready
        self._wait_for_page_load_complete()
        max_retries = 3
        for attempt in range(max_retries):
            try:
                parent_element = self.find_element(HazardLocators.EXPAND_COLLAPSE, use_healing=False)
                if not parent_element:
                    print("⚠️ Hazard section element not found")
                    return False

                # Check if the section is expanded before trying to collapse
                aria_expanded = parent_element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Hazard Options already collapsed")
                    return True

                # APPROACH 1: Try hover-based collapse button (for larger sections)
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(parent_element).perform()

                    collapse_button = self.find_element(HazardLocators.COLLAPSE_BUTTON, use_healing=False)
                    if collapse_button and collapse_button.is_displayed():
                        collapse_button.click()
                        print("✅ Hazard Options collapsed successfully (hover method)")
                        return True
                except Exception as hover_error:
                    print(f"⚠️ Hover method failed: {hover_error}, trying fallback...")

                # APPROACH 2: Direct click on parent element (toggle behavior)
                try:
                    parent_element.click()

                    # Verify it collapsed
                    parent_element = self.find_element(HazardLocators.EXPAND_COLLAPSE, use_healing=False)
                    if parent_element:
                        aria_expanded = parent_element.get_attribute('aria-expanded')
                        if aria_expanded == 'false':
                            print("✅ Hazard Options collapsed successfully (direct click)")
                            return True
                except Exception as click_error:
                    print(f"⚠️ Direct click failed: {click_error}")

                # APPROACH 3: JavaScript click as last resort
                try:
                    self.driver.execute_script("arguments[0].click();", parent_element)
                    print("✅ Hazard Options collapsed successfully (JavaScript click)")
                    return True
                except Exception as js_error:
                    print(f"⚠️ JavaScript click failed: {js_error}")

                # If we got here, retry
                if attempt < max_retries - 1:
                    print(f"⚠️ Collapse attempt {attempt + 1} failed, retrying...")
                    continue

            except (StaleElementReferenceException, TimeoutException) as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Stale element in collapse, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Failed to collapse Hazard Options after {max_retries} attempts: {e}")
                    return False
            except Exception as e:
                print(f"❌ Error in collapse_hazard_options: {e}")
                if attempt < max_retries - 1:
                    continue
                return False

        return False

    def select_indicator_by_text(self, indicator_text, section_name="Indicator"):
        """
        Dynamically select an indicator by its text label (supports any indicator)
        With retry logic for stale elements and dynamic DOM updates

        Args:
            indicator_text: The exact text of the indicator (e.g., "Total Monthly Rainfall")
            section_name: Section name for logging (Hazard, Exposure, etc.)

        Returns:
            bool: Success status
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
        import time

        # Wait for page to stabilize
        self._wait_for_page_load_complete()
        max_retries = 3
        for attempt in range(max_retries):
            try:
                wait = WebDriverWait(self.driver, 20)  # Increased timeout for parallel execution

                # Fix XPath injection for indicators with apostrophes by using concat
                # If indicator_text contains apostrophes, we need to escape them properly
                if "'" in indicator_text:
                    # Split on apostrophes and use concat to build the XPath string
                    parts = indicator_text.split("'")
                    xpath_string = "concat(" + ", \"'\", ".join([f"'{part}'" for part in parts]) + ")"
                    label_xpath = f"//label[@aria-label={xpath_string}]"
                else:
                    label_xpath = f"//label[@aria-label='{indicator_text}']"

                try:
                    label_element = wait.until(
                        EC.element_to_be_clickable((By.XPATH, label_xpath))
                    )
                except TimeoutException:
                    # Fallback: try finding by visible text in span with proper apostrophe handling
                    if "'" in indicator_text:
                        parts = indicator_text.split("'")
                        xpath_string = "concat(" + ", \"'\", ".join([f"'{part}'" for part in parts]) + ")"
                        label_xpath = f"//label[.//span[normalize-space()={xpath_string}]]"
                    else:
                        label_xpath = f"//label[.//span[normalize-space()='{indicator_text}']]"

                    label_element = wait.until(
                        EC.element_to_be_clickable((By.XPATH, label_xpath))
                    )

                # Scroll into view with retry for stale element
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", label_element)
                except StaleElementReferenceException:
                    if attempt < max_retries - 1:
                        print(f"⚠️  Stale element during scroll, retrying ({attempt + 1}/{max_retries})...")
                        continue

                # Click the label with retry for stale element
                try:
                    label_element.click()
                except StaleElementReferenceException:
                    if attempt < max_retries - 1:
                        print(f"⚠️  Stale element during click, retrying ({attempt + 1}/{max_retries})...")
                        continue
                    else:
                        raise
                except:
                    # JavaScript click fallback
                    self.driver.execute_script("arguments[0].click();", label_element)

                print(f"✅ Selected indicator: {indicator_text}")
                return True

            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element in select_indicator, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Indicator element remained stale after {max_retries} attempts")
                    return False

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Error on attempt {attempt + 1}, retrying...")
                    continue

                print(f"❌ Failed to select indicator '{indicator_text}': {e}")
                break  # Exit retry loop on final failure

        # If we get here, all retries failed - show debug info
        # DEBUG: Show what indicators ARE available
        try:
            available_indicators = self.driver.find_elements(By.XPATH, "//label[@aria-label]")
            if available_indicators:
                print(f"📋 Available indicators in UI ({len(available_indicators)}):")
                for idx, label in enumerate(available_indicators[:15], 1):  # Show first 15
                    aria_label = label.get_attribute('aria-label')
                    if aria_label:
                        print(f"   {idx}. {aria_label}")
                if len(available_indicators) > 15:
                    print(f"   ... and {len(available_indicators) - 15} more")
            else:
                print("⚠️  No indicators with aria-label found in UI")
        except Exception as debug_err:
            print(f"⚠️  Could not list available indicators: {debug_err}")

        return False

    def select_hazard_option(self, option_name, screenshot_prefix=None):
        """
        Select a hazard option

        Args:
            option_name: Name of the hazard option (monthly_rainfall, inundation, elevation)
            screenshot_prefix: Prefix for screenshot

        Returns:
            bool: Success status
        """
        hazard_options = {
            'monthly_rainfall': (HazardLocators.TOTAL_MONTHLY_RAINFALL, "Total Monthly Rainfall", "monthly_rainfall"),
            'inundation': (HazardLocators.SUM_INUNDATION_INTENSITIES, "Sum of Inundation Intensities", "sum_inundation_ratio"),
            'elevation': (HazardLocators.MEAN_ELEVATION, "Mean Elevation", "mean_elevation")
        }

        if option_name not in hazard_options:
            print(f"❌ Unknown hazard option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = hazard_options[option_name]
        screenshot_name = f"{screenshot_prefix}hazard_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)

    # Exposure Section Methods
    def expand_exposure_options(self, screenshot_prefix=None):
        """Expand Exposure options section (only if not already expanded)"""
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

        # Check if already expanded to avoid collapsing it
        try:
            parent_element = self.find_element(ExposureLocators.EXPAND_COLLAPSE, use_healing=False)
            if parent_element:
                aria_expanded = parent_element.get_attribute('aria-expanded')
                if aria_expanded == 'true':
                    print("✅ Exposure section already expanded")
                    return True
        except Exception:
            pass

        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = self.interact_with_option(
                    ExposureLocators.EXPAND_COLLAPSE,
                    "Exposure Options",
                    f"{screenshot_prefix}exposure_show_options" if screenshot_prefix else None,
                    self.screenshot_dir
                )
                if result:
                    return True
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element in expand_exposure_options, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    return False
        return False

    def collapse_exposure_options(self):
        """Collapse Exposure options section with enhanced fallback logic"""
        import time
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

        # Wait for page to be ready
        self._wait_for_page_load_complete()
        max_retries = 3
        for attempt in range(max_retries):
            try:
                parent_element = self.find_element(ExposureLocators.EXPAND_COLLAPSE, use_healing=False)
                if not parent_element:
                    print("⚠️ Exposure section element not found")
                    return False

                # Check if the section is expanded before trying to collapse
                aria_expanded = parent_element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Exposure Options already collapsed")
                    return True

                # APPROACH 1: Try hover-based collapse button (for larger sections)
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(parent_element).perform()

                    collapse_button = self.find_element(ExposureLocators.COLLAPSE_BUTTON, use_healing=False)
                    if collapse_button and collapse_button.is_displayed():
                        collapse_button.click()
                        print("✅ Exposure Options collapsed successfully (hover method)")
                        return True
                except Exception as hover_error:
                    print(f"⚠️ Hover method failed: {hover_error}, trying fallback...")

                # APPROACH 2: Direct click on parent element (toggle behavior)
                try:
                    parent_element.click()

                    # Verify it collapsed
                    parent_element = self.find_element(ExposureLocators.EXPAND_COLLAPSE, use_healing=False)
                    if parent_element:
                        aria_expanded = parent_element.get_attribute('aria-expanded')
                        if aria_expanded == 'false':
                            print("✅ Exposure Options collapsed successfully (direct click)")
                            return True
                except Exception as click_error:
                    print(f"⚠️ Direct click failed: {click_error}")

                # APPROACH 3: JavaScript click as last resort
                try:
                    self.driver.execute_script("arguments[0].click();", parent_element)
                    print("✅ Exposure Options collapsed successfully (JavaScript click)")
                    return True
                except Exception as js_error:
                    print(f"⚠️ JavaScript click failed: {js_error}")

                # If we got here, retry
                if attempt < max_retries - 1:
                    print(f"⚠️ Collapse attempt {attempt + 1} failed, retrying...")
                    continue

            except (StaleElementReferenceException, TimeoutException) as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Stale element in collapse, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Failed to collapse Exposure Options after {max_retries} attempts: {e}")
                    return False
            except Exception as e:
                print(f"❌ Error in collapse_exposure_options: {e}")
                if attempt < max_retries - 1:
                    continue
                return False

        return False

    def select_exposure_option(self, option_name, screenshot_prefix=None):
        """
        Select an exposure option

        Args:
            option_name: Name of the exposure option
            screenshot_prefix: Prefix for screenshot

        Returns:
            bool: Success status
        """
        exposure_options = {
            'households': (ExposureLocators.TOTAL_HOUSEHOLDS, "Total Households", "total_households"),
            'population': (ExposureLocators.POPULATION, "Population", "population"),
            'elderly': (ExposureLocators.ELDERLY_POPULATION, "Elderly Population", "elderly_population"),
            'children': (ExposureLocators.CHILDREN_POPULATION, "Children Population", "children_population")
        }

        if option_name not in exposure_options:
            print(f"❌ Unknown exposure option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = exposure_options[option_name]
        screenshot_name = f"{screenshot_prefix}exposure_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)

    # Vulnerability Section Methods
    def expand_vulnerability_options(self, screenshot_prefix=None):
        """Expand Vulnerability options section (only if not already expanded)"""
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

        # Check if already expanded to avoid collapsing it
        try:
            parent_element = self.find_element(VulnerabilityLocators.EXPAND_COLLAPSE, use_healing=False)
            if parent_element:
                aria_expanded = parent_element.get_attribute('aria-expanded')
                if aria_expanded == 'true':
                    print("✅ Vulnerability section already expanded")
                    return True
        except Exception:
            pass

        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = self.interact_with_option(
                    VulnerabilityLocators.EXPAND_COLLAPSE,
                    "Vulnerability Options",
                    f"{screenshot_prefix}vulnerability_show_options" if screenshot_prefix else None,
                    self.screenshot_dir
                )
                if result:
                    return True
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element in expand_vulnerability_options, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    return False
        return False

    def collapse_vulnerability_options(self):
        """Collapse Vulnerability options section with enhanced fallback logic"""
        import time
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

        # Wait for page to be ready
        self._wait_for_page_load_complete()
        max_retries = 3
        for attempt in range(max_retries):
            try:
                parent_element = self.find_element(VulnerabilityLocators.EXPAND_COLLAPSE, use_healing=False)
                if not parent_element:
                    print("⚠️ Vulnerability section element not found")
                    return False

                # Check if the section is expanded before trying to collapse
                aria_expanded = parent_element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Vulnerability Options already collapsed")
                    return True

                # APPROACH 1: Try hover-based collapse button (for larger sections)
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(parent_element).perform()

                    collapse_button = self.find_element(VulnerabilityLocators.COLLAPSE_BUTTON, use_healing=False)
                    if collapse_button and collapse_button.is_displayed():
                        collapse_button.click()
                        print("✅ Vulnerability Options collapsed successfully (hover method)")
                        return True
                except Exception as hover_error:
                    print(f"⚠️ Hover method failed: {hover_error}, trying fallback...")

                # APPROACH 2: Direct click on parent element (toggle behavior)
                try:
                    parent_element.click()

                    # Verify it collapsed
                    parent_element = self.find_element(VulnerabilityLocators.EXPAND_COLLAPSE, use_healing=False)
                    if parent_element:
                        aria_expanded = parent_element.get_attribute('aria-expanded')
                        if aria_expanded == 'false':
                            print("✅ Vulnerability Options collapsed successfully (direct click)")
                            return True
                except Exception as click_error:
                    print(f"⚠️ Direct click failed: {click_error}")

                # APPROACH 3: JavaScript click as last resort
                try:
                    self.driver.execute_script("arguments[0].click();", parent_element)
                    print("✅ Vulnerability Options collapsed successfully (JavaScript click)")
                    return True
                except Exception as js_error:
                    print(f"⚠️ JavaScript click failed: {js_error}")

                # If we got here, retry
                if attempt < max_retries - 1:
                    print(f"⚠️ Collapse attempt {attempt + 1} failed, retrying...")
                    continue

            except (StaleElementReferenceException, TimeoutException) as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Stale element in collapse, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Failed to collapse Vulnerability Options after {max_retries} attempts: {e}")
                    return False
            except Exception as e:
                print(f"❌ Error in collapse_vulnerability_options: {e}")
                if attempt < max_retries - 1:
                    continue
                return False

        return False

    def select_vulnerability_option(self, option_name, screenshot_prefix=None):
        """Select a vulnerability option"""
        vulnerability_options = {
            'health_centres': (VulnerabilityLocators.HEALTH_CENTRES, "Health Centres", "health_centre"),
            'electricity': (VulnerabilityLocators.DOMESTIC_ELECTRICITY, "Domestic Electricity", "domestic_electricity"),
            'water': (VulnerabilityLocators.PIPED_WATER, "Piped Water", "piped_water"),
            'sanitation': (VulnerabilityLocators.WITHOUT_SANITATION, "Without Sanitation", "without_sanitation"),
            'schools': (VulnerabilityLocators.NUMBER_OF_SCHOOLS, "Number of Schools", "number_schools"),
            'rail': (VulnerabilityLocators.RAIL_LENGTH, "Rail Length", "rail_length"),
            'road': (VulnerabilityLocators.ROAD_LENGTH, "Road Length", "road_length"),
            'sown_area': (VulnerabilityLocators.NET_SOWN_AREA, "Net Sown Area", "sown_area"),
            'sex_ratio': (VulnerabilityLocators.MEAN_SEX_RATIO, "Mean Sex Ratio", "sex_ratio"),
            'population_affected': (VulnerabilityLocators.POPULATION_AFFECTED, "Population Affected", "population_affected"),
            'lives_lost': (VulnerabilityLocators.HUMAN_LIVES_LOST, "Human Lives Lost", "humans_life_lost"),
            'crop_affected': (VulnerabilityLocators.CROP_AREA_AFFECTED, "Crop Area Affected", "crop_area_affected"),
            'embankments_affected': (VulnerabilityLocators.EMBANKMENTS_AFFECTED, "Embankments Affected", "embankments_affected"),
            'roads_damaged': (VulnerabilityLocators.ROADS_DAMAGED, "Roads Damaged", "roads_damaged"),
            'bridges_damaged': (VulnerabilityLocators.BRIDGES_DAMAGED, "Bridges Damaged", "bridges_damaged"),
            'embankments_breached': (VulnerabilityLocators.EMBANKMENTS_BREACHED, "Embankments Breached", "embankments_breached")
        }

        if option_name not in vulnerability_options:
            print(f"❌ Unknown vulnerability option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = vulnerability_options[option_name]
        screenshot_name = f"{screenshot_prefix}vulnerability_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)

    # Government Response Section Methods
    def expand_govt_response_options(self, screenshot_prefix=None):
        """Expand Government Response options section (called once before testing all indicators)"""
        import time
        from selenium.common.exceptions import StaleElementReferenceException

        # Wait for page to be ready
        self._wait_for_page_load_complete()

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Scroll to element with JavaScript for reliability
                try:
                    parent_element = self.find_element(GovtResponseLocators.EXPAND_COLLAPSE, use_healing=False)
                    if parent_element:
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", parent_element)
                except:
                    # Fallback scroll
                    self.scroll_to_element(GovtResponseLocators.EXPAND_COLLAPSE)
                # Click to expand
                result = self.interact_with_option(
                    GovtResponseLocators.EXPAND_COLLAPSE,
                    "Government Response Options",
                    f"{screenshot_prefix}govt_response_show_options" if screenshot_prefix else None,
                    self.screenshot_dir
                )
                if result:
                    return True

                # If interact_with_option returned False, retry
                if attempt < max_attempts - 1:
                    print(f"⚠️  Expand click failed, retrying (attempt {attempt + 2}/{max_attempts})...")
                    continue

                return False

            except (StaleElementReferenceException, Exception) as e:
                if attempt < max_attempts - 1:
                    print(f"⚠️  Error expanding section (attempt {attempt + 1}/{max_attempts}): {str(e)[:80]}")
                    continue
                else:
                    print(f"❌ Failed to expand Government Response section after {max_attempts} attempts")
                    return False

        return False

    def collapse_govt_response_options(self):
        """Collapse Government Response options section with enhanced fallback logic"""
        import time
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

        # Wait for page to be ready
        self._wait_for_page_load_complete()

        self.scroll_to_element(GovtResponseLocators.EXPAND_COLLAPSE)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                parent_element = self.find_element(GovtResponseLocators.EXPAND_COLLAPSE, use_healing=False)
                if not parent_element:
                    print("⚠️ Government Response section element not found")
                    return False

                # Check if the section is expanded before trying to collapse
                aria_expanded = parent_element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Government Response Options already collapsed")
                    return True

                # APPROACH 1: Try hover-based collapse button (for larger sections)
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(parent_element).perform()

                    collapse_button = self.find_element(GovtResponseLocators.COLLAPSE_BUTTON, use_healing=False)
                    if collapse_button and collapse_button.is_displayed():
                        collapse_button.click()
                        print("✅ Government Response Options collapsed successfully (hover method)")
                        return True
                except Exception as hover_error:
                    print(f"⚠️ Hover method failed: {hover_error}, trying fallback...")

                # APPROACH 2: Direct click on parent element (toggle behavior)
                try:
                    parent_element.click()

                    # Verify it collapsed
                    parent_element = self.find_element(GovtResponseLocators.EXPAND_COLLAPSE, use_healing=False)
                    if parent_element:
                        aria_expanded = parent_element.get_attribute('aria-expanded')
                        if aria_expanded == 'false':
                            print("✅ Government Response Options collapsed successfully (direct click)")
                            return True
                except Exception as click_error:
                    print(f"⚠️ Direct click failed: {click_error}")

                # APPROACH 3: JavaScript click as last resort
                try:
                    self.driver.execute_script("arguments[0].click();", parent_element)
                    print("✅ Government Response Options collapsed successfully (JavaScript click)")
                    return True
                except Exception as js_error:
                    print(f"⚠️ JavaScript click failed: {js_error}")

                # If we got here, retry
                if attempt < max_retries - 1:
                    print(f"⚠️ Collapse attempt {attempt + 1} failed, retrying...")
                    continue

            except (StaleElementReferenceException, TimeoutException) as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Stale element in collapse, retrying ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    print(f"❌ Failed to collapse Government Response Options after {max_retries} attempts: {e}")
                    return False
            except Exception as e:
                print(f"❌ Error in collapse_govt_response_options: {e}")
                if attempt < max_retries - 1:
                    continue
                return False

        return False

    def select_govt_response_option(self, option_name, screenshot_prefix=None):
        """Select a government response option"""
        govt_response_options = {
            'flood_tenders': (GovtResponseLocators.FLOOD_TENDERS, "Flood Tenders", "flood_tenders"),
            'sdrf': (GovtResponseLocators.SDRF, "SDRF", "flood_tenders_sdrf"),
            'repairs': (GovtResponseLocators.REPAIRS_RESTORATION, "Repairs and Restoration", "flood_tenders_repair_restore"),
            'immediate': (GovtResponseLocators.IMMEDIATE_MEASURES, "Immediate Measures", "flood_tenders_immediate_measures"),
            'others': (GovtResponseLocators.OTHERS, "Others", "flood_tenders_other"),
            'funds': (GovtResponseLocators.FUNDS_ALLOCATED_SDRF_SEC, "Funds Allocated SDRF SEC", "funds_allocated_sdrf_sec")
        }

        if option_name not in govt_response_options:
            print(f"❌ Unknown government response option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = govt_response_options[option_name]
        screenshot_name = f"{screenshot_prefix}govt_response_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)
