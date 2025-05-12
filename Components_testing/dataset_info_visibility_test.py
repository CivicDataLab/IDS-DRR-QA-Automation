import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from component_visibility_func import check_component_visibility

def dataset_info_visibility_test(driver):

    # moving to Datasets info page from datasets landing Page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/section/div[2]/div[2]/div[2]/div/div[1]/a"))
        )
        driver.find_element(By.XPATH, "/html/body/main/main/section/div[2]/div[2]/div[2]/div/div[1]/a").click()
        print("✅ DRIMS dataset hyperlink clicked")
    except:
        print("❌ DRIMS dataset hyperlink not found")
        return

    time.sleep(1)

    # Check if dataset info page top text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Home > Datasets > Dataset details text',
        selector="/html/body/main/main/div[1]/nav/ol",
        selector_type=By.XPATH
    )

    # Check if dataset details (name and description is visible)  text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Dataset names and description details text',
        selector="/html/body/main/main/div[2]/div/div[1]/div/div",
        selector_type=By.XPATH
    )

    # Check if Visualizations label text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Visualizations label text',
        selector="/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/span",
        selector_type=By.XPATH
    )

# Check if Visualizations description text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Visualizations description text',
        selector="/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/div",
        selector_type=By.XPATH
    )

    # Check if Metadata description text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Metadata  text',
        selector="/html/body/main/main/div[2]/div/div[2]/div[2]/div/div",
        selector_type=By.XPATH
    )

    # Check if downloadable resources description text is visible using XPath
    check_component_visibility(
        driver,
        component_name='downloadable resources text',
        selector="/html/body/main/main/div[2]/div/div[2]/div[1]/div[2]",
        selector_type=By.XPATH
    )
