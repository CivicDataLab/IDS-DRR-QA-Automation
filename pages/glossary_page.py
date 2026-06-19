from pages.base_page import BasePage
from locators.glossary_locators import GlossaryLocators
from config.config import Config


class GlossaryPage(BasePage):
    """Page Object for the Glossary page"""

    def navigate_to(self):
        """Navigate to the glossary page.

        Tries clicking any glossary link on the current page first; falls back
        to direct URL navigation.
        """
        from selenium.webdriver.common.by import By

        links = self.driver.find_elements(By.XPATH, "//a[contains(@href,'glossary')]")
        if links:
            try:
                links[0].click()
                return "glossary" in self.driver.current_url.lower()
            except Exception:
                pass

        self.driver.get(Config.BASE_URL.rstrip('/') + "/glossary")
        return "glossary" in self.driver.current_url.lower()

    def is_search_input_visible(self):
        """Check the glossary search input is visible"""
        return self.is_element_visible(GlossaryLocators.SEARCH_INPUT, "Glossary search input")

    def search_term(self, query):
        """Type a search query into the glossary search box"""
        if not self.send_keys(GlossaryLocators.SEARCH_INPUT, query, "Glossary search input"):
            return False
        print(f"✅ Searched glossary for '{query}'")
        return True

    def clear_search(self):
        """Clear the glossary search input and trigger React's onChange to reset the filter.

        element.clear() alone doesn't fire React's synthetic onChange. We use the native
        value setter via JS + an input event — the same mechanism Playwright's fill('') uses.
        """
        try:
            element = self.find_element(GlossaryLocators.SEARCH_INPUT)
            if element:
                self.driver.execute_script(
                    """
                    var setter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value').set;
                    setter.call(arguments[0], '');
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    """,
                    element
                )
                print("✅ Glossary search cleared")
                return True
        except Exception as e:
            print(f"❌ Failed to clear glossary search: {e}")
        return False

    def are_results_visible(self):
        """Check at least one letter section or term is visible after a search"""
        element = self.find_visible_element(GlossaryLocators.FIRST_TERM_TRIGGER, timeout=5)
        if element:
            print("✅ Glossary term results visible")
            return True
        print("❌ No glossary term results visible")
        return False

    def get_term_group_count(self):
        """Return the number of visible letter-group sections"""
        from selenium.webdriver.common.by import By
        try:
            sections = self.driver.find_elements(*GlossaryLocators.LETTER_SECTIONS)
            visible = [s for s in sections if s.is_displayed()]
            return len(visible)
        except Exception:
            return 0

    def click_first_term(self):
        """Click the first accordion term to expand its definition"""
        return self.click(GlossaryLocators.FIRST_TERM_TRIGGER, "First glossary term")

    def is_content_loaded(self):
        """Check that glossary content (at least one term trigger) is present"""
        element = self.find_element(GlossaryLocators.FIRST_TERM_TRIGGER, timeout=10)
        return element is not None
