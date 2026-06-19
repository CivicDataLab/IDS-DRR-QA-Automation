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
