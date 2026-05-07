"""Page Objects module"""
from pages.base_page import BasePage
from pages.common_page import CommonPage
from pages.analytics_page import AnalyticsPage
from pages.dataset_page import DatasetPage, DatasetInfoPage

__all__ = ['BasePage', 'CommonPage', 'AnalyticsPage', 'DatasetPage', 'DatasetInfoPage']
