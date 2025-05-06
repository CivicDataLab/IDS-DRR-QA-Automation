import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from component_visibility_func import check_component_visibility

district_values = []

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

    # Check if the State Selection dropdown is visible using XPath
    check_component_visibility(
        driver,
        component_name='State Selection Dropdown',
        selector="/html/body/main/div/aside/div/div[1]/div[2]",
        selector_type=By.XPATH
    )

    # Check if the State Selection dropdown is visible using XPath
    check_component_visibility(
        driver,
        component_name='Indicators',
        selector="/html/body/main/div/aside/div/div[1]/div[3]",
        selector_type=By.XPATH
    )

    # Check for visibility of the Indicators on left menu.
    time.sleep(2)

    # Check for visibility of the Indicators on left menu.

    # Find all elements with a same class
    overall_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]")
    for index, element in enumerate(overall_indicators):
        check_component_visibility(
            driver,
            component_name='Overall Flood risk',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]",
            selector_type=By.XPATH
        )

    # Check for visibility of the Hazard Indicators.

    driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]").click()

    # Find all elements with a same class
    hazard_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]")
    for index, element in enumerate(hazard_indicators):
        check_component_visibility(
            driver,
            component_name='Hazard indicators',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]",
            selector_type=By.XPATH
        )

    # Check for visibility of the Exposure Indicators.
    driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div/div/div/div[1]").click()

    # Find all elements with a same class
    exposure_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]")
    for index, element in enumerate(exposure_indicators):
        check_component_visibility(
            driver,
            component_name='Exposure indicators',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]",
            selector_type=By.XPATH
        )


    # Check for visibility of the Vulnerability Indicators.
    driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div/div/div/div[1]").click()

    # Find all elements with a same class
    vulnerability_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]")
    for index, element in enumerate(vulnerability_indicators):
        check_component_visibility(
            driver,
            component_name='Vulnerability indicators',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]",
            selector_type=By.XPATH
        )

    # Check for visibility of the Government Response Indicators.
    driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[1]/div/div/div[1]").click()

    # Find all elements with a same class
    govt_response_indicators = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]")
    for index, element in enumerate(govt_response_indicators):
        check_component_visibility(
            driver,
            component_name='Government Response indicators',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]",
            selector_type=By.XPATH
        )

    # Check for visibility of the Actions section using XPath

    # Find all elements with a same class
    actions_section = driver.find_elements(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[2]")
    for index, element in enumerate(actions_section):
        check_component_visibility(
            driver,
            component_name='Actions Section',
            selector="/html/body/main/div/aside/div/div[1]/div[4]/div[2]",
            selector_type=By.XPATH
        )

    # Check if the Data last updated is visible using XPath
    check_component_visibility(
        driver,
        component_name='Data last updated',
        selector="/html/body/main/div/aside/div/div[2]/span",
        selector_type=By.XPATH
    )

    # Check for visibility of the Tabs sections using XPath

    # Find all elements with a same class
    tabs_section = driver.find_elements(By.XPATH, "/html/body/main/div/main/div/div[1]")
    for index, element in enumerate(tabs_section):
        check_component_visibility(
            driver,
            component_name='View Tabs elements',
            selector="/html/body/main/div/main/div/div[1]",
            selector_type=By.XPATH
        )

    # Check for visibility of the Map View Components using XPath

    # Find all elements with a same class
    map_view_section = driver.find_elements(By.XPATH, "//*[contains(@id, 'content-map')]")
    for index, element in enumerate(map_view_section):
        check_component_visibility(
            driver,
            component_name='All Map View components',
            selector="//*[contains(@id, 'content-map')]",
            selector_type=By.XPATH
        )

    # Check if the Select District dropdown label is visible using XPath
    check_component_visibility(
        driver,
        component_name='Select district dropdown label',
        selector="//*[contains(@id, 'content-map')]/div/div[1]/div/div/div[1]/div[1]/label",
        selector_type=By.XPATH
    )

    # Check for visibility of the Map View Select District Options using XPath

    # Find all elements with a same class
    select_district_section = driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div/div[1]/div/div/div[1]/div[2]/select")
    if select_district_section.tag_name.lower() == 'select':
    # Get all options in the dropdown
        dropdown_options = select_district_section.find_elements(By.TAG_NAME, "option")
        # print(f"Number of options in dropdown: {len(dropdown_options)}")
    #
        for index, element in enumerate(dropdown_options):
            district_values.append(element.text)

    print(district_values)

    select_district_section = driver.find_elements(By.XPATH, "//*[contains(@id, 'content-map')]/div/div[1]/div/div/div[1]")
    for index, element in enumerate(select_district_section):
        check_component_visibility(
            driver,
            component_name='Show District Options',
            selector="//*[contains(@id, 'content-map')]/div/div[1]/div/div/div[1]",
            selector_type=By.XPATH
        )


    # Check for visibility of the Map View Select Revenue Circle Options using XPath

    # Find all elements with a same class
    select_revenue_section = driver.find_elements(By.XPATH, "//*[contains(@id, 'content-map')]/div/div[1]/div/div/div[2]")
    for index, element in enumerate(select_revenue_section):
        check_component_visibility(
            driver,
            component_name='Show Revenue Circle Options',
            selector="//*[contains(@id, 'content-map')]/div/div[1]/div/div/div[2]",
            selector_type=By.XPATH
        )

    # Check for visibility of the Map View Select Month Options using XPath

    # Find all elements with a same class
    select_month_section = driver.find_elements(By.XPATH, "//*[contains(@id, 'content-map')]/div/div[1]/div/div/div[3]")
    for index, element in enumerate(select_month_section):
        check_component_visibility(
            driver,
            component_name='Show Month picker Options',
            selector="//*[contains(@id, 'content-map')]/div/div[1]/div/div/div[3]",
            selector_type=By.XPATH
        )

    # Check for visibility of the Chart View Components using XPath

    # Find all elements with a same class
    map_view_section = driver.find_elements(By.XPATH, "//*[contains(@id, 'content-chart')]")
    for index, element in enumerate(map_view_section):
        check_component_visibility(
            driver,
            component_name='All Chart View components',
            selector="//*[contains(@id, 'content-chart')]",
            selector_type=By.XPATH
        )

    # Check if the Select District dropdown label is visible using XPath
    check_component_visibility(
        driver,
        component_name='Select district dropdown label',
        selector="//*[contains(@id, 'content-map')]/div/div[1]/div/div[1]/div[1]/label",
        selector_type=By.XPATH
    )
