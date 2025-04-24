from selenium.webdriver.common.by import By
from component_visibility_func import check_component_visibility
import load_driver

def component_visibility_test():
    #Check if Main top left logo in header is visible using XPath
    check_component_visibility(
        component_name = 'logo',
        selector="//img[@alt='IDS-DRR Logo']",
        selector_type=By.XPATH
        )

    #Check if Home link in header is visible using XPath
    check_component_visibility(
        component_name='Home',
        selector="/html/body/main/header/div/div[2]/div[1]/a[1]",
        selector_type=By.XPATH
        )

    # Check if Analytics link in header is visible using XPath
    check_component_visibility(
        component_name='Analytics',
        selector="/html/body/main/header/div/div[2]/div[1]/a[2]",
        selector_type=By.XPATH
    )

    # Check if Datasets link in header is visible using XPath
    check_component_visibility(
        component_name='Datasets',
        selector="/html/body/main/header/div/div[2]/div[1]/a[3]",
        selector_type=By.XPATH
    )

    # Check if About Us link in header is visible using XPath
    check_component_visibility(
        component_name='About Us',
        selector="/html/body/main/header/div/div[2]/div[1]/a[4]",
        selector_type=By.XPATH
    )
    # Check if Language Dropdown in header is visible using XPath
    check_component_visibility(
        component_name='Language Dropdown',
        selector="Select-module_Select__YceVe",
        selector_type=By.CLASS_NAME
    )
