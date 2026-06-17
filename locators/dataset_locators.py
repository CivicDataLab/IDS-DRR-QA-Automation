from selenium.webdriver.common.by import By


class DatasetPageLocators:
    """Locators for Dataset listing page elements"""

    # Filters — fieldset#Source contains button[role="checkbox"] items (no native checkboxes)
    # HPSDMA is a confirmed live source in the current dataset catalogue
    SOURCE_FILTER_HPSDMA = (By.CSS_SELECTOR, "fieldset#Source button[value='HPSDMA']")

    # Dataset cards — anchor tags linking to individual dataset UUIDs (exclude listing/query links)
    FIRST_DATASET_CARD = (By.XPATH, "(//main//a[contains(@href, '/en/datasets/') and not(contains(@href, '?'))])[1]")

    # Search — SearchInput component renders with name="Search"
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='Search']")
    # Submit button immediately after the search input in the DOM
    SEARCH_SUBMIT_BUTTON = (By.XPATH, "//input[@name='Search']/following::button[1]")

    # Sort — Select component renders with name="select"; options: Recent / Alphabetical
    SORT_SELECT = (By.CSS_SELECTOR, "select[name='select']")

    # Pagination — page-size select has an empty name attribute; it's a native <select> with opacity:0
    PAGINATION_PAGE_SIZE_SELECT = (By.XPATH, "(//select[@name=''])[1]")
    # Navigation buttons in the pagination footer (bg-baseGraySlateSolid3 bar); order: First, Prev, Next, Last.
    # These only render when there is more than one page of results.
    PAGINATION_NEXT_BUTTON = (By.XPATH, "(//div[contains(@class,'bg-baseGraySlateSolid3')]//button)[3]")
    PAGINATION_PREV_BUTTON = (By.XPATH, "(//div[contains(@class,'bg-baseGraySlateSolid3')]//button)[2]")
    PAGINATION_FIRST_BUTTON = (By.XPATH, "(//div[contains(@class,'bg-baseGraySlateSolid3')]//button)[1]")
    PAGINATION_LAST_BUTTON = (By.XPATH, "(//div[contains(@class,'bg-baseGraySlateSolid3')]//button)[4]")


class DatasetInfoPageLocators:
    """Locators for Dataset info/detail page elements"""

    # Action buttons — text-based so they survive DOM restructuring
    VISIT_SOURCE_WEBSITE = (By.XPATH, "//a[normalize-space()='Visit Source Website']")
    GITHUB_REPO = (By.XPATH, "//a[normalize-space()='GitHub Repository']")
    SHARE_DATASET = (By.XPATH, "//button[normalize-space()='Share dataset']")

    # Visualizations — chart widgets (may not exist on all datasets; tests are marked xfail)
    VISUALIZATION_1 = (By.XPATH, "//main//div[contains(@class,'recharts') or contains(@class,'Visualization') or contains(@class,'chart')]")
    VISUALIZATION_2_BUTTON = (By.XPATH, "//main//button[contains(@class,'visualization') or @aria-label='Next visualization' or @aria-label='Switch visualization']")
    VISUALIZATION_2_BACK_BUTTON = (By.XPATH, "//main//button[contains(@aria-label,'Previous') or contains(@aria-label,'Back')]")
    VISUALIZATION_DOWNLOAD = (By.XPATH, "//main//button[@aria-label='Download chart' or @aria-label='Export' or (contains(@class,'download') and ancestor::*[contains(@class,'chart') or contains(@class,'visual')])]")

    # Metadata
    CATEGORY_LINK = (By.XPATH, "(//a[contains(@href, 'categories=')])[1]")

    # Download buttons — anchors pointing directly to the download API
    DOWNLOAD_DATASET_1 = (By.XPATH, "(//main//a[contains(@href, '/api/download/resource/')])[1]")
    DOWNLOAD_DATASET_2 = (By.XPATH, "(//main//a[contains(@href, '/api/download/resource/')])[2]")
    DOWNLOAD_DATASET_3 = (By.XPATH, "(//main//a[contains(@href, '/api/download/resource/')])[3]")
    DOWNLOAD_DATASET_4 = (By.XPATH, "(//main//a[contains(@href, '/api/download/resource/')])[4]")
