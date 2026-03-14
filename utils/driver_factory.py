from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import Config
import time


class DriverFactory:
    """Factory class for creating WebDriver instances with performance optimizations"""

    @staticmethod
    def get_chrome_options():
        """Configure and return Chrome options with performance optimizations"""
        options = Options()
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")

        if Config.HEADLESS:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')  # Faster in headless mode

        # Performance optimizations
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')  # Suppress logs

        # Faster browser startup
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-default-apps')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--disable-component-extensions-with-background-pages')

        # Disable unnecessary features for speed
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0,
            'download.prompt_for_download': False,
            'profile.managed_default_content_settings.images': 1  # Enable images (change to 2 to disable for faster loading)
        })

        # REMOVED: detach option (causes issues with parallel execution and cleanup)
        # options.add_experimental_option("detach", True)

        return options

    @staticmethod
    def create_driver():
        """Create and return a WebDriver instance with performance settings"""
        options = DriverFactory.get_chrome_options()

        if Config.IS_LOCAL:
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Remote(Config.REMOTE_LINK, options=options)

        # Set timeouts for better performance
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)

        return driver

    @staticmethod
    def quit_driver(driver):
        """Safely quit the driver"""
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error quitting driver: {e}")
