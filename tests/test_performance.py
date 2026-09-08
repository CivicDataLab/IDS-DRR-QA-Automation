"""
Performance Tests — page-load timing via the browser's own Navigation Timing API.

No new dependency: `window.performance.getEntriesByType('navigation')` is read
directly through Selenium's `execute_script`, the same way `wait_helpers.py`
already reads document state elsewhere in this repo.

Thresholds are deliberately generous — this is a regression guard against a page
becoming pathologically slow (e.g. a stuck request, a runaway bundle), not a
performance budget. Live measurements on dev today are well under 1s for every
page checked (Home ~760ms load, Analytics ~250ms, Datasets ~70ms), so a
multi-second threshold still catches a real problem without flaking on CI
variance.

Run:
    pytest tests/test_performance.py -v
    pytest tests/test_performance.py -m smoke -v
"""

import pytest

from config.config import Config

TTFB_THRESHOLD_MS = 3000
DOM_CONTENT_LOADED_THRESHOLD_MS = 8000
LOAD_THRESHOLD_MS = 10000

_NAVIGATION_TIMING_SCRIPT = """
const e = performance.getEntriesByType('navigation')[0];
return e ? {
    ttfb: e.responseStart - e.requestStart,
    domContentLoaded: e.domContentLoadedEventEnd - e.startTime,
    load: e.loadEventEnd - e.startTime
} : null;
"""


def _measure(driver, url):
    """Load a URL and return its Navigation Timing metrics (ms)."""
    driver.get(url)
    timing = driver.execute_script(_NAVIGATION_TIMING_SCRIPT)
    assert timing is not None, f"Navigation Timing API returned nothing for {url}"
    print(f"⏱️  {url} -> TTFB={timing['ttfb']:.0f}ms DCL={timing['domContentLoaded']:.0f}ms load={timing['load']:.0f}ms")
    return timing


def _assert_within_budget(timing, url):
    assert timing["ttfb"] < TTFB_THRESHOLD_MS, f"{url}: TTFB {timing['ttfb']:.0f}ms exceeds {TTFB_THRESHOLD_MS}ms"
    assert timing["domContentLoaded"] < DOM_CONTENT_LOADED_THRESHOLD_MS, (
        f"{url}: DOMContentLoaded {timing['domContentLoaded']:.0f}ms exceeds {DOM_CONTENT_LOADED_THRESHOLD_MS}ms"
    )
    assert timing["load"] < LOAD_THRESHOLD_MS, f"{url}: load {timing['load']:.0f}ms exceeds {LOAD_THRESHOLD_MS}ms"


@pytest.mark.performance
class TestPerformance:
    """Page-load timing budgets for the core pages."""

    @pytest.mark.smoke
    def test_home_page_load_time(self, driver):
        """Home page loads within budget"""
        timing = _measure(driver, Config.BASE_URL)
        _assert_within_budget(timing, "Home")

    def test_analytics_page_load_time(self, driver):
        """Analytics dashboard (Assam, map view) loads within budget"""
        url = f"{Config.BASE_URL.rstrip('/')}/assam/analytics?indicator=risk-score&view=map"
        timing = _measure(driver, url)
        _assert_within_budget(timing, "Analytics")

    def test_datasets_page_load_time(self, driver):
        """Datasets page loads within budget"""
        url = f"{Config.BASE_URL.rstrip('/')}/datasets"
        timing = _measure(driver, url)
        _assert_within_budget(timing, "Datasets")
