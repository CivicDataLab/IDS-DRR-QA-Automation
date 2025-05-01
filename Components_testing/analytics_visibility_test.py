import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from component_visibility_func import check_component_visibility

def analytics_visibility_test(driver):

    # moving to analytics page from homepage
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]/div/span"))
        )
        driver.find_element(By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]/div/span").click()
        print("✅ Analytics button clicked")
    except:
        print("❌ Analytics button not found")
        return

    # Check if Main top Analytics Dashboard text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Analytics Dashboard text',
        selector="/html/body/main/div/aside/div/div[1]/div[1]/span",
        selector_type=By.XPATH
    )

    # Check if State Selection dropdown is visible using XPath
    check_component_visibility(
        driver,
        component_name='State Selection Dropdown',
        selector="/html/body/main/div/aside/div/div[1]/div[2]",
        selector_type=By.XPATH
    )

    # Check if State Selection dropdown is visible using XPath
    check_component_visibility(
        driver,
        component_name='Indicators',
        selector="/html/body/main/div/aside/div/div[1]/div[3]",
        selector_type=By.XPATH
    )

    # Check for visibility of the analytics board links.
    time.sleep(2)

    # Check for visibility of the analytics board links.

    # Find all elements with a same class
    analytics_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]")
    for index, element in enumerate(analytics_indicators):
        check_component_visibility(
            driver,
            component_name='Hazard options',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]",
            selector_type=By.XPATH
        )

    # Check for visibility of the analytics board links.

    # Find all elements with a same class
    analytics_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]")
    for index, element in enumerate(analytics_indicators):
        check_component_visibility(
            driver,
            component_name='Exposure options',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]",
            selector_type=By.XPATH
        )

    # Check for visibility of the analytics board links.

    # Find all elements with a same class
    analytics_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]")
    for index, element in enumerate(analytics_indicators):
        check_component_visibility(
            driver,
            component_name='Vulnerability options',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]",
            selector_type=By.XPATH
        )

    # Check for visibility of the analytics board links.

    # Find all elements with a same class
    analytics_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]")
    for index, element in enumerate(analytics_indicators):
        check_component_visibility(
            driver,
            component_name='Government Response options',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]",
            selector_type=By.XPATH
        )

    #
    # Check for visibility of the Left menu board links.



