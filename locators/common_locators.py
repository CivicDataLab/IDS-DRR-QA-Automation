from selenium.webdriver.common.by import By


class HeaderLocators:
    """Locators for header/navigation elements"""

    # Navigation links — absolute position-based paths that work reliably
    HOME_LINK = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[1]/div/span")
    ANALYTICS_LINK = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]/div/span")
    DATASETS_LINK = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[3]/div/span")
    ABOUT_US_LINK = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[4]/div/span")

    # Alternative locators using position (fallback)
    ANALYTICS_LINK_ALT = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]/div/span")
    DATASETS_LINK_ALT = (By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[3]/div/span")

    # Logo
    HEADER_LOGO = (By.XPATH, "//header//img[@alt='IDS-DRR Logo']")

    # Language dropdown
    LANGUAGE_DROPDOWN = (By.XPATH, "//select[@name='lang-select']")


class FooterLocators:
    """Locators for footer elements"""

    # Footer logos
    IDS_DRR_LOGO = (By.XPATH, "//body//main//footer//div//img[@alt='IDS-DRR Logo']")
    CDL_LOGO = (By.XPATH, "//img[@alt='CivicDataLab Logo']")
    OCP_LOGO = (By.XPATH, "//body//main//footer//div//div//img[@alt='OCP Logo']")

    # Partner logos
    ROCKEFELLER_LOGO = (By.XPATH, "//img[@alt='Rockefeller Logo']")
    PJMF_LOGO = (By.XPATH, "//img[@alt='PJMF Logo']")
    ASDMA_LOGO = (By.XPATH, "//img[@alt='ASDMA Logo']")
    HPSDMA_LOGO = (By.XPATH, "//img[@alt='HPSDMA Logo']")

    # Social media
    SOCIAL_MEDIA_BUTTONS = (By.CLASS_NAME, "social-button")
