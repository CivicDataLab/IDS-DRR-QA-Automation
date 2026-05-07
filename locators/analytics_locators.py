from selenium.webdriver.common.by import By


class AnalyticsPageLocators:
    """Locators for Analytics page elements"""

    # View toggle buttons
    MAP_VIEW_BUTTON = (By.XPATH, "/html/body/main/div/main/div/div[1]/button[1]/span")
    CHART_VIEW_BUTTON = (By.XPATH, "/html/body/main/div/main/div/div[1]/button[2]/span")
    TABLE_VIEW_BUTTON = (By.XPATH, "/html/body/main/div/main/div/div[1]/button[3]/span")

    # Dropdowns
    DISTRICT_SELECT = (By.NAME, "district-select")
    REVENUE_CIRCLE_SELECT = (By.NAME, "revenue-circle-select")

    # Calendar
    CALENDAR_BUTTON = (By.XPATH, "//button[@aria-label='Calendar']")

    @staticmethod
    def get_calendar_month(month):
        """Get locator for specific calendar month"""
        return (By.XPATH, f"//button[@value='{month}']")

    @staticmethod
    def get_view_button(index):
        """Get locator for view button by index (1=map, 2=chart, 3=table)"""
        return (By.XPATH, f"/html/body/main/div/main/div/div[1]/button[{index}]/span")


class HazardLocators:
    """Locators for Hazard section in Analytics"""

    # Expand/Collapse - target the parent div that contains both expand and collapse states
    EXPAND_COLLAPSE = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]")
    # Collapse button specifically (visible on hover) - targets the button with upward chevron
    COLLAPSE_BUTTON = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]//button[@type='button']")

    # Options
    TOTAL_MONTHLY_RAINFALL = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/span/div/label/span")
    SUM_INUNDATION_INTENSITIES = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/span/div/label/span")
    MEAN_ELEVATION = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/span/div/label/span")


class ExposureLocators:
    """Locators for Exposure section in Analytics"""

    # Expand/Collapse - target the parent div that contains both expand and collapse states
    EXPAND_COLLAPSE = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div/div/div/div[1]")
    # Collapse button specifically (visible on hover) - targets the button with upward chevron
    COLLAPSE_BUTTON = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div/div/div/div[1]//button[@type='button']")

    # Options
    TOTAL_HOUSEHOLDS = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/span/div/label/span")
    POPULATION = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/span/div/label/span")
    ELDERLY_POPULATION = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[3]/div/span/div/label/span")
    CHILDREN_POPULATION = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[4]/div/span/div/label/span")


class VulnerabilityLocators:
    """Locators for Vulnerability section in Analytics"""

    # Expand/Collapse - target the parent div that contains both expand and collapse states
    EXPAND_COLLAPSE = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div/div/div/div[1]")
    # Collapse button specifically (visible on hover) - targets the button with upward chevron
    COLLAPSE_BUTTON = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div/div/div/div[1]//button[@type='button']")

    # Infrastructure Options
    HEALTH_CENTRES = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/span/div/label/span")
    DOMESTIC_ELECTRICITY = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[2]/div/span/div/label/span")
    PIPED_WATER = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[3]/div/span/div/label/span")
    WITHOUT_SANITATION = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[4]/div/span/div/label/span")
    NUMBER_OF_SCHOOLS = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[5]/div/span/div/label/span")
    RAIL_LENGTH = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[6]/div/span/div/label/span")
    ROAD_LENGTH = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[7]/div/span/div/label/span")
    NET_SOWN_AREA = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[8]/div/span/div/label/span")
    MEAN_SEX_RATIO = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[9]/div/span/div/label/span")

    # Impact Options
    POPULATION_AFFECTED = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[10]/div/span/div/label/span")
    HUMAN_LIVES_LOST = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[11]/div/span/div/label/span")
    CROP_AREA_AFFECTED = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[12]/div/span/div/label/span")
    EMBANKMENTS_AFFECTED = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[13]/div/span/div/label/span")
    ROADS_DAMAGED = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[14]/div/span/div/label/span")
    BRIDGES_DAMAGED = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[15]/div/span/div/label/span")
    EMBANKMENTS_BREACHED = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[16]/div/span/div/label/span")


class GovtResponseLocators:
    """Locators for Government Response section in Analytics"""

    # Expand/Collapse - target the parent div that contains both expand and collapse states
    EXPAND_COLLAPSE = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div/div/div/div[1]")
    # Collapse button specifically (visible on hover) - targets the button with upward chevron
    COLLAPSE_BUTTON = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div/div/div/div[1]//button[@type='button']")

    # Options
    FLOOD_TENDERS = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/span/div/label/span")
    SDRF = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[2]/div/span/div/label/span")
    REPAIRS_RESTORATION = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[3]/div/span/div/label/span")
    IMMEDIATE_MEASURES = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[4]/div/span/div/label/span")
    OTHERS = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[5]/div/span/div/label/span")
    FUNDS_ALLOCATED_SDRF_SEC = (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[6]/div/span/div/label/span")
