"""
GIGW 3.0 / WCAG 2.1 AA checks that go beyond tests/test_accessibility.py.

That file runs one broad axe scan per page and tolerates everything below
"serious". This one pins specific, measured outcomes so a single rule or
criterion going green (or regressing) is visible on its own:

  * axe-core 4.10.2 restricted to the WCAG 2.0/2.1 A and AA rules, asserted
    clean on the pages that are clean today, and rule-by-rule on the pages
    that are not;
  * page-structure criteria axe does not report: one <main> landmark (1.3.1),
    a descriptive <title> per page (2.4.2), a skip link (2.4.1), a heading 1
    (1.3.1/2.4.6), the document language (3.1.1) and the mobile menu button's
    expanded state (4.1.2).

Every known defect is asserted as the correct behaviour under a strict xfail,
so fixing the product turns the test into an XPASS failure and the marker has
to come off. Nothing here modifies product code or data.

Not covered, because it cannot be judged from the DOM: reading order, focus
order quality, meaningful alt text, and the Bhashini plugin's own widget
(third-party, and unreachable from some networks).

Run:
    pytest tests/test_accessibility_gigw.py -v -m accessibility
"""

import pytest
from axe_selenium_python import Axe
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config
from locators.common_locators import HeaderLocators
from locators.module_analytics_locators import ModuleAnalyticsLocators
from pages.common_page import CommonPage
from utils.driver_factory import DriverFactory

WCAG_AA_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]

CONTENT_PAGES = ["", "about-us", "privacy-policy", "datasets", "glossary"]


def _url(path):
    return f"{Config.BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def _wcag_violations(driver, url, ready=()):
    """Load `url`, wait for hydration, and return axe's WCAG 2.x A/AA violations by rule id.

    `ready` lists the locators of the late-rendering controls the assertion is
    about. axe only sees what is in the DOM when it runs, and these controls
    render after the header (measured: a scan taken too early reported neither
    defect), so each test names what must exist before scanning.
    """
    driver.get(url)
    CommonPage(driver).is_header_logo_visible()
    for locator in ready:
        WebDriverWait(driver, Config.LONG_TIMEOUT).until(EC.presence_of_element_located(locator))
    axe = Axe(driver)
    axe.inject()
    results = axe.run(options={"runOnly": {"type": "tag", "values": WCAG_AA_TAGS}})
    found = {}
    for violation in results["violations"]:
        found[violation["id"]] = violation
        print(f"[{violation['impact']}] {violation['id']}: {len(violation['nodes'])} node(s) - {violation['help']}")
    return found


def _strict_xfail(reason):
    return pytest.mark.xfail(strict=True, raises=AssertionError, reason=reason)


@pytest.mark.accessibility
class TestWcagRulesClean:
    """Pages with no WCAG 2.x A/AA axe violations today stay that way."""

    @pytest.mark.parametrize("path", ["", "about-us", "glossary"])
    def test_page_has_no_wcag_aa_violations(self, driver, path):
        """axe-core finds no WCAG 2.0/2.1 A or AA rule violations"""
        found = _wcag_violations(driver, _url(path))
        assert not found, f"/{path}: {[(i, len(v['nodes'])) for i, v in found.items()]}"


@pytest.mark.accessibility
class TestWcagRuleDefects:
    """Rule-level defects measured live on dev, each pinned to the page and rule."""

    @pytest.mark.multistate
    @_strict_xfail("Measured live: risk-count tag text on the Assam hub fails 4.5:1 contrast")
    def test_state_hub_text_contrast(self, driver):
        """The state hub's text meets WCAG 1.4.3 contrast (color-contrast)"""
        found = _wcag_violations(
            driver, _url("en/assam"), ready=[(By.XPATH, "//main//*[contains(., 'Very High Risk')]")]
        )
        assert "color-contrast" not in found, (
            f"color-contrast on {len(found['color-contrast']['nodes'])} node(s), e.g. "
            f"{found['color-contrast']['nodes'][0]['html'][:100]}"
        )

    @_strict_xfail("Measured live: the Sort select on the datasets page has no accessible name")
    def test_datasets_selects_have_names(self, driver):
        """Every select on /datasets has an accessible name (WCAG 4.1.2, select-name)"""
        found = _wcag_violations(driver, _url("datasets"), ready=[(By.CSS_SELECTOR, "main select")])
        assert "select-name" not in found, (
            f"unnamed select: {found['select-name']['nodes'][0]['html'][:120]}"
        )

    @pytest.mark.multistate
    @pytest.mark.parametrize(
        "rule",
        [
            pytest.param(
                "select-name",
                marks=_strict_xfail("Measured live: the sidebar State select has no accessible name"),
            ),
            pytest.param(
                "nested-interactive",
                marks=_strict_xfail(
                    "Measured live: sidebar section headers are role=button containers holding focusable children"
                ),
            ),
        ],
    )
    def test_analytics_sidebar_rule(self, driver, rule):
        """The analytics dashboard sidebar passes this WCAG rule"""
        found = _wcag_violations(
            driver,
            _url("en/assam/flood/analytics?indicator=risk-score&view=map"),
            ready=[
                ModuleAnalyticsLocators.INDICATOR_TITLE,
                ModuleAnalyticsLocators.STATE_SELECT,
                (By.CSS_SELECTOR, "aside [role='button'][aria-label]"),
            ],
        )
        assert rule not in found, (
            f"{rule}: {len(found[rule]['nodes'])} node(s), e.g. {found[rule]['nodes'][0]['html'][:120]}"
        )


@pytest.fixture(scope="module")
def page_facts():
    """Structural facts for each content page, read once with a single browser."""
    driver = DriverFactory.create_driver()
    facts = {}
    try:
        for path in CONTENT_PAGES:
            driver.get(_url(path))
            CommonPage(driver).is_header_logo_visible()
            facts[path] = driver.execute_script(
                """
                return {
                  title: document.title,
                  lang: document.documentElement.lang,
                  mains: document.querySelectorAll('main, [role="main"]').length,
                  h1s: document.querySelectorAll('h1').length
                };
                """
            )
    finally:
        DriverFactory.quit_driver(driver)
    return facts


@pytest.mark.accessibility
class TestPageStructure:
    """Criteria axe's WCAG rules do not report on these pages."""

    @pytest.mark.parametrize("path", CONTENT_PAGES)
    def test_document_language_is_declared(self, page_facts, path):
        """<html lang> is set to the locale in the URL (WCAG 3.1.1)"""
        assert page_facts[path]["lang"] == "en", (
            f"/{path}: <html lang> is {page_facts[path]['lang']!r}, expected 'en' for the /en route"
        )

    @pytest.mark.parametrize(
        "path",
        [
            pytest.param(p, marks=_strict_xfail("Measured live: the page renders more than one <main> landmark"))
            for p in CONTENT_PAGES
        ],
    )
    def test_single_main_landmark(self, page_facts, path):
        """The page has exactly one main landmark (WCAG 1.3.1)"""
        assert page_facts[path]["mains"] == 1, (
            f"/{path}: {page_facts[path]['mains']} <main>/role=main landmarks"
        )

    @pytest.mark.parametrize(
        "path",
        [
            "",
            "about-us",
            "privacy-policy",
            pytest.param("datasets", marks=_strict_xfail("Measured live: no <h1> on the page")),
            pytest.param("glossary", marks=_strict_xfail("Measured live: no <h1> on the page")),
        ],
    )
    def test_page_has_one_h1(self, page_facts, path):
        """The page has exactly one level-1 heading (WCAG 1.3.1, 2.4.6)"""
        assert page_facts[path]["h1s"] == 1, f"/{path}: {page_facts[path]['h1s']} <h1> elements"

    @_strict_xfail("Measured live: every page is titled just 'IDS-DRR'")
    def test_pages_have_distinct_titles(self, page_facts):
        """Each page's <title> identifies that page (WCAG 2.4.2)"""
        titles = {path or "home": facts["title"] for path, facts in page_facts.items()}
        assert len(set(titles.values())) == len(titles), f"identical page titles: {titles}"

    @_strict_xfail("Measured live: the first Tab stop is the logo link; there is no skip link")
    def test_skip_link_is_first_tab_stop(self, driver):
        """The first keyboard stop is a link to an in-page target (WCAG 2.4.1, GIGW skip-to-content)"""
        driver.get(_url(""))
        CommonPage(driver).is_header_logo_visible()
        ActionChains(driver).send_keys(Keys.TAB).perform()
        target = driver.execute_script(
            """
            var el = document.activeElement;
            var href = el && el.tagName === 'A' ? el.getAttribute('href') || '' : '';
            return {href: href, resolves: href.charAt(0) === '#' && href.length > 1 &&
                    !!document.getElementById(href.slice(1))};
            """
        )
        assert target["resolves"], (
            f"first Tab stop is {target['href']!r}, not an in-page skip link to an existing id"
        )

    @pytest.mark.responsive
    @_strict_xfail("Measured live: the Menu button never gets aria-expanded")
    def test_mobile_menu_button_reports_expanded_state(self, driver):
        """The mobile Menu button exposes aria-expanded and flips it when opened (WCAG 4.1.2)"""
        driver.set_window_size(375, 800)
        driver.get(_url(""))
        common = CommonPage(driver)
        assert common.is_mobile_menu_button_visible(), "Menu button not visible at 375px"

        def expanded():
            # Re-find each time: opening the menu re-renders the header.
            return driver.find_element(*HeaderLocators.MOBILE_MENU_BUTTON).get_attribute("aria-expanded")

        closed = expanded()
        assert common.open_mobile_menu(), "Could not open the mobile menu"
        opened = expanded()
        assert (closed, opened) == ("false", "true"), (
            f"aria-expanded was {closed!r} before and {opened!r} after opening the menu"
        )
