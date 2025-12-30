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
        # Initialize self-healing capabilities
        self.healer = SelfHealingLocator(driver, Config.DEFAULT_TIMEOUT)
        self.element_finder = ElementFinder(driver, Config.DEFAULT_TIMEOUT)

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
        Click on an element with wait and error handling

        Args:
            locator: Tuple of (By, selector)
            element_name: Name for logging purposes

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.find_clickable_element(locator)
            if element:
                element.click()
                print(f"✅ {element_name} clicked successfully")
                return True
            else:
                print(f"❌ {element_name} not found")
                return False
        except Exception as e:
            print(f"❌ Error clicking {element_name}: {e}")
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
            if element and element.is_displayed():
                print(f"✅ {element_name} is visible")
                return True
            else:
                print(f"❌ {element_name} is not visible")
                return False
        except Exception as e:
            print(f"❌ {element_name} not found: {e}")
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
        Select dropdown option by visible text

        Args:
            locator: Tuple of (By, selector)
            text: Visible text to select
            element_name: Name for logging purposes

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from selenium.webdriver.support.ui import Select
            element = self.find_element(locator)
            if element:
                select = Select(element)
                select.select_by_visible_text(text)
                print(f"✅ Selected '{text}' from {element_name}")
                return True
            else:
                print(f"❌ {element_name} not found")
                return False
        except Exception as e:
            print(f"❌ Error selecting from {element_name}: {e}")
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

            element.click()
            print(f"✅ {option_name} clicked")

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
