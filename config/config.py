import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Central configuration for the test framework.
    All values are loaded from .env file.
    """

    # Environment
    IS_LOCAL = os.getenv('LOCAL', 'true').lower() == 'true'
    REMOTE_LINK = os.getenv('REMOTE_LINK', '')

    # URLs
    BASE_URL = os.getenv('URL', '')
    HOME_URL_4 = os.getenv('HOME_URL_4', '')
    MEDIUM_URL = os.getenv('MEDIUM_URL', '')

    # Authentication
    USERNAME = os.getenv('HOME_URL_USERNAME', '')
    PASSWORD = os.getenv('HOME_URL_PASSWORD', '')

    # Timeouts (in seconds) - OPTIMIZED defaults for better performance
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '10'))  # Reduced from 20
    SHORT_TIMEOUT = int(os.getenv('SHORT_TIMEOUT', '5'))       # Reduced from 10
    LONG_TIMEOUT = int(os.getenv('LONG_TIMEOUT', '15'))        # Reduced from 30
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '1'))

    # Browser Settings - can be customized in .env or use defaults
    WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '1920'))
    WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '1080'))
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

    # Directory paths (constants, not in .env)
    SCREENSHOTS_DIR = './screenshots'
    ANALYTICS_SCREENSHOTS_DIR = './screenshots/analytics'
    DATASETS_SCREENSHOTS_DIR = './screenshots/datasets'
    REPORT_DIR = './reports'
    REPORT_FILENAME = 'comprehensive_report.pdf'
