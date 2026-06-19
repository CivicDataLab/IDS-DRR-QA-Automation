"""
State Indicator Discovery Utility
Automatically discovers available indicators for each state from the web UI
"""

import time
import yaml
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.driver_factory import DriverFactory
from config.config import Config
import os


class StateIndicatorDiscovery:
    """Discovers and validates available indicators for each state"""

    STATE_DROPDOWN_LOCATOR = (By.CSS_SELECTOR, "aside select")
    STATE_DROPDOWN_OPTIONS = (By.CSS_SELECTOR, "aside select option")

    STATE_LIST = [
        "Assam",
        "Himachal pradesh",
        "Odisha",
        "Bihar",
        "Uttar pradesh"
    ]

    # URL slugs match the <select> option values (hyphens, not underscores)
    STATE_URL_SLUGS = {
        "Assam": "assam",
        "Himachal pradesh": "himachal-pradesh",
        "Odisha": "odisha",
        "Bihar": "bihar",
        "Uttar pradesh": "uttar-pradesh",
    }

    def __init__(self, driver=None):
        """
        Initialize discovery utility

        Args:
            driver: WebDriver instance (optional, will create if not provided)
        """
        self.driver = driver
        self.should_quit = False

        if not self.driver:
            self.driver = DriverFactory.create_driver()
            self.should_quit = True

        self.wait = WebDriverWait(self.driver, 10)
        self.discovered_data = {}

        # Initialize common page for navigation
        from pages.common_page import CommonPage
        self.common_page = CommonPage(self.driver)

    def navigate_to_analytics(self):
        """Navigate to analytics page using CommonPage"""
        try:
            # First navigate to homepage to ensure we start from a known state
            self.driver.get(Config.BASE_URL)
            time.sleep(1)  # Wait for homepage to load

            # Use CommonPage navigation (handles fallback locators)
            success = self.common_page.navigate_to_analytics()

            if success:
                time.sleep(2)  # Allow analytics page to fully load
                print("✅ Navigated to analytics page using CommonPage")
                return True
            else:
                print("❌ Failed to navigate to analytics using CommonPage")
                return False

        except Exception as e:
            print(f"❌ Failed to navigate to analytics: {e}")
            return False

    def get_available_states(self):
        """
        Discover available states from the <select> dropdown

        Returns:
            list: Available state names
        """
        try:
            # Find the state select dropdown inside the aside sidebar
            select_element = self.driver.find_element(By.CSS_SELECTOR, "aside select")

            # Get all option elements
            options = select_element.find_elements(By.TAG_NAME, "option")

            states = []
            for option in options:
                state_name = option.text.strip()
                if state_name:
                    states.append(state_name)

            if states:
                print(f"✅ Discovered {len(states)} states from dropdown: {states}")
                return states
            else:
                print(f"⚠️  No states found in dropdown, using predefined list")
                return self.STATE_LIST

        except NoSuchElementException:
            print(f"⚠️  State dropdown not found, using predefined list")
            return self.STATE_LIST
        except Exception as e:
            print(f"⚠️  Error discovering states: {e}")
            return self.STATE_LIST

    def select_state(self, state_name):
        """
        Navigate directly to a state's analytics page via URL.

        Args:
            state_name: Name of the state (e.g., "Assam", "Himachal pradesh")

        Returns:
            bool: Success status
        """
        try:
            url_slug = self.STATE_URL_SLUGS.get(state_name)

            # Fallback: read slug from the live select element
            if not url_slug:
                try:
                    from selenium.webdriver.support.ui import Select
                    sel_el = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "aside select"))
                    )
                    select = Select(sel_el)
                    for opt in select.options:
                        if opt.text.strip().lower() == state_name.lower():
                            url_slug = opt.get_attribute("value")
                            break
                except Exception:
                    pass

            if not url_slug:
                print(f"❌ No URL slug found for state: {state_name}")
                return False

            target_url = f"{Config.BASE_URL}en/{url_slug}/analytics?indicator=risk-score&view=map"
            self.driver.get(target_url)
            time.sleep(3)
            print(f"✅ Navigated to state: {state_name} ({target_url})")
            return True

        except Exception as e:
            print(f"❌ Failed to navigate to state {state_name}: {e}")
            return False

    def discover_section_indicators(self, section_name, expand_locator, container_xpath):
        """
        Discover indicators for a specific section

        Args:
            section_name: Name of the section (Hazard, Exposure, etc.)
            expand_locator: Locator to expand the section
            container_xpath: XPath to the container with indicators

        Returns:
            list: List of discovered indicators with metadata
        """
        indicators = []

        try:
            # Expand the section
            expand_btn = self.wait.until(EC.element_to_be_clickable(expand_locator))

            # Scroll element into view to avoid header overlap
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", expand_btn)
            time.sleep(0.5)  # Wait for scroll animation

            # Check if already expanded by looking for aria-expanded or class
            is_expanded = expand_btn.get_attribute("aria-expanded") == "true"

            if not is_expanded:
                # Use JavaScript click as fallback if regular click is intercepted
                try:
                    expand_btn.click()
                except Exception as e:
                    print(f"   ⚠️  Regular click failed, using JavaScript click: {e}")
                    self.driver.execute_script("arguments[0].click();", expand_btn)
                time.sleep(0.5)

            # Find all indicator elements within the expanded section container.
            # New UI: indicators are <div role="button" aria-label="..."> elements.
            indicator_elements = []

            # Strategy 1: div[role=button][aria-label] inside the container (current UI)
            try:
                role_btns = self.driver.find_elements(
                    By.XPATH,
                    f"{container_xpath}//*[@role='button' and @aria-label]"
                )
                if role_btns:
                    indicator_elements = role_btns
                    print(f"   Found {len(role_btns)} indicators using role=button aria-label")
            except:
                pass

            # Strategy 2: labels with aria-label (legacy fallback)
            if not indicator_elements:
                try:
                    labels = self.driver.find_elements(
                        By.XPATH,
                        f"{container_xpath}//label[@aria-label]"
                    )
                    if labels:
                        indicator_elements = labels
                        print(f"   Found {len(labels)} indicators using aria-label labels")
                except:
                    pass

            for idx, element in enumerate(indicator_elements, 1):
                try:
                    # aria-label holds the display name directly in the new UI
                    indicator_text = element.get_attribute("aria-label") or element.text.strip()

                    if indicator_text:
                        indicator_data = {
                            "name": indicator_text,
                            "key": self._sanitize_key(indicator_text),
                            "position": idx,
                            "enabled": True,  # Assume enabled by default
                            "section": section_name
                        }
                        indicators.append(indicator_data)

                except Exception as e:
                    print(f"⚠️  Error extracting indicator at position {idx}: {e}")
                    continue

            print(f"✅ Discovered {len(indicators)} indicators in {section_name}")

        except Exception as e:
            print(f"❌ Failed to discover {section_name} indicators: {e}")
            import traceback
            traceback.print_exc()

        return indicators

    def discover_all_indicators(self, state_name):
        """
        Discover all indicators for a given state

        Args:
            state_name: Name of the state

        Returns:
            dict: Complete indicator mapping for the state
        """
        print(f"\n{'='*60}")
        print(f"Discovering indicators for: {state_name}")
        print(f"{'='*60}")

        if not self.navigate_to_analytics():
            return {}

        # Select the state
        if not self.select_state(state_name):
            print(f"⚠️  Could not select state {state_name}, using default state")

        # Wait for page to stabilize
        time.sleep(2)

        state_data = {
            "state_name": state_name,
            "state_key": self._sanitize_key(state_name),
            "discovered_at": datetime.now().isoformat(),
            "sections": {}
        }

        # Discover Hazard indicators
        from locators.analytics_locators import HazardLocators
        hazard_indicators = self.discover_section_indicators(
            "Hazard",
            HazardLocators.EXPAND_COLLAPSE,
            "//aside//*[@role='button' and @aria-label='Hazard']/following-sibling::div"
        )
        state_data["sections"]["hazard"] = {
            "name": "Hazard",
            "indicators": hazard_indicators
        }

        # Discover Exposure indicators
        from locators.analytics_locators import ExposureLocators
        exposure_indicators = self.discover_section_indicators(
            "Exposure",
            ExposureLocators.EXPAND_COLLAPSE,
            "//aside//*[@role='button' and @aria-label='Exposure']/following-sibling::div"
        )
        state_data["sections"]["exposure"] = {
            "name": "Exposure",
            "indicators": exposure_indicators
        }

        # Discover Vulnerability indicators
        from locators.analytics_locators import VulnerabilityLocators
        vulnerability_indicators = self.discover_section_indicators(
            "Vulnerability",
            VulnerabilityLocators.EXPAND_COLLAPSE,
            "//aside//*[@role='button' and @aria-label='Vulnerability']/following-sibling::div"
        )
        state_data["sections"]["vulnerability"] = {
            "name": "Vulnerability",
            "indicators": vulnerability_indicators
        }

        # Discover Government Response indicators
        from locators.analytics_locators import GovtResponseLocators
        govt_response_indicators = self.discover_section_indicators(
            "Government Response",
            GovtResponseLocators.EXPAND_COLLAPSE,
            "//aside//*[@role='button' and @aria-label='Government Response']/following-sibling::div"
        )
        state_data["sections"]["government_response"] = {
            "name": "Government Response",
            "indicators": govt_response_indicators
        }

        # Summary
        total_indicators = sum(
            len(section["indicators"])
            for section in state_data["sections"].values()
        )

        print(f"\n{'='*60}")
        print(f"Discovery Summary for {state_name}:")
        print(f"  Total Indicators: {total_indicators}")
        for section_key, section_data in state_data["sections"].items():
            print(f"  - {section_data['name']}: {len(section_data['indicators'])} indicators")
        print(f"{'='*60}\n")

        return state_data

    def discover_all_states(self, states=None):
        """
        Discover indicators for all states

        Args:
            states: List of state names (optional, will auto-discover if not provided)

        Returns:
            dict: Complete mapping of all states and their indicators
        """
        if states is None:
            states = self.get_available_states()

        print(f"\n{'='*70}")
        print(f"Starting Multi-State Indicator Discovery")
        print(f"States to discover: {', '.join(states)}")
        print(f"{'='*70}\n")

        all_states_data = {
            "discovery_timestamp": datetime.now().isoformat(),
            "total_states": len(states),
            "states": {}
        }

        for state in states:
            state_data = self.discover_all_indicators(state)
            if state_data:
                state_key = self._sanitize_key(state)
                all_states_data["states"][state_key] = state_data

        self.discovered_data = all_states_data
        return all_states_data

    def save_to_yaml(self, output_dir="config/states"):
        """
        Save discovered data to YAML files

        Args:
            output_dir: Directory to save YAML files
        """
        os.makedirs(output_dir, exist_ok=True)

        # Save individual state files
        for state_key, state_data in self.discovered_data.get("states", {}).items():
            yaml_path = os.path.join(output_dir, f"{state_key}.yaml")

            with open(yaml_path, 'w') as f:
                yaml.dump(state_data, f, default_flow_style=False, sort_keys=False)

            print(f"✅ Saved {state_data['state_name']} configuration to {yaml_path}")

        # Save master config file
        master_config_path = os.path.join(output_dir, "states_master.yaml")

        # Create a summary for master config
        master_config = {
            "discovery_timestamp": self.discovered_data.get("discovery_timestamp"),
            "total_states": self.discovered_data.get("total_states"),
            "states": {}
        }

        for state_key, state_data in self.discovered_data.get("states", {}).items():
            master_config["states"][state_key] = {
                "name": state_data["state_name"],
                "config_file": f"{state_key}.yaml",
                "total_indicators": sum(
                    len(section["indicators"])
                    for section in state_data["sections"].values()
                ),
                "sections": {
                    section_key: len(section["indicators"])
                    for section_key, section in state_data["sections"].items()
                }
            }

        with open(master_config_path, 'w') as f:
            yaml.dump(master_config, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Saved master configuration to {master_config_path}")

    @staticmethod
    def _sanitize_key(text):
        """
        Convert text to a valid key

        Args:
            text: Input text

        Returns:
            str: Sanitized key
        """
        import re
        # Convert to lowercase, replace spaces and special chars with underscores
        key = re.sub(r'[^a-z0-9]+', '_', text.lower())
        # Remove leading/trailing underscores
        key = key.strip('_')
        return key

    def cleanup(self):
        """Cleanup resources"""
        if self.should_quit and self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except Exception as e:
                print(f"⚠️  Error closing browser: {e}")


def run_discovery(states=None):
    """
    Convenience function to run discovery

    Args:
        states: List of states to discover (optional)

    Returns:
        dict: Discovery results
    """
    discovery = StateIndicatorDiscovery()

    try:
        results = discovery.discover_all_states(states)
        discovery.save_to_yaml()
        return results
    finally:
        discovery.cleanup()


if __name__ == "__main__":
    print("Starting State Indicator Discovery...")
    results = run_discovery()

    print("\n" + "="*70)
    print("Discovery Complete!")
    print("="*70)
