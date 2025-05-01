import time

from selenium.webdriver.common.by import By
from component_visibility_func import check_component_visibility

def component_visibility_test(driver):
    time.sleep(3)
    #Check if Main top left logo in header is visible using XPath
    check_component_visibility(
        driver,
        component_name = 'logo',
        selector="//img[@alt='IDS-DRR Logo']",
        selector_type=By.XPATH
        )

    #Check if Home link in header is visible using XPath
    check_component_visibility(
        driver,
        component_name='Home',
        selector="/html/body/main/header/div/div[2]/div[1]/a[1]",
        selector_type=By.XPATH
        )

    # Check if Analytics link in header is visible using XPath
    check_component_visibility(
        driver,
        component_name='Analytics',
        selector="/html/body/main/header/div/div[2]/div[1]/a[2]",
        selector_type=By.XPATH
    )

    # Check if Datasets link in header is visible using XPath
    check_component_visibility(
        driver,
        component_name='Datasets',
        selector="/html/body/main/header/div/div[2]/div[1]/a[3]",
        selector_type=By.XPATH
    )

    # Check if About Us link in header is visible using XPath
    check_component_visibility(
        driver,
        component_name='About Us',
        selector="/html/body/main/header/div/div[2]/div[1]/a[4]",
        selector_type=By.XPATH
    )
    # Check if Language Dropdown in header is visible using XPath
    check_component_visibility(
        driver,
        component_name='Language Dropdown',
        selector="Select-module_Select__YceVe",
        selector_type=By.CLASS_NAME
    )
    # time.sleep(3)
    # Check if Homepage image is visible using XPath
    check_component_visibility(
        driver,
        component_name='Homepage Image',
        selector="/html/body/main/main/div/section[1]/div/img[1]",
        selector_type=By.CLASS_NAME
    )

    # Check if H2 text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Homepage-lower text',
        selector="/html/body/main/main/div/section[1]/div/span",
        selector_type=By.XPATH
    )

    # Check if Analytics Dashboard text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Analytics dashboard text',
        selector="/html/body/main/main/div/section[2]/div[1]/h2",
        selector_type=By.XPATH
    )

    # Check if Analytics Dashboard sub text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Analytics Dashboard sub text',
        selector="/html/body/main/main/div/section[2]/div[1]/span",
        selector_type=By.XPATH
    )


    # Check for visibility of the analytics board links.

    # Find all elements with a same class
    time.sleep(3)
    analytics_elements = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[2]/div[2]/div/div[2]/div")
    for element in enumerate(analytics_elements):
        check_component_visibility(
            driver,
            component_name='Analytics dashboard links',
            selector="/html/body/main/main/div/section[2]/div[2]/div/div[2]/div/div[1]/a/div/h3",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")


    # Check for visibility of dataset catalogs heading and subheadings.

    # Find all elements with a same class
    dataset_catalog = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[3]/div[1]")
    for element in enumerate(dataset_catalog):
        check_component_visibility(
            driver,
            component_name='Data Catalogs heading and subheadings',
            selector="/html/body/main/main/div/section[3]/div[1]",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")

    # Check for visibility of dataset catalogs links.

    # Find all elements with a same class
    dataset_catalog_links = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[3]/div[2]")
    for element in enumerate(dataset_catalog_links):
        check_component_visibility(
            driver,
            component_name='dataset catalogs links',
            selector="/html/body/main/main/div/section[3]/div[2]",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")

    # Check for visibility of Resources heading and subheading using Xpath.

    # Find all elements with a same class
    resource_heading = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[4]/div[1]")
    for element in enumerate(resource_heading):
        check_component_visibility(
            driver,
            component_name='Resources heading and subheading',
            selector="/html/body/main/main/div/section[4]/div[1]",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")

    # Check for visibility of Resources cards and metadata using Xpath.

    # Find all elements with a same class
    resource_cards = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[4]/div[2]/div")
    for element in enumerate(resource_cards):
        check_component_visibility(
            driver,
            component_name='cards and metadata',
            selector="/html/body/main/main/div/section[4]/div[2]/div",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")

    # Check for visibility of DataStories using Xpath.

    # Find all elements with a same class
    datastories_heading = driver.find_elements(By.XPATH, "/html/body/main/main/div/div/section/div[1]")
    for index, element in enumerate(datastories_heading):
        check_component_visibility(
            driver,
            component_name='DataStories heading',
            selector="/html/body/main/main/div/div/section/div[1]",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")

    # Check for visibility of DataStories cards using Xpath.

    # Find all elements with a same class
    datastories_cards = driver.find_elements(By.XPATH, "/html/body/main/main/div/div/section/div[2]/div")
    for index, element in enumerate(datastories_cards):
        check_component_visibility(
            driver,
            component_name='DataStories cards',
            selector="/html/body/main/main/div/div/section/div[2]/div",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")

    # Check for visibility of About IDS-DRR using Xpath.

    # Find all elements with a same class
    about_section = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[5]/div")
    for index, element in enumerate(about_section):
        check_component_visibility(
            driver,
            component_name='About Us section',
            selector="/html/body/main/main/div/section[5]/div",
            selector_type=By.XPATH
        )

        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")
    # Check for visibility of Partners Section using Xpath.

    # Find all elements with a same class
    partners_section = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[6]")
    for index, element in enumerate(partners_section):
        check_component_visibility(
            component_name='Partners Section',
            selector="/html/body/main/main/div/section[6]",
            selector_type=By.XPATH
        )
        # Optional: Get additional information about the element
        text = element.text
        print(f" Text: {text}")


        print("in the end now")
        return driver
