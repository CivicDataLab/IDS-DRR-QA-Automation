from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


def check_component_visibility(component_name, selector, selector_type=By.XPATH, timeout=10):
    try:

        # Wait for the element to be visible
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((selector_type, selector))
        )

        # Check if the element is displayed
        is_visible = element.is_displayed()

        if is_visible:
            print(f"✅ Component '{component_name}' is visible on the page")
        else:
            print(f"❌ Component '{component_name}' is not visible on the page")

        return is_visible

    except TimeoutException:
        print(f"❌ Component '{component_name}' not found within {timeout} seconds")
        return False
    except NoSuchElementException:
        print(f"❌ Component '{component_name}' not found on the page")
        return False
    except Exception as e:
        print(f"❌ Error checking component visibility: {e}")
        return False
    # finally:
        # Always close the browser
        # driver.quit()

