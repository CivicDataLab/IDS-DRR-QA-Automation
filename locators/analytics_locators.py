from selenium.webdriver.common.by import By


class AnalyticsPageLocators:
    """Locators for Analytics page elements"""

    # View toggle tabs — text is "Map View", "Chart View", "Table View"
    MAP_VIEW_BUTTON = (By.XPATH, "//button[normalize-space()='Map View']")
    CHART_VIEW_BUTTON = (By.XPATH, "//button[normalize-space()='Chart View']")
    TABLE_VIEW_BUTTON = (By.XPATH, "//button[normalize-space()='Table View']")

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
        return (By.XPATH, f"(//button[normalize-space()='Map View' or normalize-space()='Chart View' or normalize-space()='Table View'])[{index}]")


class HazardLocators:
    """Locators for Hazard section in Analytics"""

    EXPAND_COLLAPSE = (By.CSS_SELECTOR, "aside [aria-label='Hazard']")
    COLLAPSE_BUTTON = (By.CSS_SELECTOR, "aside [aria-label='Hazard']")

    # Indicators — aria-label matches the button text discovered from live UI (Assam baseline)
    TOTAL_MONTHLY_RAINFALL = (By.CSS_SELECTOR, "aside [aria-label='Total Monthly Rainfall']")
    SUM_INUNDATION_INTENSITIES = (By.CSS_SELECTOR, "aside [aria-label='Sum of inundation intensities']")
    MEAN_ELEVATION = (By.CSS_SELECTOR, "aside [aria-label='Mean Elevation']")


class ExposureLocators:
    """Locators for Exposure section in Analytics"""

    EXPAND_COLLAPSE = (By.CSS_SELECTOR, "aside [aria-label='Exposure']")
    COLLAPSE_BUTTON = (By.CSS_SELECTOR, "aside [aria-label='Exposure']")

    # Indicators
    TOTAL_HOUSEHOLDS = (By.CSS_SELECTOR, "aside [aria-label='Total Number of Households']")
    POPULATION = (By.CSS_SELECTOR, "aside [aria-label='Population']")
    ELDERLY_POPULATION = (By.CSS_SELECTOR, "aside [aria-label='Elderly population']")
    CHILDREN_POPULATION = (By.CSS_SELECTOR, "aside [aria-label='Children population']")


class VulnerabilityLocators:
    """Locators for Vulnerability section in Analytics"""

    EXPAND_COLLAPSE = (By.CSS_SELECTOR, "aside [aria-label='Vulnerability']")
    COLLAPSE_BUTTON = (By.CSS_SELECTOR, "aside [aria-label='Vulnerability']")

    # Infrastructure indicators
    HEALTH_CENTRES = (By.CSS_SELECTOR, "aside [aria-label='Number of Health Centres']")
    DOMESTIC_ELECTRICITY = (By.CSS_SELECTOR, "aside [aria-label='Average availablity of domestic electricity']")
    PIPED_WATER = (By.CSS_SELECTOR, "aside [aria-label='Percentage of households with piped water connection']")
    WITHOUT_SANITATION = (By.CSS_SELECTOR, "aside [aria-label='Percentage of households without sanitation facilities']")
    NUMBER_OF_SCHOOLS = (By.CSS_SELECTOR, "aside [aria-label='Number of Schools']")
    RAIL_LENGTH = (By.CSS_SELECTOR, "aside [aria-label='Length of rail in the region']")
    ROAD_LENGTH = (By.CSS_SELECTOR, "aside [aria-label='Length of Road']")
    NET_SOWN_AREA = (By.CSS_SELECTOR, "aside [aria-label='Net Sown Area']")
    MEAN_SEX_RATIO = (By.CSS_SELECTOR, "aside [aria-label='Mean Sex Ratio']")

    # Impact indicators
    POPULATION_AFFECTED = (By.CSS_SELECTOR, "aside [aria-label='Total Population Affected']")
    HUMAN_LIVES_LOST = (By.CSS_SELECTOR, "aside [aria-label='Human Lives Lost']")
    CROP_AREA_AFFECTED = (By.CSS_SELECTOR, "aside [aria-label='Total Crop Area Affected']")
    EMBANKMENTS_AFFECTED = (By.CSS_SELECTOR, "aside [aria-label='Total Number of Embankments Affected']")
    ROADS_DAMAGED = (By.CSS_SELECTOR, "aside [aria-label='Total Number of Roads Damaged']")
    BRIDGES_DAMAGED = (By.CSS_SELECTOR, "aside [aria-label='Number of Bridges damaged']")
    EMBANKMENTS_BREACHED = (By.CSS_SELECTOR, "aside [aria-label='Number of embankments breached']")


class GovtResponseLocators:
    """Locators for Government Response section in Analytics"""

    EXPAND_COLLAPSE = (By.CSS_SELECTOR, "aside [aria-label='Government Response']")
    COLLAPSE_BUTTON = (By.CSS_SELECTOR, "aside [aria-label='Government Response']")

    # Indicators — aria-label wording confirmed live 2026-09-09 (was stale: the
    # previous values, e.g. "Total Value of Flood Tenders", matched zero
    # elements). Not caught earlier because select_govt_response_option() was
    # never actually called by any test — dead, unexercised code.
    FLOOD_TENDERS = (By.CSS_SELECTOR, "aside [aria-label='Flood Tenders : Total Value']")
    SDRF = (By.CSS_SELECTOR, "aside [aria-label='Flood Tenders Under SDRF : Total value']")
    REPAIRS_RESTORATION = (By.CSS_SELECTOR, "aside [aria-label='Repairs and Restoration Flood Tenders : Total Value']")
    IMMEDIATE_MEASURES = (By.CSS_SELECTOR, "aside [aria-label='Immediate Measure Flood Tenders : Total Value']")
    OTHERS = (By.CSS_SELECTOR, "aside [aria-label='Other Flood Tenders : Total value of Non restoration and Preparedness tenders']")
    FUNDS_ALLOCATED_SDRF_SEC = (By.CSS_SELECTOR, "aside [aria-label='State Disaster Relief Funds Allocated District-wise During SEC meetings : Total Value']")


class ShareAndReportLocators:
    """Locators for the Share menu and Download Report action on the analytics dashboard"""

    SHARE_BUTTON = (By.XPATH, "//button[normalize-space()='Share']")
    DOWNLOAD_REPORT_BUTTON = (By.XPATH, "//button[normalize-space()='Download Report']")

    # Opens as a role=dialog popover — confirmed live 2026-09-09
    SHARE_DIALOG = (By.XPATH, "//*[@role='dialog']")
    SHARE_FACEBOOK = (By.XPATH, "//*[@role='dialog']//button[normalize-space()='Facebook']")
    SHARE_LINKEDIN = (By.XPATH, "//*[@role='dialog']//button[normalize-space()='LinkedIn']")
    SHARE_TWITTER = (By.XPATH, "//*[@role='dialog']//button[normalize-space()='Twitter']")
    SHARE_COPY_LINK = (By.XPATH, "//*[@role='dialog']//button[normalize-space()='Copy Link']")
