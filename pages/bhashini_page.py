from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from locators.bhashini_locators import BhashiniLocators


class BhashiniPage(BasePage):
    """Page Object for the Bhashini translation widget in the site header.

    The component injects its script from a useEffect, so none of this exists
    in the server-rendered HTML - every check here needs a real browser.
    """

    def is_script_injected_by_id(self, timeout=15):
        """The script tag the component creates, matched on its own id"""
        return self._exists(BhashiniLocators.SCRIPT_BY_ID, timeout)

    def is_script_injected_by_src(self, timeout=15):
        """The same script tag, matched on the Bhashini plugin URL"""
        return self._exists(BhashiniLocators.SCRIPT_BY_SRC, timeout)

    def is_container_rendered(self, timeout=15):
        """The mount point TranslateDropdown renders"""
        return self._exists(BhashiniLocators.CONTAINER, timeout)

    def is_container_testid_rendered(self, timeout=15):
        """The same mount point via its data-testid"""
        return self._exists(BhashiniLocators.CONTAINER_TESTID, timeout)

    def is_widget_mounted_in_container(self, timeout=25):
        """The third-party widget, once loaded, mounts inside our container.

        Longer default timeout: this waits on translation-plugin.bhashini.co.in.
        """
        return self._exists(BhashiniLocators.WIDGET_IN_CONTAINER, timeout)

    def get_preferred_language(self):
        """localStorage.preferredLanguage, or None when nothing is selected yet"""
        return self.driver.execute_script(
            "return localStorage.getItem('preferredLanguage');"
        )

    def _exists(self, locator, timeout):
        """Presence check, not visibility - a <script> tag is never visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False
