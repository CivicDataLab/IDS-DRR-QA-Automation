"""
Wait Helper Utilities

This module provides reusable explicit wait functions to replace time.sleep() calls
throughout the test automation codebase. These functions follow Selenium best practices
for waiting on dynamic web content.
"""

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def wait_for_dropdown_options(driver, locator, timeout=15, min_options=1):
    """
    Wait for dropdown to populate with actual options (not just placeholder).

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, selector)
        timeout: Maximum wait time in seconds (default: 15)
        min_options: Minimum number of non-placeholder options required (default: 1)

    Returns:
        bool: True if dropdown populated, False if timeout

    Example:
        wait_for_dropdown_options(driver, (By.ID, "district-dropdown"))
    """
    def dropdown_has_options(driver):
        try:
            element = driver.find_element(*locator)
            select = Select(element)
            # Filter out placeholder options (ones that start with "Select")
            actual_options = [opt for opt in select.options if opt.text.strip()
                            and not opt.text.strip().lower().startswith('select')]
            return len(actual_options) >= min_options
        except:
            return False

    try:
        WebDriverWait(driver, timeout).until(dropdown_has_options)
        return True
    except TimeoutException:
        return False


def wait_for_dropdown_option_text(driver, locator, text, timeout=20):
    """
    Wait until the dropdown contains an option matching `text` (exact, or
    case-insensitive partial — mirroring select_dropdown_by_text).

    Guards against a stale dropdown: when the browser is reused across states
    (--dist load), selecting a new state triggers an async reload of dependent
    dropdowns. Until that completes, the dropdown still holds the PREVIOUS
    state's options. Waiting for the specific target option ensures the new
    state's data has loaded before we attempt selection.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, selector)
        text: Visible option text to wait for
        timeout: Maximum wait time in seconds (default: 20)

    Returns:
        bool: True if the option appeared, False if timeout
    """
    target = text.strip().lower()

    def option_present(driver):
        try:
            select = Select(driver.find_element(*locator))
            for opt in select.options:
                opt_text = opt.text.strip().lower()
                if opt_text == target or target in opt_text:
                    return True
            return False
        except Exception:
            return False

    try:
        WebDriverWait(driver, timeout).until(option_present)
        return True
    except TimeoutException:
        return False


def wait_for_element_clickable(driver, locator, timeout=10):
    """
    Wait for element to be clickable (visible and enabled).

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, selector)
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        WebElement if successful, None if timeout

    Example:
        element = wait_for_element_clickable(driver, (By.ID, "submit-button"))
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    except TimeoutException:
        return None


def wait_for_document_ready(driver, timeout=10):
    """
    Wait for document.readyState to be 'complete'.

    Args:
        driver: WebDriver instance
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        bool: True if document ready, False if timeout

    Example:
        wait_for_document_ready(driver)
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except TimeoutException:
        return False


def wait_for_loading_to_disappear(driver, timeout=10):
    """
    Wait for loading spinners/indicators to disappear.

    Args:
        driver: WebDriver instance
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        bool: True if loading disappeared or not found, False if timeout with loading still visible

    Example:
        wait_for_loading_to_disappear(driver)
    """
    loading_selectors = [
        (By.CSS_SELECTOR, ".loading"),
        (By.CSS_SELECTOR, ".spinner"),
        (By.CSS_SELECTOR, "[class*='loading']"),
        (By.CSS_SELECTOR, "[class*='spinner']"),
        (By.XPATH, "//*[contains(@class, 'spinner')]"),
        (By.XPATH, "//div[contains(@class, 'loader')]")
    ]

    for selector in loading_selectors:
        try:
            WebDriverWait(driver, timeout).until_not(
                EC.presence_of_element_located(selector)
            )
        except TimeoutException:
            # Loading indicator not found or already gone
            pass

    return True


def wait_for_element_stable_position(driver, element, timeout=2, check_interval=0.1):
    """
    Wait for element position to stabilize (useful after scrolling or animations).

    Args:
        driver: WebDriver instance
        element: WebElement to check
        timeout: Maximum wait time in seconds (default: 2)
        check_interval: Time between position checks in seconds (default: 0.1)

    Returns:
        bool: True if position stabilized, False if timeout

    Example:
        wait_for_element_stable_position(driver, my_element)
    """
    import time
    try:
        def position_stable():
            initial_pos = element.location
            time.sleep(check_interval)
            return element.location == initial_pos

        WebDriverWait(driver, timeout).until(lambda d: position_stable())
        return True
    except TimeoutException:
        return False


def wait_for_any_condition(driver, conditions, timeout=10):
    """
    Wait for any one of multiple conditions to be true.

    Args:
        driver: WebDriver instance
        conditions: List of callables that take driver as argument and return a value or False
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        The return value of the first condition that becomes true, or False if timeout

    Example:
        result = wait_for_any_condition(
            driver,
            [
                lambda d: d.find_elements(By.CSS_SELECTOR, ".error") and 'error',
                lambda d: d.find_elements(By.CSS_SELECTOR, "canvas") and 'success'
            ],
            timeout=10
        )
    """
    def check_any_condition(driver):
        for condition in conditions:
            try:
                result = condition(driver)
                if result:
                    return result
            except:
                pass
        return False

    try:
        return WebDriverWait(driver, timeout).until(check_any_condition)
    except TimeoutException:
        return False


def wait_for_url_change(driver, initial_url, timeout=10):
    """
    Wait for URL to change from initial value.

    Args:
        driver: WebDriver instance
        initial_url: The URL to wait to change from
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        bool: True if URL changed, False if timeout

    Example:
        initial = driver.current_url
        # Click navigation link
        wait_for_url_change(driver, initial)
    """
    try:
        WebDriverWait(driver, timeout).until(EC.url_changes(initial_url))
        return True
    except TimeoutException:
        return False


def wait_for_url_contains(driver, url_fragment, timeout=10):
    """
    Wait for URL to contain a specific fragment.

    Args:
        driver: WebDriver instance
        url_fragment: String that should appear in URL
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        bool: True if URL contains fragment, False if timeout

    Example:
        wait_for_url_contains(driver, "/dashboard")
    """
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(url_fragment))
        return True
    except TimeoutException:
        return False


def wait_for_element_visibility(driver, locator, timeout=10):
    """
    Wait for element to be visible.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, selector)
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        WebElement if successful, None if timeout

    Example:
        element = wait_for_element_visibility(driver, (By.ID, "results-table"))
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    except TimeoutException:
        return None


def wait_for_element_invisibility(driver, locator, timeout=10):
    """
    Wait for element to become invisible or removed from DOM.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, selector)
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        bool: True if element invisible, False if timeout

    Example:
        wait_for_element_invisibility(driver, (By.ID, "loading-overlay"))
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False


def wait_for_element_attribute_value(driver, locator, attribute, expected_value, timeout=5):
    """
    Wait for element's attribute to reach expected value.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By, selector)
        attribute: Attribute name to check
        expected_value: Expected value of the attribute
        timeout: Maximum wait time in seconds (default: 5)

    Returns:
        bool: True if attribute matches, False if timeout

    Example:
        wait_for_element_attribute_value(driver, (By.ID, "section"), "aria-expanded", "true")
    """
    def check_attribute(driver):
        try:
            element = driver.find_element(*locator)
            return element.get_attribute(attribute) == expected_value
        except:
            return False

    try:
        WebDriverWait(driver, timeout).until(check_attribute)
        return True
    except TimeoutException:
        return False


def wait_for_animation_complete(driver, element, timeout=2):
    """
    Wait for CSS animations/transitions to complete on an element.

    Args:
        driver: WebDriver instance
        element: WebElement to check
        timeout: Maximum wait time in seconds (default: 2)

    Returns:
        bool: True if animation complete, False if timeout

    Example:
        wait_for_animation_complete(driver, my_element)
    """
    import time

    def animation_finished():
        try:
            # Check if element has any active animations or transitions
            script = """
            var elem = arguments[0];
            var animations = elem.getAnimations ? elem.getAnimations() : [];
            var computedStyle = window.getComputedStyle(elem);
            var hasTransition = computedStyle.transition !== 'all 0s ease 0s';
            return animations.length === 0 && !hasTransition;
            """
            result = driver.execute_script(script, element)
            return result
        except:
            # If getAnimations not supported, wait a minimal time
            time.sleep(0.1)
            return True

    try:
        WebDriverWait(driver, timeout).until(lambda d: animation_finished())
        return True
    except TimeoutException:
        return False


def wait_for_stale_element(driver, element, timeout=5):
    """
    Wait for element to become stale (useful after DOM updates).

    Args:
        driver: WebDriver instance
        element: WebElement that should become stale
        timeout: Maximum wait time in seconds (default: 5)

    Returns:
        bool: True if element became stale, False if timeout

    Example:
        old_element = driver.find_element(By.ID, "content")
        # Trigger page update
        wait_for_stale_element(driver, old_element)
    """
    try:
        WebDriverWait(driver, timeout).until(EC.staleness_of(element))
        return True
    except TimeoutException:
        return False
