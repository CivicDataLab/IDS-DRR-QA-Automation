from selenium.webdriver.common.by import By


class ModuleAnalyticsLocators:
    """Selectors for /<state>/<module>/analytics and the /<state> hub (merged #530, #534)."""

    # Sidebar state picker. A native <select> named "State"; its options are
    # the states the module layout (#530) decided are available for the module.
    STATE_SELECT = (By.CSS_SELECTOR, "select[name='State']")
    STATE_OPTIONS = (By.CSS_SELECTOR, "select[name='State'] option")

    # Indicator heading above the map/chart/table. The class is a CSS-module
    # name (hashed suffix), so match on the stable prefix.
    INDICATOR_TITLE = (By.CSS_SELECTOR, "h2[class*='analyticsIndicatorTitle']")


class StateHubLocators:
    """Selectors for the per-state disaster-type hub (/<state>)."""

    MAIN = (By.TAG_NAME, "main")
    EXPLORE_LINKS = (By.XPATH, "//main//a[normalize-space()='Explore']")
