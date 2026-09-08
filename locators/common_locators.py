from selenium.webdriver.common.by import By


class HeaderLocators:
    """Locators for header/navigation elements"""

    # Navigation links — text-based, survive DOM restructuring
    HOME_LINK = (By.XPATH, "//header//a[normalize-space()='Home']")
    ANALYTICS_LINK = (By.XPATH, "//header//a[normalize-space()='Analytics']")
    DATASETS_LINK = (By.XPATH, "//header//a[normalize-space()='Datasets']")
    ABOUT_US_LINK = (By.XPATH, "//header//a[normalize-space()='About us']")

    # Alternative locators — href-based fallback
    ANALYTICS_LINK_ALT = (By.XPATH, "//header//a[contains(@href,'/analytics')]")
    DATASETS_LINK_ALT = (By.XPATH, "//header//a[contains(@href,'/datasets')]")

    # Logo — alt text is "IDS-DRR home" (not "IDS-DRR Logo")
    HEADER_LOGO = (By.XPATH, "//header//img[@alt='IDS-DRR home']")

    # Language dropdown
    LANGUAGE_DROPDOWN = (By.XPATH, "//select[@name='lang-select']")



class FooterLocators:
    """Locators for footer elements"""

    # Footer logos.
    # IDS_DRR_LOGO removed 2026-09-08: the footer no longer carries a standalone
    # IDS-DRR image — confirmed against the live footer markup on prod and dev
    # (home, /datasets, /assam/analytics), which now renders only CDL + OCP plus
    # a Privacy Policy link. The header logo is untouched (see HEADER_LOGO above);
    # this was footer-only.
    CDL_LOGO = (By.XPATH, "//img[@alt='CivicDataLab Logo']")
    OCP_LOGO = (By.XPATH, "//body//main//footer//div//div//img[@alt='OCP Logo']")

    # Partner logos
    ROCKEFELLER_LOGO = (By.XPATH, "//img[@alt='Rockefeller Logo']")
    PJMF_LOGO = (By.XPATH, "//img[@alt='PJMF Logo']")
    ASDMA_LOGO = (By.XPATH, "//img[@alt='ASDMA Logo']")
    HPSDMA_LOGO = (By.XPATH, "//img[@alt='HPSDMA Logo']")

    # Social media
    SOCIAL_MEDIA_BUTTONS = (By.CLASS_NAME, "social-button")
