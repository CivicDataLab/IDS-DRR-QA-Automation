from selenium.webdriver.common.by import By


class DatasetPageLocators:
    """Locators for Dataset listing page elements"""

    # Filters
    SOURCE_FILTER_DRIMS = (By.XPATH, "/html/body/main/main/section/div[2]/div[1]/div/div[2]/div[2]/div/div/div/div/fieldset/ul/li[4]/div/button")

    # Dataset cards
    FIRST_DATASET_CARD = (By.XPATH, "/html/body/main/main/section/div[2]/div[2]/div[2]/div/div[1]/a/div/div")

    # Search and sorting
    SEARCH_BAR = (By.CLASS_NAME, "search-input")
    SORT_DROPDOWN = (By.CLASS_NAME, "sort-dropdown")


class DatasetInfoPageLocators:
    """Locators for Dataset info/detail page elements"""

    # Action buttons
    VISIT_SOURCE_WEBSITE = (By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[1]/a/span[1]")
    GITHUB_REPO = (By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[2]/a/span[1]")
    SHARE_DATASET = (By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[3]/button")

    # Visualizations
    VISUALIZATION_1 = (By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div")
    # Button to switch to the next/alternate visualization (try div[3] then div[2] as fallback)
    VISUALIZATION_2_BUTTON = (By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[3]/button | /html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/button[last()]")
    # Back button to return to visualization 1
    VISUALIZATION_2_BACK_BUTTON = (By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/button | /html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/button[last()]")
    # Download/export button for the visualization chart
    VISUALIZATION_DOWNLOAD = (By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/button[2] | /html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/button[last()]")

    # Metadata
    CATEGORY_LINK = (By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div[8]/div/a")

    # Download buttons — anchor tags wrapping buttons (file download links), indexed by position.
    # Using main-relative XPath so they survive minor layout changes.
    DOWNLOAD_DATASET_1 = (By.XPATH, "(//main//a[.//button])[1]//button")
    DOWNLOAD_DATASET_2 = (By.XPATH, "(//main//a[.//button])[2]//button")
    DOWNLOAD_DATASET_3 = (By.XPATH, "(//main//a[.//button])[3]//button")
    DOWNLOAD_DATASET_4 = (By.XPATH, "(//main//a[.//button])[4]//button")
