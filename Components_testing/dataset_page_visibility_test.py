import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from component_visibility_func import check_component_visibility

def dataset_page_visibility_test(driver):

    # moving to Datasets page from Analytics Page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[3]/div/span"))
        )
        driver.find_element(By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[3]/div/span").click()
        print("✅ Datasets button clicked")
    except:
        print("❌ Datasets button not found")
        return

    # Check if Main top Datasets text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Home > Datasets text',
        selector="/html/body/main/main/div/nav/ol",
        selector_type=By.XPATH
    )

    # Check if showing datasets and search bar elements  is visible using XPath
    check_component_visibility(
        driver,
        component_name='Showing no. of datasets and search bar',
        selector="/html/body/main/main/section/div[1]/div[1]",
        selector_type=By.XPATH
    )

    # Check if sort by text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Showing no. of datasets and search bar',
        selector="/html/body/main/main/section/div[1]/div[2]",
        selector_type=By.XPATH
    )

    # Check if filters section is visible using XPath
    check_component_visibility(
        driver,
        component_name='Showing filters section',
        selector="/html/body/main/main/section/div[2]/div[1]/div",
        selector_type=By.XPATH
    )

    # Check if datasets section is visible using XPath
    check_component_visibility(
        driver,
        component_name='Showing datasets section',
        selector="/html/body/main/main/section/div[2]/div[2]",
        selector_type=By.XPATH
    )
