"""Test data configurations for different test scenarios"""


class AnalyticsTestData:
    """Test data for analytics flow tests"""

    # State-specific district and revenue circle mappings
    STATE_SPECIFIC_DATA = {
        'assam': {
            'district': 'Sivasagar',
            'revenue_circle': 'Sibsagar'
        },
        'himachal_pradesh': {
            'district': 'Shimla',
            'revenue_circle': 'Shimla'
        },
        'odisha': {
            'district': 'Khordha',
            'revenue_circle': 'Bhubaneswar'
        },
        'bihar': {
            'district': 'Patna',
            'revenue_circle': 'Patna Sadar'
        },
        'uttar_pradesh': {
            'district': 'Lucknow',
            'revenue_circle': 'Lucknow'
        }
    }

    MAP_VIEW_DATA = {
        'view_type': 'map',
        'screenshot_prefix': 'map_',
        'calendar_month': '7',
        'view_index': 1
    }

    CHART_VIEW_DATA = {
        'view_type': 'chart',
        'screenshot_prefix': 'chart_',
        'calendar_month': '8',
        'view_index': 2
    }

    TABLE_VIEW_DATA = {
        'view_type': 'table',
        'screenshot_prefix': 'table_',
        'calendar_month': '9',
        'view_index': 3
    }

    ALL_VIEWS = [MAP_VIEW_DATA, CHART_VIEW_DATA, TABLE_VIEW_DATA]

    @staticmethod
    def get_district_for_state(state_key):
        """Get district for a specific state"""
        return AnalyticsTestData.STATE_SPECIFIC_DATA.get(state_key, {}).get('district', 'Select a district')

    @staticmethod
    def get_revenue_circle_for_state(state_key):
        """Get revenue circle for a specific state"""
        return AnalyticsTestData.STATE_SPECIFIC_DATA.get(state_key, {}).get('revenue_circle', 'Select a revenue circle')


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
