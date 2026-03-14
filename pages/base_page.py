import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config
from utils.self_healing import SelfHealingLocator, ElementFinder
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page class with common WebDriver operations and self-healing capabilities"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.DEFAULT_TIMEOUT)
        self.short_wait = WebDriverWait(driver, Config.SHORT_TIMEOUT)
        # Initialize self-healing capabilities (share one healer to avoid duplicate file I/O)
        self.healer = SelfHealingLocator(driver, Config.DEFAULT_TIMEOUT)
        self.element_finder = ElementFinder(driver, Config.DEFAULT_TIMEOUT, healer=self.healer)

    def find_element(self, locator, timeout=None, use_healing=True):
        """
        Find element with explicit wait and optional self-healing

        Args:
            locator: Tuple of (By, selector)
            timeout: Optional custom timeout
            use_healing: Whether to use self-healing if element not found

        Returns:
            WebElement or None
        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            if use_healing:
                logger.info(f"Standard find failed, attempting self-healing for: {locator}")
                return self.healer.find_element_with_healing(locator, timeout=timeout)
            else:
                print(f"Element not found within timeout: {locator}")
                return None

    def find_visible_element(self, locator, timeout=None, use_healing=True):
        """
        Find visible element with explicit wait and optional self-healing

        Args:
            locator: Tuple of (By, selector)
            timeout: Optional custom timeout
            use_healing: Whether to use self-healing if element not found

        Returns:
            WebElement or None
        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            if use_healing:
                logger.info(f"Standard visible element find failed, attempting self-healing for: {locator}")
                return self.element_finder.find_visible_with_healing(locator)
            else:
                print(f"Visible element not found within timeout: {locator}")
                return None

    def find_clickable_element(self, locator, timeout=None, use_healing=True):
        """
        Find clickable element with explicit wait and optional self-healing

        Args:
            locator: Tuple of (By, selector)
            timeout: Optional custom timeout
            use_healing: Whether to use self-healing if element not found

        Returns:
            WebElement or None
        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            if use_healing:
                logger.info(f"Standard clickable element find failed, attempting self-healing for: {locator}")
                return self.element_finder.find_clickable_with_healing(locator)
            else:
                print(f"Clickable element not found within timeout: {locator}")
                return None

    def click(self, locator, element_name="Element"):
        """
        Click on an element with wait, retry, and error handling

        Args:
            locator: Tuple of (By, selector)
            element_name: Name for logging purposes

        Returns:
            bool: True if successful, False otherwise
        """
        from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
        import time

        max_retries = 3
        for attempt in range(max_retries):
            try:
                element = self.find_clickable_element(locator)
                if element:
                    try:
                        element.click()
                        print(f"✅ {element_name} clicked successfully")
                        return True
                    except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                        if attempt < max_retries - 1:
                            print(f"⚠️  Click failed ({type(e).__name__}), retrying ({attempt + 1}/{max_retries})...")
                            time.sleep(0.5)
                            continue
                        else:
                            # Try JavaScript click as last resort
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                print(f"✅ {element_name} clicked successfully (JavaScript)")
                                return True
                            except:
                                print(f"❌ Error clicking {element_name}: {e}")
                                return False
                else:
                    print(f"❌ {element_name} not found")
                    return False
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Error in click attempt {attempt + 1}: {e}, retrying...")
                    time.sleep(0.5)
                    continue
                else:
                    print(f"❌ Error clicking {element_name}: {e}")
                    return False

        return False

    def send_keys(self, locator, text, element_name="Input"):
        """
        Send keys to an element with wait

        Args:
            locator: Tuple of (By, selector)
            text: Text to send
            element_name: Name for logging purposes

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.find_element(locator)
            if element:
                element.clear()
                element.send_keys(text)
                print(f"✅ Text entered in {element_name}")
                return True
            else:
                print(f"❌ {element_name} not found")
                return False
        except Exception as e:
            print(f"❌ Error sending keys to {element_name}: {e}")
            return False

    def is_element_visible(self, locator, element_name="Element", timeout=None):
        """
        Check if element is visible

        Args:
            locator: Tuple of (By, selector)
            element_name: Name for logging purposes
            timeout: Optional custom timeout

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            element = self.find_visible_element(locator, timeout)
            if element:
                # Double-check the element is actually displayed (not just present in DOM)
                if element.is_displayed():
                    print(f"✅ {element_name} is visible")
                    return True
                else:
                    print(f"❌ {element_name} is not visible (found in DOM but hidden)")
                    return False
            else:
                print(f"❌ {element_name} is not visible")
                return False
        except Exception as e:
            print(f"❌ {element_name} is not visible")
            return False

    def get_text(self, locator):
        """
        Get text from an element

        Args:
            locator: Tuple of (By, selector)

        Returns:
            str: Element text or empty string
        """
        try:
            element = self.find_visible_element(locator)
            return element.text if element else ""
        except Exception:
            return ""

    def scroll_to_element(self, locator):
        """
        Scroll to an element

        Args:
            locator: Tuple of (By, selector)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.find_element(locator)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                return True
            return False
        except Exception as e:
            print(f"❌ Error scrolling to element: {e}")
            return False

    def take_screenshot(self, filename, directory=None):
        """
        Take a screenshot

        Args:
            filename: Screenshot filename
            directory: Optional custom directory (uses config default if None)

        Returns:
            str: Path to screenshot file
        """
        try:
            screenshot_dir = directory or Config.SCREENSHOTS_DIR
            os.makedirs(screenshot_dir, exist_ok=True)

            screenshot_path = os.path.join(screenshot_dir, filename)
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
            return None

    def dismiss_alert(self):
        """
        Dismiss an alert if present

        Returns:
            bool: True if alert was dismissed, False otherwise
        """
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            print("✅ Alert dismissed")
            return True
        except Exception:
            return False

    def select_dropdown_by_text(self, locator, text, element_name="Dropdown"):
        """
        Select dropdown option by visible text with stale element retry logic

        Args:
            locator: Tuple of (By, selector)
            text: Visible text to select
            element_name: Name for logging purposes

        Returns:
            bool: True if successful, False otherwise
        """
        from selenium.webdriver.support.ui import Select
        from selenium.common.exceptions import StaleElementReferenceException
        import time

        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Re-fetch element on each retry to handle stale references
                element = self.find_element(locator)
                if not element:
                    print(f"❌ {element_name} not found")
                    return False

                # Wait for dropdown options to populate (especially for dependent dropdowns)
                from utils.wait_helpers import wait_for_dropdown_options
                wait_for_dropdown_options(self.driver, locator, timeout=5)

                # Create Select object with fresh element reference
                select = Select(element)

                # Try exact match first
                try:
                    select.select_by_visible_text(text)
                    print(f"✅ Selected '{text}' from {element_name}")
                    return True
                except NoSuchElementException:
                    # If exact match fails, try partial match
                    print(f"⚠️ Exact match failed for '{text}', trying partial match...")

                    # Re-fetch element and recreate Select for partial match attempt
                    element = self.find_element(locator)
                    if not element:
                        print(f"❌ {element_name} became stale during partial match")
                        return False

                    select = Select(element)
                    options = select.options

                    for option in options:
                        if text.lower() in option.text.lower():
                            # Re-fetch one more time before selection
                            element = self.find_element(locator)
                            if element:
                                select = Select(element)
                                select.select_by_visible_text(option.text)
                                print(f"✅ Selected '{option.text}' from {element_name} (partial match for '{text}')")
                                return True

                    # If still not found, print available options for debugging
                    available = [opt.text for opt in options if opt.text.strip()]
                    print(f"❌ Could not find '{text}' in {element_name}")
                    print(f"   Available options: {available}")
                    return False

            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"⚠️ Stale element in {element_name}, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(1)
                    continue
                else:
                    print(f"❌ {element_name} remained stale after {max_retries} attempts")
                    return False
            except Exception as e:
                print(f"❌ Error selecting from {element_name}: {e}")
                return False

        return False

    def click_and_screenshot(self, locator, element_name, screenshot_name, screenshot_dir=None):
        """
        Click an element and take a screenshot

        Args:
            locator: Tuple of (By, selector)
            element_name: Name for logging
            screenshot_name: Screenshot filename
            screenshot_dir: Optional screenshot directory

        Returns:
            bool: True if successful, False otherwise
        """
        if self.click(locator, element_name):
            self.take_screenshot(screenshot_name, screenshot_dir)
            return True
        return False

    def interact_with_option(self, locator, option_name, screenshot_prefix, screenshot_dir):
        """
        Generic method to interact with analytics options (expand/collapse/select)
        Uses JavaScript click as fallback if regular click fails

        Args:
            locator: Tuple of (By, selector)
            option_name: Name of the option for logging
            screenshot_prefix: Prefix for screenshot filename
            screenshot_dir: Directory to save screenshot

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.find_clickable_element(locator)
            if not element:
                print(f"❌ {option_name} not found")
                return False

            # Try regular click first
            try:
                element.click()
                print(f"✅ {option_name} clicked")
            except Exception as click_err:
                # Fallback to JavaScript click
                print(f"⚠️  Regular click failed for {option_name}, trying JavaScript click...")
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    print(f"✅ {option_name} clicked (JavaScript)")
                except Exception as js_err:
                    print(f"❌ Both click methods failed for {option_name}: {js_err}")
                    return False

            # Take screenshot if screenshot_prefix is provided
            if screenshot_prefix:
                screenshot_name = f"{screenshot_prefix}{self._sanitize_filename(option_name)}.png"
                self.take_screenshot(screenshot_name, screenshot_dir)

            return True

        except Exception as e:
            print(f"❌ Error with {option_name}: {e}")
            return False

    @staticmethod
    def _sanitize_filename(name):
        """Convert option name to valid filename"""
        return name.lower().replace(' ', '_').replace('/', '_')

    def get_healing_report(self):
        """
        Get self-healing report for this page

        Returns:
            list: List of healing events
        """
        return self.healer.get_healing_report()

    def clear_healing_log(self):
        """Clear the healing log"""
        self.healer.clear_healing_log()
