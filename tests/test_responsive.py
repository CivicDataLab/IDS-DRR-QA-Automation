"""
Responsive Tests — layout checks across mobile/tablet/desktop breakpoints.

Run:
    pytest tests/test_responsive.py -v
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import Config
from locators.common_locators import HeaderLocators
from pages.common_page import CommonPage

# The open drawer's Home link isn't under <header> at all — it's rendered via
# a portal elsewhere in the DOM, confirmed live. CommonPage.is_nav_link_visible()
# depends on self-healing relaxing HeaderLocators.HOME_LINK's //header scope to
# find it, which worked locally but not reliably under CI's parallel xdist load
# (self-healing exhausted every strategy and found nothing there — not a false
# positive this time, a real timeout). Checking the real, unscoped element
# directly is both more precise and doesn't depend on healing succeeding.
_DRAWER_HOME_LINK = (By.XPATH, "//a[normalize-space()='Home']")

MOBILE = (375, 667)
TABLET = (768, 1024)
DESKTOP = (1920, 1080)
BREAKPOINTS = [("mobile", *MOBILE), ("tablet", *TABLET), ("desktop", *DESKTOP)]

# dev's Analytics nav lands on a per-state disaster-type hub (Flood/Heat cards)
# before the actual dashboard — see DisasterHubLocators in
# fix-footer-analytics-hub-locators (not yet merged as of this branch).
# Duplicated inline here rather than importing it, since that locator doesn't
# exist on this branch yet; once that PR merges this can import it instead.
_EXPLORE_LINK = (By.XPATH, "(//a[normalize-space()='Explore'] | //button[normalize-space()='Explore'])[1]")


def _goto_analytics_dashboard(driver):
    """Navigate to the Assam analytics dashboard, stepping through the
    disaster-type hub if the viewport/environment shows one."""
    driver.get(f"{Config.BASE_URL.rstrip('/')}/assam/analytics?indicator=risk-score&view=map")
    common_page = CommonPage(driver)
    if common_page.is_element_visible(_EXPLORE_LINK, "Explore (disaster hub)", timeout=3):
        common_page.click(_EXPLORE_LINK, "Explore (disaster hub)")


def _has_horizontal_overflow(driver):
    body_width = driver.execute_script("return document.body.scrollWidth")
    window_width = driver.execute_script("return window.innerWidth")
    return body_width > window_width, body_width, window_width


@pytest.mark.responsive
class TestResponsiveLayout:
    """No horizontal overflow at any breakpoint, on Home and Analytics."""

    @pytest.mark.parametrize("label,width,height", BREAKPOINTS)
    def test_home_page_no_horizontal_overflow(self, driver, label, width, height):
        """Home page fits its viewport width at each breakpoint"""
        driver.set_window_size(width, height)
        driver.get(Config.BASE_URL)
        overflowing, body_w, window_w = _has_horizontal_overflow(driver)
        assert not overflowing, f"{label} ({width}x{height}): body scrollWidth {body_w} > viewport {window_w}"

    @pytest.mark.parametrize("label,width,height", BREAKPOINTS)
    def test_analytics_dashboard_no_horizontal_overflow(self, driver, label, width, height):
        """Analytics dashboard fits its viewport width at each breakpoint"""
        driver.set_window_size(width, height)
        _goto_analytics_dashboard(driver)
        overflowing, body_w, window_w = _has_horizontal_overflow(driver)
        assert not overflowing, f"{label} ({width}x{height}): body scrollWidth {body_w} > viewport {window_w}"


def _home_link_directly_visible(common_page):
    """Whether the Home nav link is visible via its exact locator alone.

    use_healing=False deliberately: self-healing exists to find *something*
    when the exact locator fails, which is exactly wrong for a "should not be
    findable yet" assertion — confirmed live, a healed-relaxed match
    (//header//a, any anchor in the header) found the logo link and reported
    "visible" even when the actual Home nav link was genuinely collapsed
    behind the hamburger menu.
    """
    return common_page.find_visible_element(HeaderLocators.HOME_LINK, timeout=3, use_healing=False) is not None


@pytest.mark.responsive
class TestResponsiveNavigation:
    """Nav is reachable at every breakpoint, even where it's collapsed behind a toggle.

    The real breakpoint was confirmed live (binary-searched 900-1280px): nav
    collapses behind a hamburger below 1024px width and is directly visible at
    1024px and above. That means a 768-wide "tablet" viewport gets the *same*
    collapsed nav as mobile, not the desktop-style nav — verified directly
    rather than assumed, after an earlier version of this test wrongly grouped
    tablet with desktop and only passed because self-healing masked the
    mismatch the same way described above.
    """

    @pytest.mark.parametrize("label,width,height", [("mobile", *MOBILE), ("tablet", *TABLET)])
    def test_nav_collapsed_behind_menu_toggle(self, driver, label, width, height):
        """Below the 1024px breakpoint: nav links aren't directly visible, but the hamburger toggle reveals them"""
        driver.set_window_size(width, height)
        driver.get(Config.BASE_URL)
        common_page = CommonPage(driver)

        assert not _home_link_directly_visible(common_page), (
            f"{label} ({width}x{height}): expected Home link to be collapsed behind the mobile menu, "
            "but it's directly visible — the breakpoint or menu markup may have changed"
        )
        assert common_page.is_mobile_menu_button_visible(), f"{label} ({width}x{height}): menu toggle not visible"
        assert common_page.open_mobile_menu(), f"{label} ({width}x{height}): failed to open the mobile menu"

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(_DRAWER_HOME_LINK))
        except Exception:
            pass
        home_links = driver.find_elements(*_DRAWER_HOME_LINK)
        assert any(el.is_displayed() for el in home_links), (
            f"{label} ({width}x{height}): Home link not visible anywhere after opening the mobile menu"
        )

    def test_nav_directly_visible_on_desktop(self, driver):
        """At 1024px and above: nav links are directly visible, no menu toggle needed"""
        driver.set_window_size(*DESKTOP)
        driver.get(Config.BASE_URL)
        common_page = CommonPage(driver)
        assert _home_link_directly_visible(common_page), "Desktop: Home link not directly visible"
