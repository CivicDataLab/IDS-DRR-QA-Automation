"""
Accessibility Tests — axe-core (WCAG) scans of the core IDS-DRR pages.

Only `critical`/`serious` violations fail a test — `moderate`/`minor` are logged
to stdout so they show up in the HTML report without adding flakiness from
third-party widget markup CDL doesn't control (e.g. the Bhashini translator).

Scoped to Home, one analytics dashboard (Assam — the richest state, already the
QA convention elsewhere in this repo), Datasets, Glossary, and About Us — not
every state, since axe-core scans the DOM once loaded and a second state's
shared layout wouldn't add new coverage.

Run:
    pytest tests/test_accessibility.py -v
    pytest tests/test_accessibility.py -m smoke -v
"""

import pytest
from axe_selenium_python import Axe

from config.config import Config
from pages.common_page import CommonPage

CRITICAL_IMPACTS = ("critical", "serious")


def _scan(driver, url):
    """Load a URL, wait for the shared header to render (axe-core scanning before
    hydration finishes gives inconsistent results — confirmed live: an unthrottled
    scan XPASSed a page that reliably shows a critical violation once settled),
    then run an axe-core scan and split violations by impact.
    """
    driver.get(url)
    CommonPage(driver).is_header_logo_visible()
    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    critical = [v for v in results["violations"] if v["impact"] in CRITICAL_IMPACTS]
    other = [v for v in results["violations"] if v["impact"] not in CRITICAL_IMPACTS]

    for v in other:
        print(f"ℹ️  [{v['impact']}] {v['id']}: {v['description']} (nodes={len(v['nodes'])})")
    for v in critical:
        print(f"❌ [{v['impact']}] {v['id']}: {v['description']} (nodes={len(v['nodes'])})")

    return critical


@pytest.mark.accessibility
class TestAccessibility:
    """WCAG scans of the core pages, via axe-core."""

    @pytest.mark.smoke
    @pytest.mark.xfail(
        reason="Live 2026-09-09: aria-required-children (critical), "
        "aria-valid-attr-value/aria-valid-attr (critical) on Home — tracked in issue"
    )
    def test_home_page_accessibility(self, driver):
        """Home page has no critical/serious axe-core violations"""
        critical = _scan(driver, Config.BASE_URL)
        assert not critical, f"{len(critical)} critical/serious violation(s): {[v['id'] for v in critical]}"

    @pytest.mark.xfail(
        reason="Live 2026-09-09: aria-required-children (critical), "
        "color-contrast (serious) on the analytics dashboard — tracked in issue"
    )
    def test_analytics_page_accessibility(self, driver):
        """Analytics dashboard (Assam, map view) has no critical/serious axe-core violations"""
        critical = _scan(driver, f"{Config.BASE_URL.rstrip('/')}/assam/analytics?indicator=risk-score&view=map")
        assert not critical, f"{len(critical)} critical/serious violation(s): {[v['id'] for v in critical]}"

    @pytest.mark.xfail(
        reason="Live 2026-09-09: aria-required-children, aria-valid-attr-value, label "
        "(all critical), button-name (serious, 27 nodes) on Datasets — tracked in issue"
    )
    def test_datasets_page_accessibility(self, driver):
        """Datasets page has no critical/serious axe-core violations"""
        critical = _scan(driver, f"{Config.BASE_URL.rstrip('/')}/datasets")
        assert not critical, f"{len(critical)} critical/serious violation(s): {[v['id'] for v in critical]}"

    @pytest.mark.xfail(
        reason="Live 2026-09-09: aria-required-children (critical) on Glossary — tracked in issue"
    )
    def test_glossary_page_accessibility(self, driver):
        """Glossary page has no critical/serious axe-core violations"""
        critical = _scan(driver, f"{Config.BASE_URL.rstrip('/')}/glossary")
        assert not critical, f"{len(critical)} critical/serious violation(s): {[v['id'] for v in critical]}"

    @pytest.mark.xfail(
        reason="Live 2026-09-09: aria-required-children (critical) on About Us — tracked in issue"
    )
    def test_about_us_page_accessibility(self, driver):
        """About Us page has no critical/serious axe-core violations"""
        critical = _scan(driver, f"{Config.BASE_URL.rstrip('/')}/about-us")
        assert not critical, f"{len(critical)} critical/serious violation(s): {[v['id'] for v in critical]}"
