from pages.base_page import BasePage
from locators.analytics_locators import (
    AnalyticsPageLocators,
    HazardLocators,
    ExposureLocators,
    VulnerabilityLocators,
    GovtResponseLocators
)
from config.config import Config


class AnalyticsPage(BasePage):
    """Page Object for Analytics page"""

    def __init__(self, driver):
        super().__init__(driver)
        self.screenshot_dir = Config.ANALYTICS_SCREENSHOTS_DIR

    def select_view(self, view_index):
        """
        Select analytics view (1=Map, 2=Chart, 3=Table)

        Args:
            view_index: View index (1, 2, or 3)

        Returns:
            bool: Success status
        """
        locator = AnalyticsPageLocators.get_view_button(view_index)
        view_names = {1: "Map View", 2: "Chart View", 3: "Table View"}
        return self.click(locator, view_names.get(view_index, f"View {view_index}"))

    def select_district(self, district_name):
        """Select district from dropdown"""
        success = self.select_dropdown_by_text(
            AnalyticsPageLocators.DISTRICT_SELECT,
            district_name,
            "District Dropdown"
        )
        if success:
            print(f"Selected district: {district_name}")
        return success

    def select_revenue_circle(self, revenue_circle_name):
        """Select revenue circle from dropdown"""
        success = self.select_dropdown_by_text(
            AnalyticsPageLocators.REVENUE_CIRCLE_SELECT,
            revenue_circle_name,
            "Revenue Circle Dropdown"
        )
        if success:
            print(f"Selected revenue circle: {revenue_circle_name}")
        return success

    def open_calendar(self):
        """Open calendar picker"""
        return self.click(AnalyticsPageLocators.CALENDAR_BUTTON, "Calendar Button")

    def select_calendar_month(self, month):
        """
        Select month from calendar

        Args:
            month: Month value (as string)

        Returns:
            bool: Success status
        """
        locator = AnalyticsPageLocators.get_calendar_month(month)
        return self.click(locator, f"Calendar Month {month}")

    def take_analytics_screenshot(self, filename_prefix, description=""):
        """
        Take screenshot with analytics directory

        Args:
            filename_prefix: Prefix for filename
            description: Optional description for filename
        """
        filename = f"{filename_prefix}{description}.png" if description else f"{filename_prefix}.png"
        return self.take_screenshot(filename, self.screenshot_dir)

    # Hazard Section Methods
    def expand_hazard_options(self, screenshot_prefix=None):
        """Expand Hazard options section"""
        if self.interact_with_option(
            HazardLocators.EXPAND_COLLAPSE,
            "Hazard Options",
            f"{screenshot_prefix}hazard_show_options" if screenshot_prefix else None,
            self.screenshot_dir
        ):
            return True
        return False

    def collapse_hazard_options(self):
        """Collapse Hazard options section"""
        return self.click(HazardLocators.EXPAND_COLLAPSE, "Collapse Hazard Options")

    def select_hazard_option(self, option_name, screenshot_prefix=None):
        """
        Select a hazard option

        Args:
            option_name: Name of the hazard option (monthly_rainfall, inundation, elevation)
            screenshot_prefix: Prefix for screenshot

        Returns:
            bool: Success status
        """
        hazard_options = {
            'monthly_rainfall': (HazardLocators.TOTAL_MONTHLY_RAINFALL, "Total Monthly Rainfall", "monthly_rainfall"),
            'inundation': (HazardLocators.SUM_INUNDATION_INTENSITIES, "Sum of Inundation Intensities", "sum_inundation_ratio"),
            'elevation': (HazardLocators.MEAN_ELEVATION, "Mean Elevation", "mean_elevation")
        }

        if option_name not in hazard_options:
            print(f"❌ Unknown hazard option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = hazard_options[option_name]
        screenshot_name = f"{screenshot_prefix}hazard_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)

    # Exposure Section Methods
    def expand_exposure_options(self, screenshot_prefix=None):
        """Expand Exposure options section"""
        return self.interact_with_option(
            ExposureLocators.EXPAND_COLLAPSE,
            "Exposure Options",
            f"{screenshot_prefix}exposure_show_options" if screenshot_prefix else None,
            self.screenshot_dir
        )

    def collapse_exposure_options(self):
        """Collapse Exposure options section"""
        return self.click(ExposureLocators.EXPAND_COLLAPSE, "Collapse Exposure Options")

    def select_exposure_option(self, option_name, screenshot_prefix=None):
        """
        Select an exposure option

        Args:
            option_name: Name of the exposure option
            screenshot_prefix: Prefix for screenshot

        Returns:
            bool: Success status
        """
        exposure_options = {
            'households': (ExposureLocators.TOTAL_HOUSEHOLDS, "Total Households", "total_households"),
            'population': (ExposureLocators.POPULATION, "Population", "population"),
            'elderly': (ExposureLocators.ELDERLY_POPULATION, "Elderly Population", "elderly_population"),
            'children': (ExposureLocators.CHILDREN_POPULATION, "Children Population", "children_population")
        }

        if option_name not in exposure_options:
            print(f"❌ Unknown exposure option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = exposure_options[option_name]
        screenshot_name = f"{screenshot_prefix}exposure_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)

    # Vulnerability Section Methods
    def expand_vulnerability_options(self, screenshot_prefix=None):
        """Expand Vulnerability options section"""
        return self.interact_with_option(
            VulnerabilityLocators.EXPAND_COLLAPSE,
            "Vulnerability Options",
            f"{screenshot_prefix}vulnerability_show_options" if screenshot_prefix else None,
            self.screenshot_dir
        )

    def collapse_vulnerability_options(self):
        """Collapse Vulnerability options section"""
        return self.click(VulnerabilityLocators.EXPAND_COLLAPSE, "Collapse Vulnerability Options")

    def select_vulnerability_option(self, option_name, screenshot_prefix=None):
        """Select a vulnerability option"""
        vulnerability_options = {
            'health_centres': (VulnerabilityLocators.HEALTH_CENTRES, "Health Centres", "health_centre"),
            'electricity': (VulnerabilityLocators.DOMESTIC_ELECTRICITY, "Domestic Electricity", "domestic_electricity"),
            'water': (VulnerabilityLocators.PIPED_WATER, "Piped Water", "piped_water"),
            'sanitation': (VulnerabilityLocators.WITHOUT_SANITATION, "Without Sanitation", "without_sanitation"),
            'schools': (VulnerabilityLocators.NUMBER_OF_SCHOOLS, "Number of Schools", "number_schools"),
            'rail': (VulnerabilityLocators.RAIL_LENGTH, "Rail Length", "rail_length"),
            'road': (VulnerabilityLocators.ROAD_LENGTH, "Road Length", "road_length"),
            'sown_area': (VulnerabilityLocators.NET_SOWN_AREA, "Net Sown Area", "sown_area"),
            'sex_ratio': (VulnerabilityLocators.MEAN_SEX_RATIO, "Mean Sex Ratio", "sex_ratio"),
            'population_affected': (VulnerabilityLocators.POPULATION_AFFECTED, "Population Affected", "population_affected"),
            'lives_lost': (VulnerabilityLocators.HUMAN_LIVES_LOST, "Human Lives Lost", "humans_life_lost"),
            'crop_affected': (VulnerabilityLocators.CROP_AREA_AFFECTED, "Crop Area Affected", "crop_area_affected"),
            'embankments_affected': (VulnerabilityLocators.EMBANKMENTS_AFFECTED, "Embankments Affected", "embankments_affected"),
            'roads_damaged': (VulnerabilityLocators.ROADS_DAMAGED, "Roads Damaged", "roads_damaged"),
            'bridges_damaged': (VulnerabilityLocators.BRIDGES_DAMAGED, "Bridges Damaged", "bridges_damaged"),
            'embankments_breached': (VulnerabilityLocators.EMBANKMENTS_BREACHED, "Embankments Breached", "embankments_breached")
        }

        if option_name not in vulnerability_options:
            print(f"❌ Unknown vulnerability option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = vulnerability_options[option_name]
        screenshot_name = f"{screenshot_prefix}vulnerability_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)

    # Government Response Section Methods
    def expand_govt_response_options(self, screenshot_prefix=None):
        """Expand Government Response options section"""
        # Scroll to element first
        self.scroll_to_element(GovtResponseLocators.EXPAND_COLLAPSE)

        return self.interact_with_option(
            GovtResponseLocators.EXPAND_COLLAPSE,
            "Government Response Options",
            f"{screenshot_prefix}govt_response_show_options" if screenshot_prefix else None,
            self.screenshot_dir
        )

    def collapse_govt_response_options(self):
        """Collapse Government Response options section"""
        self.scroll_to_element(GovtResponseLocators.EXPAND_COLLAPSE)
        return self.click(GovtResponseLocators.EXPAND_COLLAPSE, "Collapse Government Response Options")

    def select_govt_response_option(self, option_name, screenshot_prefix=None):
        """Select a government response option"""
        govt_response_options = {
            'flood_tenders': (GovtResponseLocators.FLOOD_TENDERS, "Flood Tenders", "flood_tenders"),
            'sdrf': (GovtResponseLocators.SDRF, "SDRF", "flood_tenders_sdrf"),
            'repairs': (GovtResponseLocators.REPAIRS_RESTORATION, "Repairs and Restoration", "flood_tenders_repair_restore"),
            'immediate': (GovtResponseLocators.IMMEDIATE_MEASURES, "Immediate Measures", "flood_tenders_immediate_measures"),
            'others': (GovtResponseLocators.OTHERS, "Others", "flood_tenders_other"),
            'funds': (GovtResponseLocators.FUNDS_ALLOCATED_SDRF_SEC, "Funds Allocated SDRF SEC", "funds_allocated_sdrf_sec")
        }

        if option_name not in govt_response_options:
            print(f"❌ Unknown government response option: {option_name}")
            return False

        locator, display_name, screenshot_suffix = govt_response_options[option_name]
        screenshot_name = f"{screenshot_prefix}govt_response_{screenshot_suffix}" if screenshot_prefix else None

        return self.interact_with_option(locator, display_name, screenshot_name, self.screenshot_dir)
