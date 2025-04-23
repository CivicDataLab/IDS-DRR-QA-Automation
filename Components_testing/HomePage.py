from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from dotenv import load_dotenv


load_dotenv()
options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920,1080")
# options.add_argument("start-maximized")
# options.add_experimental_option("detach", True)

options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)
home_url = f"https://{os.getenv('HOME_URL_USERNAME')}:{os.getenv('HOME_URL_PASSWORD')}@{os.getenv('HOME_URL_4')}"
driver.get(home_url)

def check_component_visibility(selector, selector_type=By.XPATH, timeout=10):
    try:

        # Wait for the element to be visible
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((selector_type, selector))
        )

        # Check if the element is displayed
        is_visible = element.is_displayed()

        if is_visible:
            print(f"✅ Component '{selector}' is visible on the page")
        else:
            print(f"❌ Component '{selector}' is not visible on the page")

        return is_visible

    except TimeoutException:
        print(f"❌ Component '{selector}' not found within {timeout} seconds")
        return False
    except NoSuchElementException:
        print(f"❌ Component '{selector}' not found on the page")
        return False
    except Exception as e:
        print(f"❌ Error checking component visibility: {e}")
        return False
    finally:
        # Always close the browser
        driver.quit()


if __name__ == "__main__":

    # Example 1: Check if Main top left logo is visible using XPath
    check_component_visibility(
        selector="//img[@alt='IDS-DRR Logo']",
        selector_type=By.XPATH
        )
