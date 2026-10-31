from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config
from pages.base_page import BasePage
from locators.home_locators import HomePageLocators


class HomePage(BasePage):
    """Page Object for the Home / Landing page"""

    def is_state_links_section_visible(self):
        """Check the analytics quick-links section is rendered"""
        return self.is_element_visible(HomePageLocators.STATE_LINKS_SECTION, "State links section")

    def are_state_links_visible(self):
        """Check at least one state analytics link is visible inside the carousel"""
        element = self.find_visible_element(HomePageLocators.FIRST_ANALYTICS_LINK, timeout=10)
        if element:
            print("✅ State analytics links are visible")
            return True
        print("❌ No state analytics links found")
        return False

    def click_first_state_link(self):
        """Click the first state link in the quick-links carousel"""
        return self.click(HomePageLocators.FIRST_ANALYTICS_LINK, "First state analytics link")

    def click_carousel_next(self):
        """Advance the state-links carousel one step"""
        return self.click(HomePageLocators.CAROUSEL_NEXT, "Carousel next")

    def click_carousel_prev(self):
        """Go back one step in the state-links carousel"""
        return self.click(HomePageLocators.CAROUSEL_PREV, "Carousel previous")

    def is_dataset_catalog_section_visible(self):
        """Check the dataset catalog section is visible"""
        return self.is_element_visible(HomePageLocators.DATASET_CATALOG_SECTION, "Dataset catalog section", timeout=5)

    def click_datasets_link(self):
        """Click a datasets link on the home page"""
        return self.click(HomePageLocators.DATASETS_LINK_HOME, "Datasets link (home)")

    def quick_links_geometry(self):
        """Horizontal extents (px, viewport coordinates) of the quick-links carousel parts.

        Returns {"prev": (left, right), "next": (left, right), "viewport": (left, right),
        "first_slide_left": x}. Waits for the carousel and both arrows to be rendered.
        """
        wait = WebDriverWait(self.driver, Config.LONG_TIMEOUT)
        prev = wait.until(EC.visibility_of_element_located(HomePageLocators.QUICK_LINKS_PREV))
        nxt = wait.until(EC.visibility_of_element_located(HomePageLocators.QUICK_LINKS_NEXT))
        viewport = wait.until(EC.visibility_of_element_located(HomePageLocators.QUICK_LINKS_VIEWPORT))
        first_slide = self.driver.find_elements(*HomePageLocators.QUICK_LINKS_SLIDES)[0]

        def extent(element):
            rect = self.driver.execute_script(
                "var r = arguments[0].getBoundingClientRect(); return [r.left, r.right];", element
            )
            return tuple(rect)

        return {
            "prev": extent(prev),
            "next": extent(nxt),
            "viewport": extent(viewport),
            "first_slide_left": extent(first_slide)[0],
        }

    def quick_links_slide_count(self):
        """Number of state cards in the quick-links carousel."""
        return len(self.driver.find_elements(*HomePageLocators.QUICK_LINKS_SLIDES))

    def quick_links_next_enabled(self):
        """Whether the carousel's Next arrow is enabled (it uses aria-disabled, not disabled)."""
        nxt = self.driver.find_element(*HomePageLocators.QUICK_LINKS_NEXT)
        return nxt.get_attribute("aria-disabled") != "true"

    def click_quick_links_next(self):
        """Click the carousel's Next arrow and wait until the track has moved."""
        before = self.quick_links_geometry()["first_slide_left"]
        self.driver.find_element(*HomePageLocators.QUICK_LINKS_NEXT).click()
        try:
            WebDriverWait(self.driver, Config.SHORT_TIMEOUT).until(
                lambda _d: self.quick_links_geometry()["first_slide_left"] != before
            )
        except Exception:
            return False
        return True
