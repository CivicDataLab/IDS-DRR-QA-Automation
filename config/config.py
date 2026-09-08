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
    # Support both production and development URLs
    # DEV_URL takes precedence if set, otherwise falls back to URL
    BASE_URL = os.getenv('DEV_URL') or os.getenv('URL', '')
    HOME_URL_4 = os.getenv('HOME_URL_4', '')
    MEDIUM_URL = os.getenv('MEDIUM_URL', '')

    # Environment indicator
    ENVIRONMENT = 'development' if os.getenv('DEV_URL') else 'production'

    # DataSpace instances backing IDS-DRR.
    # These host the datasets IDS-DRR reads from; an outage here silently breaks
    # the platform, so availability is smoke-checked directly.
    DATASPACE_DEV_URL = os.getenv(
        'DATASPACE_DEV_URL', 'https://dev.dataspace.open-contracting.in'
    )
    DATASPACE_PROD_URL = os.getenv(
        'DATASPACE_PROD_URL', 'https://dataspace.open-contracting.in'
    )

    # The DataSpace GraphQL APIs. These fail independently of the web UIs above —
    # on 2026-09-03 the API container and the frontend process went down for two
    # different reasons, so probing only the UI can miss a dead API entirely.
    DATASPACE_DEV_API_URL = os.getenv(
        'DATASPACE_DEV_API_URL', 'https://api.dev.dataspace.open-contracting.in/api/graphql'
    )
    DATASPACE_PROD_API_URL = os.getenv(
        'DATASPACE_PROD_API_URL', 'https://api.dataspace.open-contracting.in/api/graphql'
    )

    # Timeout (seconds) for plain HTTP availability probes
    HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT', '20'))

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
