from selenium.webdriver.common.by import By


class BhashiniLocators:
    """Selectors for the Bhashini translation widget (components/langSelect/lang-select.tsx).

    Only the first three belong to us. WIDGET and DROPDOWN_BUTTON are rendered
    by the third-party plugin from translation-plugin.bhashini.co.in, so they
    are kept apart from our own integration points.
    """

    # Ours: the mount point rendered by TranslateDropdown
    CONTAINER = (By.CSS_SELECTOR, ".bhashini-plugin-container")
    CONTAINER_TESTID = (By.CSS_SELECTOR, "[data-testid='bhashini-plugin-container']")

    # Ours: the script tag injected in useEffect (id set by the component)
    SCRIPT_BY_ID = (By.CSS_SELECTOR, "script#bhashini-translation-script")
    SCRIPT_BY_SRC = (
        By.CSS_SELECTOR,
        "script[src*='translation-plugin.bhashini.co.in']",
    )

    # Theirs: injected by the plugin once it loads
    WIDGET = (By.CSS_SELECTOR, "#bhashini-translation")
    WIDGET_IN_CONTAINER = (
        By.CSS_SELECTOR,
        ".bhashini-plugin-container #bhashini-translation",
    )
    DROPDOWN_BUTTON = (By.CSS_SELECTOR, ".bhashini-dropdown-btn")
