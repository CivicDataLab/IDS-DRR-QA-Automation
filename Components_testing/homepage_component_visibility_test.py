from selenium.webdriver.common.by import By
from component_visibility_func import check_component_visibility

def homepage_component_visibility_test(driver):
    # Check if Main top left logo in header is visible using XPath
    check_component_visibility(
        driver,
        component_name='logo',
        selector="//img[@alt='IDS-DRR Logo']",
        selector_type=By.XPATH
    )

    # Check if Home link in header is visible using XPath
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

    # Check if Homepage image is visible using XPath
    check_component_visibility(
        driver,
        component_name='Homepage Image',
        selector="/html/body/main/main/div/section[1]/div/img[1]",
        selector_type=By.XPATH
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
    analytics_elements = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[2]/div[2]/div/div[2]/div")
    for index, element in enumerate(analytics_elements):
        check_component_visibility(
            driver,
            component_name='Analytics dashboard links',
            selector="/html/body/main/main/div/section[2]/div[2]/div/div[2]/div/div[1]/a/div/h3",
            selector_type=By.XPATH
        )

    # Check for visibility of dataset catalogs heading and subheadings.

    # Find all elements with a same class
    dataset_catalog = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[3]/div[1]")
    for index, element in enumerate(dataset_catalog):
        check_component_visibility(
            driver,
            component_name='Data Catalogs heading and subheadings',
            selector="/html/body/main/main/div/section[3]/div[1]",
            selector_type=By.XPATH
        )

    # Check for visibility of dataset catalogs links.

    # Find all elements with a same class
    dataset_catalog = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[3]/div[2]")
    for index, element in enumerate(dataset_catalog):
        check_component_visibility(
            driver,
            component_name='dataset catalogs links',
            selector="/html/body/main/main/div/section[3]/div[2]",
            selector_type=By.XPATH
        )

    # Check for visibility of Resources heading and subheading using Xpath.

    # Find all elements with a same class
    dataset_catalog = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[4]/div[1]")
    for index, element in enumerate(dataset_catalog):
        check_component_visibility(
            driver,
            component_name='Resources heading and subheading',
            selector="/html/body/main/main/div/section[4]/div[1]",
            selector_type=By.XPATH
        )

    # Check for visibility of Resources cards and metadata using Xpath.

    # Find all elements with a same class
    dataset_catalog = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[4]/div[2]/div")
    for index, element in enumerate(dataset_catalog):
        check_component_visibility(
            driver,
            component_name='cards and metadata',
            selector="/html/body/main/main/div/section[4]/div[2]/div",
            selector_type=By.XPATH
        )

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

    # Check for visibility of About IDS-DRR using Xpath.

    # Find all elements with a same class
    # check for IDS-DRR about section image visibility
    check_component_visibility(
        driver,
        component_name='About IDS-DRR Image',
        selector="/html/body/main/main/div/section[5]/div/img",
        selector_type=By.XPATH
    )
    about_section = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[5]/div")
    for index, element in enumerate(about_section):
        check_component_visibility(
            driver,
            component_name='About Us section',
            selector="/html/body/main/main/div/section[5]/div",
            selector_type=By.XPATH
        )


    # Check for visibility of Supporters Section using Xpath.

    # Checking  visibility for Supported By Section using Xpath.

    # Find all elements with a same class
    supported_section = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[6]/div/div[1]")
    for index, element in enumerate(supported_section):
        check_component_visibility(
            driver,
            component_name='Supported By Section',
            selector="/html/body/main/main/div/section[6]/div/div[1]",
            selector_type=By.XPATH
        )


    # checking the funder's logos
    check_component_visibility(
        driver,
        component_name='The Rockefeller foundation logo',
        selector="/html/body/main/main/div/section[6]/div/div[1]/div/img[1]",
        selector_type=By.XPATH
    )
    check_component_visibility(
        driver,
        component_name='The PJMF logo',
        selector="/html/body/main/main/div/section[6]/div/div[1]/div/img[2]",
        selector_type=By.XPATH
    )

    # Check for visibility of In collaboration with Section using Xpath.

    # Find all elements with a same class
    collab_section = driver.find_elements(By.XPATH, "/html/body/main/main/div/section[6]/div/div[2]")
    for index, element in enumerate(collab_section):
        check_component_visibility(
            driver,
            component_name='Partners Section',
            selector="/html/body/main/main/div/section[6]/div/div[2]",
            selector_type=By.XPATH
        )

    # checking the Partner's logos
    check_component_visibility(
        driver,
        component_name='ASDMA logo',
        selector="/html/body/main/main/div/section[6]/div/div[2]/div/img[1]",
        selector_type=By.XPATH
    )
    check_component_visibility(
        driver,
        component_name='HPSDMA logo',
        selector="/html/body/main/main/div/section[6]/div/div[2]/div/img[2]",
        selector_type=By.XPATH
    )
    # Check for visibility of Footer section using Xpath.

    # Find all elements with a same class
    footer_section = driver.find_elements(By.XPATH, "/html/body/main/footer")
    for index, element in enumerate(footer_section):
        check_component_visibility(
            driver,
            component_name='Footer Section',
            selector="/html/body/main/footer",
            selector_type=By.XPATH
        )

    # checking the Footer logos
    check_component_visibility(
        driver,
        component_name='IDS-DRR logo',
        selector="/html/body/main/footer/div[1]/img[1]",
        selector_type=By.XPATH
    )
    check_component_visibility(
        driver,
        component_name='Divider image',
        selector="/html/body/main/footer/div[1]/img[2]",
        selector_type=By.XPATH
    )
    check_component_visibility(
        driver,
        component_name='CDL Logo',
        selector="/html/body/main/footer/div[1]/div/img[1]",
        selector_type=By.XPATH
    )
    check_component_visibility(
        driver,
        component_name='OCP Logo',
        selector="/html/body/main/footer/div[1]/div/img[2]",
        selector_type=By.XPATH
    )

    return driver
