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

    # Mobile hamburger toggle — nav links (Home/Analytics/...) aren't in the DOM
    # as visible elements below the tablet breakpoint until this is clicked;
    # confirmed live 2026-09-09 at 375x667.
    MOBILE_MENU_BUTTON = (By.XPATH, "//header//button[normalize-space()='Menu']")


class DisasterHubLocators:
    """Locators for the per-state disaster-type hub page (e.g. /en/<state>)

    dev.dataspace's Analytics nav now lands here first: a page of disaster-type
    cards (Flood, Heat, ...), each with an "Explore" link into that disaster's
    actual analytics dashboard (Map/Chart/Table views, state sidebar). prod does
    not have this hub yet and links straight to the dashboard — confirmed live
    2026-09-08. Only Flood has real data at the moment, so navigate_to_analytics()
    always takes the first Explore link.
    """

    EXPLORE_LINK = (By.XPATH, "(//a[normalize-space()='Explore'] | //button[normalize-space()='Explore'])[1]")


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
