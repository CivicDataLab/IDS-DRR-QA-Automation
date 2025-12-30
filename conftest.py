"""
Pytest configuration file - provides shared fixtures for all tests
"""

import pytest
import os
from datetime import datetime
from utils.driver_factory import DriverFactory
from config.config import Config
import logging

# Configure logging for self-healing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


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

    # Register self-healing plugin
    from utils.pytest_self_healing_plugin import SelfHealingPlugin
    config.pluginmanager.register(SelfHealingPlugin(), "self_healing_plugin")

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

    yield driver

    # Collect healing events before quitting
    if hasattr(driver, '_healing_events') and driver._healing_events:
        plugin = request.config.pluginmanager.get_plugin("self_healing_plugin")
        if plugin:
            plugin.healing_events.extend(driver._healing_events)

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


def pytest_html_results_table_header(cells):
    """Customize HTML report table headers"""
    cells.insert(2, '<th>Description</th>')
    cells.insert(3, '<th>Duration</th>')


def pytest_html_results_table_row(report, cells):
    """Customize HTML report table rows"""
    cells.insert(2, f'<td>{getattr(report, "description", "")}</td>')
    cells.insert(3, f'<td>{report.duration:.2f}s</td>')
