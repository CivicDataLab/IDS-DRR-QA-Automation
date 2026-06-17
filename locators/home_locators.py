from selenium.webdriver.common.by import By


class HomePageLocators:
    # State quick-links section (aria-labelledby set in QuickLinks component)
    STATE_LINKS_SECTION = (By.XPATH, "//section[@aria-labelledby='home-analytics-heading']")

    # State links inside the carousel (any <a> pointing to an analytics route)
    ANALYTICS_LINKS = (By.XPATH, "//section[@aria-labelledby='home-analytics-heading']//a")
    FIRST_ANALYTICS_LINK = (By.XPATH, "(//section[@aria-labelledby='home-analytics-heading']//a)[1]")

    # Carousel navigation buttons
    CAROUSEL_NEXT = (By.XPATH, "//button[@aria-label='Next slide']")
    CAROUSEL_PREV = (By.XPATH, "//button[@aria-label='Previous slide']")

    # Dataset catalog — any link pointing to the datasets listing
    DATASET_CATALOG_SECTION = (By.XPATH, "//section[.//a[contains(@href,'datasets')]]")
    DATASETS_LINK_HOME = (By.XPATH, "(//a[contains(@href,'datasets') and not(contains(@href,'http'))])[1]")
