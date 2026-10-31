from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config
from locators.module_analytics_locators import ModuleAnalyticsLocators, StateHubLocators
from pages.base_page import BasePage


def _site_url(path):
    return f"{Config.BASE_URL.rstrip('/')}/{path.lstrip('/')}"


class ModuleAnalyticsPage(BasePage):
    """Page Object for /<state>/<module>/analytics (module-aware analytics dashboard)."""

    def open(self, state_slug, module_slug, indicator, view="map"):
        """Load a module dashboard and wait until its indicator heading has rendered."""
        self.driver.get(
            _site_url(f"{state_slug}/{module_slug}/analytics?indicator={indicator}&view={view}")
        )
        WebDriverWait(self.driver, Config.LONG_TIMEOUT).until(
            EC.visibility_of_element_located(ModuleAnalyticsLocators.INDICATOR_TITLE)
        )

    def sidebar_state_slugs(self):
        """Slugs of the states offered in the sidebar State picker, in order."""
        WebDriverWait(self.driver, Config.LONG_TIMEOUT).until(
            EC.presence_of_element_located(ModuleAnalyticsLocators.STATE_SELECT)
        )
        return [
            option.get_attribute("value")
            for option in self.driver.find_elements(*ModuleAnalyticsLocators.STATE_OPTIONS)
        ]

    def indicator_heading(self):
        """(visible text, title attribute) of the indicator heading."""
        heading = self.driver.find_element(*ModuleAnalyticsLocators.INDICATOR_TITLE)
        return heading.text.strip(), heading.get_attribute("title")


class StateHubPage(BasePage):
    """Page Object for the per-state hub (/<state>) listing that state's disaster modules."""

    def open(self, state_slug):
        """Load the hub and wait for its module cards (Explore links) to render."""
        self.driver.get(_site_url(state_slug))
        WebDriverWait(self.driver, Config.LONG_TIMEOUT).until(
            EC.visibility_of_element_located(StateHubLocators.EXPLORE_LINKS)
        )

    def main_text(self):
        """Visible text of the page body (the hub's cards and notes)."""
        return self.driver.find_element(*StateHubLocators.MAIN).text
