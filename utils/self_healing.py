"""
Self-healing locator utility with intelligent fallback strategies

This module provides automatic element location with multiple fallback strategies
to reduce test failures due to minor UI changes.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class SelfHealingLocator:
    """
    Self-healing locator that tries multiple strategies to find elements
    """

    # Directory to store learned locators
    LEARNED_LOCATORS_FILE = "config/learned_locators.json"

    # Session-level cache — loaded once, shared across all instances
    _locators_cache = None

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.healing_log = []
        self._load_learned_locators()

    def _load_learned_locators(self):
        """Load previously learned locators from file (cached per session)"""
        if os.environ.get("DISABLE_LEARNED_LOCATORS", "").lower() == "true":
            self.learned_locators = {}
            logger.info("Learned locators disabled via --no-learned-locators")
            return

        if SelfHealingLocator._locators_cache is None:
            cache = {}
            if os.path.exists(self.LEARNED_LOCATORS_FILE):
                try:
                    with open(self.LEARNED_LOCATORS_FILE, 'r') as f:
                        cache = json.load(f)
                    logger.info(f"Loaded {len(cache)} learned locators from disk")
                except Exception as e:
                    logger.warning(f"Could not load learned locators: {e}")
            SelfHealingLocator._locators_cache = cache

        self.learned_locators = SelfHealingLocator._locators_cache

    def _save_learned_locator(self, original_locator, successful_locator, element_text=""):
        """Save a successful locator for future use"""
        locator_key = f"{original_locator[0]}:{original_locator[1]}"

        self.learned_locators[locator_key] = {
            "successful_locator": successful_locator,
            "element_text": element_text,
            "timestamp": datetime.now().isoformat(),
            "use_count": self.learned_locators.get(locator_key, {}).get("use_count", 0) + 1
        }

        # Keep class-level cache in sync
        SelfHealingLocator._locators_cache = self.learned_locators

        # Save to file
        try:
            os.makedirs(os.path.dirname(self.LEARNED_LOCATORS_FILE), exist_ok=True)
            with open(self.LEARNED_LOCATORS_FILE, 'w') as f:
                json.dump(self.learned_locators, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save learned locators: {e}")

    def find_element_with_healing(self, locator, element_name="Element", timeout=None):
        """
        Find element using self-healing strategies

        Strategies applied in order:
        1. Try original locator
        2. Try learned locator (if exists)
        3. Try relaxed XPath (if XPath)
        4. Try by text content
        5. Try by partial text
        6. Try by nearby elements
        7. Try by CSS alternatives

        Args:
            locator: Tuple of (By, selector)
            element_name: Name for logging
            timeout: Custom timeout

        Returns:
            WebElement or None
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)

        # Strategy 1: Try original locator
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            logger.info(f"✅ Found {element_name} using original locator")
            return element
        except TimeoutException:
            logger.warning(f"⚠️ Original locator failed for {element_name}, trying healing strategies...")

        # Strategy 2: Try learned locator
        locator_key = f"{locator[0]}:{locator[1]}"
        if locator_key in self.learned_locators:
            learned = self.learned_locators[locator_key]
            learned_locator = tuple(learned["successful_locator"])
            try:
                element = wait.until(EC.presence_of_element_located(learned_locator))
                logger.info(f"🔧 Found {element_name} using learned locator")
                self._log_healing(element_name, "learned_locator", locator, learned_locator)
                return element
            except TimeoutException:
                pass

        # Strategy 3: Try relaxed XPath (if original is XPath)
        if locator[0] == By.XPATH:
            relaxed_locators = self._generate_relaxed_xpaths(locator[1])
            for relaxed_locator in relaxed_locators:
                try:
                    element = wait.until(EC.presence_of_element_located((By.XPATH, relaxed_locator)))
                    logger.info(f"🔧 Found {element_name} using relaxed XPath")
                    self._log_healing(element_name, "relaxed_xpath", locator, (By.XPATH, relaxed_locator))
                    self._save_learned_locator(locator, [By.XPATH, relaxed_locator], element.text[:50])
                    return element
                except TimeoutException:
                    continue

        # Strategy 4: Try CSS alternatives (if original is CSS)
        if locator[0] == By.CSS_SELECTOR:
            css_alternatives = self._generate_css_alternatives(locator[1])
            for css_alt in css_alternatives:
                try:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_alt)))
                    logger.info(f"🔧 Found {element_name} using CSS alternative")
                    self._log_healing(element_name, "css_alternative", locator, (By.CSS_SELECTOR, css_alt))
                    self._save_learned_locator(locator, [By.CSS_SELECTOR, css_alt], element.text[:50])
                    return element
                except TimeoutException:
                    continue

        # Strategy 5: Try finding by tag name patterns
        tag_locators = self._generate_tag_based_locators(locator)
        for tag_locator in tag_locators:
            try:
                element = wait.until(EC.presence_of_element_located(tag_locator))
                logger.info(f"🔧 Found {element_name} using tag-based locator")
                self._log_healing(element_name, "tag_based", locator, tag_locator)
                self._save_learned_locator(locator, list(tag_locator), element.text[:50])
                return element
            except TimeoutException:
                continue

        logger.error(f"❌ All healing strategies failed for {element_name}")
        return None

    def _generate_relaxed_xpaths(self, xpath):
        """
        Generate relaxed versions of XPath

        Examples:
        - /html/body/div[1]/button -> //button
        - //div[@class='exact-class'] -> //div[contains(@class, 'exact-class')]
        """
        relaxed = []

        # Extract tag name
        if '/' in xpath:
            parts = xpath.split('/')
            # Get last meaningful tag
            for part in reversed(parts):
                if part and '[' not in part and '@' not in part:
                    relaxed.append(f"//{part}")
                    break

        # Convert exact attribute matches to contains
        if '@' in xpath and '=' in xpath:
            # Convert @attr='value' to contains(@attr, 'value')
            import re
            contains_xpath = re.sub(
                r"@(\w+)='([^']+)'",
                r"contains(@\1, '\2')",
                xpath
            )
            if contains_xpath != xpath:
                relaxed.append(contains_xpath)

        # Remove position predicates [1], [2], etc.
        if '[' in xpath:
            import re
            no_position = re.sub(r'\[\d+\]', '', xpath)
            if no_position != xpath:
                relaxed.append(no_position)

        # Try making absolute paths relative
        if xpath.startswith('/html'):
            relative = '//' + '/'.join(xpath.split('/')[3:])
            relaxed.append(relative)

        return relaxed

    def _generate_css_alternatives(self, css_selector):
        """Generate alternative CSS selectors"""
        alternatives = []

        # Remove :nth-child selectors
        if ':nth-child' in css_selector:
            import re
            no_nth = re.sub(r':nth-child\(\d+\)', '', css_selector)
            alternatives.append(no_nth)

        # Convert direct child to descendant
        if '>' in css_selector:
            descendant = css_selector.replace('>', ' ')
            alternatives.append(descendant)

        # Try more specific to less specific
        if ' ' in css_selector:
            parts = css_selector.split()
            # Try last two parts
            if len(parts) >= 2:
                alternatives.append(' '.join(parts[-2:]))
            # Try last part only
            alternatives.append(parts[-1])

        return alternatives

    def _generate_tag_based_locators(self, original_locator):
        """Generate locators based on common tag patterns"""
        locators = []

        # Common button patterns
        if 'button' in str(original_locator[1]).lower():
            locators.extend([
                (By.TAG_NAME, 'button'),
                (By.CSS_SELECTOR, 'button[type="button"]'),
                (By.CSS_SELECTOR, 'button[type="submit"]'),
            ])

        # Common input patterns
        if 'input' in str(original_locator[1]).lower():
            locators.extend([
                (By.TAG_NAME, 'input'),
                (By.CSS_SELECTOR, 'input[type="text"]'),
            ])

        # Common link patterns
        if 'a' in str(original_locator[1]).lower() or 'link' in str(original_locator[1]).lower():
            locators.extend([
                (By.TAG_NAME, 'a'),
                (By.CSS_SELECTOR, 'a[href]'),
            ])

        return locators

    def _log_healing(self, element_name, strategy, original_locator, successful_locator):
        """Log healing attempt for reporting"""
        self.healing_log.append({
            "element_name": element_name,
            "strategy": strategy,
            "original_locator": f"{original_locator[0]}:{original_locator[1]}",
            "successful_locator": f"{successful_locator[0]}:{successful_locator[1]}",
            "timestamp": datetime.now().isoformat()
        })

    def get_healing_report(self):
        """Get report of all healing activities"""
        return self.healing_log

    def clear_healing_log(self):
        """Clear the healing log"""
        self.healing_log = []


class ElementFinder:
    """
    Enhanced element finder with retry and multiple location strategies
    """

    def __init__(self, driver, timeout=10, healer=None):
        self.driver = driver
        self.timeout = timeout
        # Reuse an existing healer if provided to avoid redundant file I/O
        self.healer = healer if healer is not None else SelfHealingLocator(driver, timeout)

    def find_with_retry(self, locator, element_name="Element", max_retries=3, retry_delay=1):
        """
        Find element with retry mechanism

        Args:
            locator: Tuple of (By, selector)
            element_name: Name for logging
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds

        Returns:
            WebElement or None
        """
        import time

        for attempt in range(max_retries):
            element = self.healer.find_element_with_healing(locator, element_name)
            if element:
                return element

            if attempt < max_retries - 1:
                logger.warning(f"Retry {attempt + 1}/{max_retries} for {element_name}")
                time.sleep(retry_delay)

        return None

    def find_clickable_with_healing(self, locator, element_name="Element"):
        """Find element and ensure it's clickable"""
        element = self.healer.find_element_with_healing(locator, element_name)
        if element:
            try:
                wait = WebDriverWait(self.driver, self.timeout)
                return wait.until(EC.element_to_be_clickable(locator))
            except TimeoutException:
                # If original locator fails, try getting parent or scrolling into view
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    import time
                    time.sleep(0.5)
                    return element
                except:
                    return element
        return None

    def find_visible_with_healing(self, locator, element_name="Element"):
        """Find element and ensure it's visible"""
        element = self.healer.find_element_with_healing(locator, element_name)
        if element:
            try:
                wait = WebDriverWait(self.driver, self.timeout)
                return wait.until(EC.visibility_of_element_located(locator))
            except TimeoutException:
                # Check if element is actually visible
                if element.is_displayed():
                    return element
        return None
