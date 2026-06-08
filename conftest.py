"""
Pytest configuration file - provides shared fixtures for all tests
"""

import pytest
import os
from datetime import datetime
from utils.driver_factory import DriverFactory
from config.config import Config
import logging

# Suppress verbose logging from selenium and urllib3
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def pytest_configure(config):
    """Configure pytest with custom settings"""
    for directory in [
        Config.SCREENSHOTS_DIR,
        Config.ANALYTICS_SCREENSHOTS_DIR,
        Config.DATASETS_SCREENSHOTS_DIR,
        Config.REPORT_DIR,
        "reports/self_healing",
        "config"
    ]:
        os.makedirs(directory, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Override HTML report path only if it's the default from pytest.ini addopts.
    # CLI-provided --html paths (e.g. CI shard names) are preserved as-is.
    if config.option.htmlpath == "reports/report.html":
        config.option.htmlpath = f"reports/test_report_{timestamp}.html"

    if hasattr(config.option, 'json_report_file') and config.option.json_report_file:
        config.option.json_report_file = f"reports/test_report_{timestamp}.json"

    config._metadata = {
        "Project": "IDS-DRR QA Automation",
        "Framework": "Selenium + Pytest",
        "Python": "3.8+",
        "Base URL": Config.BASE_URL,
        "Mode": "Local" if Config.IS_LOCAL else "Remote",
        "Browser": "Chrome",
        "Timeout": f"{Config.DEFAULT_TIMEOUT}s",
        "Self-Healing": "Enabled" if not config.getoption("--disable-healing", False) else "Disabled",
        "Learned Locators": "Disabled" if config.getoption("--no-learned-locators", False) else "Enabled",
        "Timestamp": timestamp
    }


def pytest_collection_modifyitems(items):
    """Tag state-parametrized tests with xdist_group so all tests for the
    same state go to the same worker, enabling Chrome session reuse per state."""
    for item in items:
        if hasattr(item, 'callspec') and 'state_key' in item.callspec.params:
            state = item.callspec.params['state_key']
            item.add_marker(pytest.mark.xdist_group(name=state))


@pytest.fixture(scope="session")
def _state_drivers():
    """
    Session-scoped Chrome pool keyed by state_key.
    One Chrome instance per state, shared across all test classes for that state.
    With --dist loadgroup, all tests for a state land on the same worker,
    so this dict is the single source of truth for that state's driver.
    """
    drivers = {}
    yield drivers
    for d in drivers.values():
        try:
            d.delete_all_cookies()
            d.execute_script("window.localStorage.clear();")
            d.execute_script("window.sessionStorage.clear();")
        except Exception:
            pass
        DriverFactory.quit_driver(d)


@pytest.fixture(scope="function")
def driver(request, _state_drivers):
    """
    WebDriver fixture.
    - State-parametrized tests: one Chrome per state_key, reused across tests.
      Between tests: cookies/storage cleared, navigates back to BASE_URL.
    - Non-state tests: fresh Chrome per test (original behaviour).
    """
    state_key = None
    if hasattr(request.node, 'callspec') and 'state_key' in request.node.callspec.params:
        state_key = request.node.callspec.params['state_key']

    if state_key:
        if state_key not in _state_drivers:
            d = DriverFactory.create_driver()
            d.get(Config.BASE_URL)
            _state_drivers[state_key] = d

        d = _state_drivers[state_key]

        # Reset state before each test; recover if the browser crashed
        try:
            d.delete_all_cookies()
            d.execute_script("window.localStorage.clear();")
            d.execute_script("window.sessionStorage.clear();")
            d.get(Config.BASE_URL)
        except Exception:
            DriverFactory.quit_driver(d)
            d = DriverFactory.create_driver()
            d.get(Config.BASE_URL)
            _state_drivers[state_key] = d

        d._healing_events = []
        d._test_name = request.node.nodeid
        yield d
        # Driver stays alive — torn down at session end by _state_drivers fixture

    else:
        # Non-state test: fresh Chrome, original behaviour
        d = DriverFactory.create_driver()
        d._healing_events = []
        d._test_name = request.node.nodeid
        d.get(Config.BASE_URL)
        yield d
        try:
            d.delete_all_cookies()
            d.execute_script("window.localStorage.clear();")
            d.execute_script("window.sessionStorage.clear();")
        except Exception:
            pass
        DriverFactory.quit_driver(d)


@pytest.fixture(scope="session")
def driver_session():
    """
    Shared driver across all tests in a session.
    Discouraged — prefer the state-aware `driver` fixture above.
    """
    d = DriverFactory.create_driver()
    d.get(Config.BASE_URL)
    yield d
    DriverFactory.quit_driver(d)


@pytest.fixture(scope="function", autouse=True)
def test_info(request):
    """Automatically capture and log test information"""
    test_name = request.node.name
    test_file = request.node.fspath

    print(f"\n{'='*70}")
    print(f"Test: {test_name}")
    print(f"File: {test_file}")
    print(f"{'='*70}")

    yield

    print(f"\n{'='*70}")
    print(f"Completed: {test_name}")
    print(f"{'='*70}\n")


@pytest.fixture(scope="function")
def screenshot_on_failure(driver, request):
    """Take screenshot on test failure."""
    yield

    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = os.path.join(
            Config.SCREENSHOTS_DIR,
            f"FAILED_{test_name}_{timestamp}.png"
        )
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if hasattr(item, 'function'):
        rep.description = str(item.function.__doc__)


def pytest_html_report_title(report):
    report.title = "IDS-DRR QA Automation Test Report"


def pytest_addoption(parser):
    parser.addoption(
        "--disable-healing",
        action="store_true",
        default=False,
        help="Disable self-healing locators"
    )
    parser.addoption(
        "--no-learned-locators",
        action="store_true",
        default=False,
        help="Disable loading and using previously learned locators"
    )


def pytest_sessionstart(session):
    if session.config.getoption("--no-learned-locators", False):
        os.environ["DISABLE_LEARNED_LOCATORS"] = "true"


def pytest_html_results_table_header(cells):
    cells.insert(2, '<th>Description</th>')
    cells.insert(3, '<th>Duration</th>')


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f'<td>{getattr(report, "description", "")}</td>')
    duration = getattr(report, 'duration', 0)
    cells.insert(3, f'<td>{duration:.2f}s</td>')
