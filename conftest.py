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
# Note: Root logging configuration is handled by pytest.ini to avoid conflicts
# with pytest-xdist parallel workers in CI environments
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def pytest_configure(config):
    """Configure pytest with custom settings"""
    # Create required directories
    for directory in [
        Config.SCREENSHOTS_DIR,
        Config.ANALYTICS_SCREENSHOTS_DIR,
        Config.DATASETS_SCREENSHOTS_DIR,
        Config.REPORT_DIR,
        "reports/self_healing",
        "config"
    ]:
        os.makedirs(directory, exist_ok=True)

    # Generate timestamped report filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Override HTML report path
    if config.option.htmlpath:
        config.option.htmlpath = f"reports/test_report_{timestamp}.html"

    # Override JSON report path if enabled
    if hasattr(config.option, 'json_report_file') and config.option.json_report_file:
        config.option.json_report_file = f"reports/test_report_{timestamp}.json"

    # Note: Additional report plugins (self-healing, multistate) are disabled
    # All test information is consolidated into the main HTML report via pytest-html
    #
    # If you need to re-enable these plugins, uncomment the lines below:
    #
    # from utils.pytest_self_healing_plugin import SelfHealingPlugin
    # config.pluginmanager.register(SelfHealingPlugin(), "self_healing_plugin")
    #
    # from utils.pytest_multistate_plugin import MultiStateReportPlugin
    # if not hasattr(config, '_multistate_plugin'):
    #     multistate_plugin = MultiStateReportPlugin()
    #     config._multistate_plugin = multistate_plugin
    #     config.pluginmanager.register(multistate_plugin, "multistate_report_plugin")

    # Add metadata to HTML report
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


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture for each test with self-healing tracking

    Args:
        request: Pytest request object

    Yields:
        WebDriver: Configured WebDriver instance
    """
    driver = DriverFactory.create_driver()
    driver._healing_events = []
    driver._test_name = request.node.nodeid
    driver.get(Config.BASE_URL)

    yield driver

    # Note: Self-healing event collection is disabled
    # Healing events are tracked on the driver but not reported separately
    # All test results are in the main HTML report

    # Clear browser state before quitting to prevent interference
    try:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
    except:
        pass  # Ignore errors during cleanup

    DriverFactory.quit_driver(driver)


@pytest.fixture(scope="session")
def driver_session():
    """
    WebDriver fixture shared across all tests in session
    Use sparingly - prefer function-scoped driver for isolation

    Yields:
        WebDriver: Configured WebDriver instance
    """
    driver = DriverFactory.create_driver()
    driver.get(Config.BASE_URL)
    yield driver
    DriverFactory.quit_driver(driver)


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
    """
    Take screenshot if test fails

    Usage:
        def test_something(driver, screenshot_on_failure):
            # Screenshot auto-taken on failure
    """
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

    # Add test description
    if hasattr(item, 'function'):
        rep.description = str(item.function.__doc__)


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "IDS-DRR QA Automation Test Report"


def pytest_addoption(parser):
    """Add custom command line options"""
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
    """Set env vars based on CLI options before tests run"""
    if session.config.getoption("--no-learned-locators", False):
        os.environ["DISABLE_LEARNED_LOCATORS"] = "true"


def pytest_html_results_table_header(cells):
    """Customize HTML report table headers"""
    cells.insert(2, '<th>Description</th>')
    cells.insert(3, '<th>Duration</th>')


def pytest_html_results_table_row(report, cells):
    """Customize HTML report table rows"""
    cells.insert(2, f'<td>{getattr(report, "description", "")}</td>')
    # Only show duration for test reports, not collection reports
    duration = getattr(report, 'duration', 0)
    cells.insert(3, f'<td>{duration:.2f}s</td>')
