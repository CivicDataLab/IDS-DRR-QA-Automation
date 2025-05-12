import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from component_visibility_func import check_component_visibility
# team_members_xpath = ['/html/body/main/main/section[5]/div/div[3]/div[1]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[2]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[3]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[4]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[5]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[6]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[7]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[8]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[9]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[10]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[11]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[12]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[13]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[14]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[15]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[16]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[17]/img',
#                       '/html/body/main/main/section[5]/div/div[3]/div[18]/img',
#                       ]

def about_us_visibility_test(driver):

    # moving to About Us page from datasets landing Page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[4]/div/span"))
        )
        driver.find_element(By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[4]/div/span").click()
        print("✅ About Us hyperlink clicked")
    except:
        print("❌ About Us hyperlink not found")
        return

    time.sleep(1)

    # Check if About US and description text is visible using XPath
    check_component_visibility(
        driver,
        component_name='About US and description text',
        selector="/html/body/main/main/section[1]",
        selector_type=By.XPATH
    )

    # Check if Introducing IDS-DRR text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Introducing IDS-DRR text',
        selector="/html/body/main/main/section[2]",
        selector_type=By.XPATH
    )

    # Check if Collaborating partner text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Collaborating partner text',
        selector="/html/body/main/main/section[3]/div",
        selector_type=By.XPATH
    )
    # Check if ASDMA logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='ASDMA  logo',
        selector="/html/body/main/main/section[3]/div/div[1]/div[1]/img",
        selector_type=By.XPATH
    )
    # Check if ASDMA Website logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='ASDMA Website logo',
        selector="/html/body/main/main/section[3]/div/div[1]/div[1]/div/button[1]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if ASDMA Linkedin logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='ASDMA Linkedin logo',
        selector="/html/body/main/main/section[3]/div/div[1]/div[1]/div/button[2]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if ASDMA Twitter logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='ASDMA Twitter logo',
        selector="/html/body/main/main/section[3]/div/div[1]/div[1]/div/button[3]/span/span/img",
        selector_type=By.XPATH
    )

    # Check if HPSDMA logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='HPSDMA Website logo',
        selector="/html/body/main/main/section[3]/div/div[2]/div[1]/img",
        selector_type=By.XPATH
    )
    # Check if HPSDMA Website logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='HPSDMA Website logo',
        selector="/html/body/main/main/section[3]/div/div[2]/div[1]/div/button[1]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if HPSDMA Linkedin logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='HPSDMA Linkedin logo',
        selector="/html/body/main/main/section[3]/div/div[2]/div[1]/div/button[2]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if HPSDMA Twitter logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='HPSDMA Twitter logo',
        selector="/html/body/main/main/section[3]/div/div[2]/div[1]/div/button[3]/span/span/img",
        selector_type=By.XPATH
    )

    # Check if Supported By section text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Supported By section',
        selector="/html/body/main/main/section[4]/div",
        selector_type=By.XPATH
    )

    # Check if The Rockefeller Foundation logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='The Rockefeller Foundation  logo',
        selector="/html/body/main/main/section[4]/div/div[1]/div[1]/img",
        selector_type=By.XPATH
    )
    # Check if The Rockefeller Foundation website logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='The Rockefeller Foundation website logo',
        selector="/html/body/main/main/section[4]/div/div[1]/div[1]/div/button[1]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if The Rockefeller Foundation Linkedin logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='The Rockefeller Foundation Linkedin logo',
        selector="/html/body/main/main/section[4]/div/div[1]/div[1]/div/button[2]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if The Rockefeller Foundation Twitter logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='The Rockefeller Foundation Twitter logo',
        selector="/html/body/main/main/section[4]/div/div[1]/div[1]/div/button[3]/span/span/img",
        selector_type=By.XPATH
    )

    # Check if Patrick J. McGovern Foundation logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='Patrick J. McGovern Foundation logo',
        selector="/html/body/main/main/section[4]/div/div[2]/div[1]/img",
        selector_type=By.XPATH
    )
    # Check if Patrick J. McGovern Foundation Website logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='Patrick J. McGovern Foundation Website logo',
        selector="/html/body/main/main/section[4]/div/div[2]/div[1]/div/button[1]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if Patrick J. McGovern Foundation Linkedin logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='Patrick J. McGovern Foundation Linkedin logo',
        selector="/html/body/main/main/section[4]/div/div[2]/div[1]/div/button[2]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if Patrick J. McGovern Foundation Twitter logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='Patrick J. McGovern Foundation Twitter logo',
        selector="/html/body/main/main/section[4]/div/div[2]/div[1]/div/button[3]/span/span/img",
        selector_type=By.XPATH
    )


    # Check if Co-created by section text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Co-created by section text',
        selector="/html/body/main/main/section[5]/div",
        selector_type=By.XPATH
    )
    # Check if OCP logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='OCP logo',
        selector="/html/body/main/main/section[5]/div/div[1]/div[1]/img",
        selector_type=By.XPATH
    )
    # Check if OCP Website logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='OCP Website logo',
        selector="/html/body/main/main/section[5]/div/div[1]/div[1]/div/button[1]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if OCP Linkedin logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='OCP Linkedin logo',
        selector="/html/body/main/main/section[5]/div/div[1]/div[1]/div/button[2]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if OCP Twitter logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='OCP Twitter logo',
        selector="/html/body/main/main/section[5]/div/div[1]/div[1]/div/button[3]/span/span/img",
        selector_type=By.XPATH
    )

    # Check if CDL logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='CDL logo',
        selector="/html/body/main/main/section[5]/div/div[2]/div[1]/img",
        selector_type=By.XPATH
    )
    # Check if CDL Website logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='CDL Website logo',
        selector="/html/body/main/main/section[5]/div/div[2]/div[1]/div/button[1]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if CDL Linkedin logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='CDL Linkedin logo',
        selector="/html/body/main/main/section[5]/div/div[2]/div[1]/div/button[2]/span/span/img",
        selector_type=By.XPATH
    )
    # Check if CDL Twitter logo is visible using XPath
    check_component_visibility(
        driver,
        component_name='HPSDMA Twitter logo',
        selector="/html/body/main/main/section[5]/div/div[2]/div[1]/div/button[3]/span/span/img",
        selector_type=By.XPATH
    )

    # Check if Team members name & role text is visible using XPath
    check_component_visibility(
        driver,
        component_name='Team members name & role text',
        selector="/html/body/main/main/section[5]/div/div[3]",
        selector_type=By.XPATH
    )

    # Check if All Team members images are visible using XPath
    for index in range(1, 19):
        xpath = f"/html/body/main/main/section[5]/div/div[3]/div[{index}]/img"
        element = driver.find_element(By.XPATH, xpath)
        image_text = element.get_attribute("alt")
        check_component_visibility(
            driver,
            component_name=f"Team member ✅ Component '{image_text}'",
            selector=xpath,
            selector_type=By.XPATH
        )