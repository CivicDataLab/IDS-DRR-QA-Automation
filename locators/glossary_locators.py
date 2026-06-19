from selenium.webdriver.common.by import By


class GlossaryLocators:
    # Search input — name="search" from GlossaryClient SearchInput
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
    SEARCH_CLEAR_BUTTON = (By.XPATH, "//input[@name='search']//following::button[1]")

    # Letter-grouped sections — each letter group is a <section> containing accordion items
    LETTER_SECTIONS = (By.XPATH, "//main//section[.//button[@data-state]]")

    # Accordion trigger buttons (one per term)
    TERM_TRIGGERS = (By.XPATH, "//button[@data-state='closed' or @data-state='open']")
    FIRST_TERM_TRIGGER = (By.XPATH, "(//button[@data-state='closed' or @data-state='open'])[1]")

    # Empty state message (shown when no terms match search)
    EMPTY_STATE = (By.XPATH, "//div[.//p[contains(@class,'text-')] and not(.//button[@data-state])]")

    # Tag filter pills
    TAG_FILTERS = (By.XPATH, "//div[contains(@class,'flex gap-2')]//div[contains(@class,'cursor-pointer')]")
