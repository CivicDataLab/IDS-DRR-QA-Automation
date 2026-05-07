"""Locators module for all page elements"""
from locators.common_locators import HeaderLocators, FooterLocators
from locators.analytics_locators import (
    AnalyticsPageLocators,
    HazardLocators,
    ExposureLocators,
    VulnerabilityLocators,
    GovtResponseLocators
)
from locators.dataset_locators import DatasetPageLocators, DatasetInfoPageLocators

__all__ = [
    'HeaderLocators',
    'FooterLocators',
    'AnalyticsPageLocators',
    'HazardLocators',
    'ExposureLocators',
    'VulnerabilityLocators',
    'GovtResponseLocators',
    'DatasetPageLocators',
    'DatasetInfoPageLocators'
]
