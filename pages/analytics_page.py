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

            # Additional wait for DOM to be stable
            time.sleep(1)
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
                    time.sleep(0.5)

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
                    time.sleep(0.5)

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
                    time.sleep(2)
                    continue
                else:
                    print(f"❌ Failed to select state {state_name} after {max_retries} attempts: {e}")
                    self._capture_failure_screenshot(f"state_selection_error_{state_name}")
                    return False
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Attempt {attempt + 1} failed: {type(e).__name__}: {e}")
                    print(f"⚠️  Retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(2)
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
                    time.sleep(1)
                    continue
                else:
                    print(f"❌ Failed after {max_retries} attempts due to stale elements")
                    return False

        return False

    def select_district(self, district_name):
        """Select district from dropdown"""
        success = self.select_dropdown_by_text(
            AnalyticsPageLocators.DISTRICT_SELECT,
            district_name,
            "District Dropdown"
        )
        if success:
            print(f"Selected district: {district_name}")
        return success

    def select_revenue_circle(self, revenue_circle_name):
        """Select revenue circle from dropdown"""
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
        """Expand Hazard options section with stale element handling"""
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

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
                    time.sleep(0.5)  # Wait for expand animation
                    return True
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element in expand_hazard_options, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(1)
                    continue
                else:
                    return False
        return False

    def collapse_hazard_options(self):
        """Collapse Hazard options section"""
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()
        time.sleep(0.5)

        # Check if section is already collapsed by looking for expanded state
        try:
            element = self.find_element(HazardLocators.EXPAND_COLLAPSE, use_healing=False)
            if element:
                # Check if the section is expanded before trying to collapse
                aria_expanded = element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Hazard Options already collapsed")
                    return True

            # If expanded or can't determine, try to collapse
            result = self.click(HazardLocators.EXPAND_COLLAPSE, "Collapse Hazard Options")
            if result:
                time.sleep(0.5)  # Wait for collapse animation
            return result
        except Exception as e:
            print(f"❌ Error in collapse_hazard_options: {e}")
            return False

    def select_indicator_by_text(self, indicator_text, section_name="Indicator"):
        """
        Dynamically select an indicator by its text label (supports any indicator)

        Args:
            indicator_text: The exact text of the indicator (e.g., "Total Monthly Rainfall")
            section_name: Section name for logging (Hazard, Exposure, etc.)

        Returns:
            bool: Success status
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time

        try:
            wait = WebDriverWait(self.driver, 10)

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
            except:
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

            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", label_element)
            time.sleep(0.3)

            # Click the label
            try:
                label_element.click()
            except:
                # JavaScript click fallback
                self.driver.execute_script("arguments[0].click();", label_element)

            print(f"✅ Selected indicator: {indicator_text}")
            time.sleep(0.5)  # Wait for UI to update
            return True

        except Exception as e:
            print(f"❌ Failed to select indicator '{indicator_text}': {e}")
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
        """Expand Exposure options section with stale element handling"""
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

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
                    time.sleep(0.5)  # Wait for expand animation
                    return True
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element in expand_exposure_options, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(1)
                    continue
                else:
                    return False
        return False

    def collapse_exposure_options(self):
        """Collapse Exposure options section"""
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()
        time.sleep(0.5)

        # Check if section is already collapsed
        try:
            element = self.find_element(ExposureLocators.EXPAND_COLLAPSE, use_healing=False)
            if element:
                aria_expanded = element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Exposure Options already collapsed")
                    return True

            result = self.click(ExposureLocators.EXPAND_COLLAPSE, "Collapse Exposure Options")
            if result:
                time.sleep(0.5)  # Wait for collapse animation
            return result
        except Exception as e:
            print(f"❌ Error in collapse_exposure_options: {e}")
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
        """Expand Vulnerability options section with stale element handling"""
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

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
                    time.sleep(0.5)  # Wait for expand animation
                    return True
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️  Stale element in expand_vulnerability_options, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(1)
                    continue
                else:
                    return False
        return False

    def collapse_vulnerability_options(self):
        """Collapse Vulnerability options section"""
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()
        time.sleep(0.5)

        # Check if section is already collapsed
        try:
            element = self.find_element(VulnerabilityLocators.EXPAND_COLLAPSE, use_healing=False)
            if element:
                aria_expanded = element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Vulnerability Options already collapsed")
                    return True

            result = self.click(VulnerabilityLocators.EXPAND_COLLAPSE, "Collapse Vulnerability Options")
            if result:
                time.sleep(0.5)  # Wait for collapse animation
            return result
        except Exception as e:
            print(f"❌ Error in collapse_vulnerability_options: {e}")
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
        """Expand Government Response options section"""
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

        # Scroll to element first
        self.scroll_to_element(GovtResponseLocators.EXPAND_COLLAPSE)

        result = self.interact_with_option(
            GovtResponseLocators.EXPAND_COLLAPSE,
            "Government Response Options",
            f"{screenshot_prefix}govt_response_show_options" if screenshot_prefix else None,
            self.screenshot_dir
        )
        if result:
            time.sleep(0.5)  # Wait for expand animation
        return result

    def collapse_govt_response_options(self):
        """Collapse Government Response options section"""
        import time

        # Wait for page to be ready
        self._wait_for_page_load_complete()

        self.scroll_to_element(GovtResponseLocators.EXPAND_COLLAPSE)
        time.sleep(0.5)

        # Check if section is already collapsed
        try:
            element = self.find_element(GovtResponseLocators.EXPAND_COLLAPSE, use_healing=False)
            if element:
                aria_expanded = element.get_attribute('aria-expanded')
                if aria_expanded == 'false':
                    print("✅ Government Response Options already collapsed")
                    return True

            result = self.click(GovtResponseLocators.EXPAND_COLLAPSE, "Collapse Government Response Options")
            if result:
                time.sleep(0.5)  # Wait for collapse animation
            return result
        except Exception as e:
            print(f"❌ Error in collapse_govt_response_options: {e}")
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
