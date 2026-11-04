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


def _goto_analytics_dashboard(driver):
    """Navigate to the Assam analytics dashboard via the header nav, same path
    a real user takes — CommonPage.navigate_to_analytics() already steps
    through the disaster-type hub when dev shows one (see DisasterHubLocators)."""
    CommonPage(driver).navigate_to_analytics()


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


# WCAG 2.1 SC 1.4.10 (Reflow, Level AA): content must fit a 320 CSS px wide
# viewport without horizontal scrolling. 320 is below the 375px "mobile" size
# used above, so it catches fixed-width controls that 375 hides.
REFLOW_WIDTH = (320, 640)

# Both defects were measured live (dev, 2026-10-31): the search box on each page
# is wider than the viewport (datasets 376px wide, glossary 325px wide). Strict,
# so the day one is fixed this test says so and the marker comes off.
_OVERFLOW_DEFECT = "Measured live: a search control is wider than the 320px viewport, so the page scrolls horizontally"


def _settled_overflow(driver, ready_selector=None):
    """(overflowing, body_width, window_width) once the page has rendered and stopped changing.

    Several pages grow wider only after client-side content renders (the
    datasets page was measured at 306px for the first second, then 376px), so
    a single early read can be too narrow. Waits for `ready_selector` when
    given, then for two equal width reads in a row.
    """
    CommonPage(driver).is_header_logo_visible()
    if ready_selector:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ready_selector))
        )
    last = {"w": None}

    def settled(d):
        width = d.execute_script("return document.body.scrollWidth")
        stable = width == last["w"]
        last["w"] = width
        return stable

    try:
        WebDriverWait(driver, 10, poll_frequency=0.5).until(settled)
    except Exception:
        pass  # report whatever the width is; the assertion below carries the detail
    return _has_horizontal_overflow(driver)


@pytest.mark.responsive
class TestReflowAt320:
    """WCAG 1.4.10: no horizontal scroll at 320 CSS px on the public content pages."""

    @pytest.mark.parametrize(
        "path,ready_selector",
        [
            pytest.param("", None, id="home"),
            pytest.param("about-us", None, id="about-us"),
            pytest.param("privacy-policy", None, id="privacy-policy"),
            pytest.param("datasets", "main input", id="datasets",
                         marks=pytest.mark.xfail(strict=True, raises=AssertionError, reason=_OVERFLOW_DEFECT)),
            pytest.param("glossary", "main input", id="glossary",
                         marks=pytest.mark.xfail(strict=True, raises=AssertionError, reason=_OVERFLOW_DEFECT)),
        ],
    )
    def test_page_reflows_at_320px(self, driver, path, ready_selector):
        """The page body is no wider than a 320px viewport"""
        driver.set_window_size(*REFLOW_WIDTH)
        driver.get(f"{Config.BASE_URL.rstrip('/')}/{path}")
        overflowing, body_w, window_w = _settled_overflow(driver, ready_selector)
        assert not overflowing, (
            f"/{path}: body scrollWidth {body_w}px > viewport {window_w}px at 320px wide"
        )
