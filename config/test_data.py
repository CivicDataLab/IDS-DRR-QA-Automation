"""Test data configurations for different test scenarios"""


class AnalyticsTestData:
    """Test data for analytics flow tests"""

    MAP_VIEW_DATA = {
        'view_type': 'map',
        'screenshot_prefix': 'map_',
        'district': 'Sivasagar',
        'revenue_circle': 'Sibsagar',
        'calendar_month': '7',
        'view_index': 1
    }

    CHART_VIEW_DATA = {
        'view_type': 'chart',
        'screenshot_prefix': 'chart_',
        'district': 'Cachar',
        'revenue_circle': 'Sonai',
        'calendar_month': '8',
        'view_index': 2
    }

    TABLE_VIEW_DATA = {
        'view_type': 'table',
        'screenshot_prefix': 'table_',
        'district': 'South salmara mancachar',
        'revenue_circle': 'Mankachar',
        'calendar_month': '9',
        'view_index': 3
    }

    ALL_VIEWS = [MAP_VIEW_DATA, CHART_VIEW_DATA, TABLE_VIEW_DATA]


class DatasetTestData:
    """Test data for dataset flow tests"""

    SOURCE_FILTER = 'DRIMS'
    DATASET_NAME = 'DRIMS'


class ComponentTestData:
    """Test data for component visibility tests"""

    HEADER_LINKS = ['Home', 'Analytics', 'Datasets', 'About Us']

    FOOTER_LOGOS = {
        'IDS-DRR': 'IDS-DRR logo',
        'CDL': 'CDL logo',
        'OCP': 'OCP logo'
    }

    PARTNER_LOGOS = [
        'Rockefeller Foundation',
        'PJMF',
        'ASDMA',
        'HPSDMA'
    ]
