from selenium.webdriver.common.by import By


class HeaderLocators:
    """Locators for header/navigation elements"""

    # Navigation links
    HOME_LINK = (By.XPATH, "//a[@aria-label='Home']//span")
    ANALYTICS_LINK = (By.XPATH, "//a[@aria-label='Analytics']//span")
    DATASETS_LINK = (By.XPATH, "//a[@aria-label='Datasets']//span")
    ABOUT_US_LINK = (By.XPATH, "//a[@aria-label='About Us']//span")

    # Alternative locators using position (fallback)
    ANALYTICS_LINK_ALT = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]/div/span")
    DATASETS_LINK_ALT = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[3]/div/span")

    # Logo
    HEADER_LOGO = (By.XPATH, "//a[normalize-space()='']//img[@alt='IDS-DRR Logo']")

    # Language dropdown
    LANGUAGE_DROPDOWN = (By.ID, "language-select")


class FooterLocators:
    """Locators for footer elements"""

    # Footer logos
    IDS_DRR_LOGO = (By.XPATH, "//img[@alt='IDS-DRR logo']")
    CDL_LOGO = (By.XPATH, "//img[@alt='CDL logo']")
    OCP_LOGO = (By.XPATH, "//img[@alt='OCP logo']")

    # Partner logos
    ROCKEFELLER_LOGO = (By.XPATH, "//img[@alt='Rockefeller Foundation']")
    PJMF_LOGO = (By.XPATH, "//img[@alt='PJMF']")
    ASDMA_LOGO = (By.XPATH, "//img[@alt='ASDMA']")
    HPSDMA_LOGO = (By.XPATH, "//img[@alt='HPSDMA']")

    # Social media
    SOCIAL_MEDIA_BUTTONS = (By.CLASS_NAME, "social-button")
