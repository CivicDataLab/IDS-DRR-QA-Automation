import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
exceptions = []
screenshot_dir = './screenshots/datasets'
ss_prefix = ""

def consumer_dataset_flow_test(driver):
    global ss_prefix
    # Create the directory if it doesn't exist
    os.makedirs(screenshot_dir, exist_ok=True)
    # Create the directory if it doesn't exist
    os.makedirs(screenshot_dir, exist_ok=True)

    # moving to Datasets page from homepage
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[3]/div/span"))
        )
        print("✅ Datasets button found")
    except:
        print("❌ Datasets button not found")
        return
    else:
        driver.find_element(By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[3]/div/span").click()
        print("✅ Datasets button clicked")

        time.sleep(4)
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'dataset_landing_page.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)


    # Clicking on DRIMS in source filter from Datasets listing page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/section/div[2]/div[1]/div/div[2]/div[2]/div/div/div/div/fieldset/ul/li[4]/div/button"))
        )
        print("✅ DRIMS checkbox Found")
    except:
        print("❌ DRIMS checkbox not found")
        return
    else:
        driver.find_element(By.XPATH, "/html/body/main/main/section/div[2]/div[1]/div/div[2]/div[2]/div/div/div/div/fieldset/ul/li[4]/div/button").click()
        print("✅ DRIMS checkbox clicked")
        time.sleep(4)
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'source_filter_applied.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)
        time.sleep(2)

    # Clicking on DRIMS dataset in Datasets listing page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/section/div[2]/div[2]/div[2]/div/div[1]/a/div/div"))
        )
        print("✅ DRIMS Dataset Found")
    except:
        print("❌ DRIMS Dataset not found")
        return
    else:
        driver.find_element(By.XPATH, "/html/body/main/main/section/div[2]/div[2]/div[2]/div/div[1]/a/div/div").click()
        print("✅ DRIMS Dataset clicked")
        time.sleep(4)
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'drims_dataset_info.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)
        time.sleep(2)

    # Clicking on Visit source website button in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[1]/a/span[1]"))
        )
        print("✅ Source website Found")
    except:
        print("❌ source website not found")
        return
    else:
        driver.find_element(By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[1]/a/span[1]").click()
        print("✅ source website clicked")
        time.sleep(4)
        driver.switch_to.alert.dismiss()
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'source_website_click.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)
        time.sleep(2)

    # Clicking on GitHub Repo website button in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[2]/a/span[1]"))
        )
        print("✅ GitHub Repo website Found")
    except:
        print("❌ GitHub Repo website not found")
        return
    else:
        driver.find_element(By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[2]/a/span[1]").click()
        print("✅ GitHub Repo website clicked")
        time.sleep(4)
        driver.switch_to.alert.dismiss()
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'github_repo_button_click.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)
        time.sleep(2)

    # Clicking on Share dataset button in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[3]/button/span/span/div/span[1]"))
        )
        print("✅ Share dataset button Found")
    except:
        print("❌ Share dataset button not found")
        return
    else:
        element.click()
        print("✅ Share dataset button clicked")
        time.sleep(4)
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'share_dataset_button.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/main/main/div[2]/div/div[1]/div/div/div[3]/div[3]/button/span/span/div/span[1]").click()


    # Clicking on Visualization in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div"))
        )
        print("✅ Visualization 1 Found")
    except:
        print("❌ Visualization 1 not found")
        return
    else:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(4)
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'demographic_damages_visualization.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)

    # Clicking on Alternate Visualization if any in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[3]/button"))
        )
        print("✅ Visualization 2 Found")
    except:
        print("❌ Visualization 2 not found")
        return
    else:
        element.click()
        time.sleep(4)
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'infra_damage_visualization.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)
        driver.find_element(By.XPATH,"/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/button").click()

    # Clicking on Visualization download button in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/button[2]"))
        )
        print("✅ Visualization download button Found")
    except:
        print("❌ Visualization download button not found")
        return
    else:
        time.sleep(2)
        element.click()
        time.sleep(4)
        # # Define the full path for the screenshot
        # screenshot_path = os.path.join(screenshot_dir, f'dataset_visualization.png')
        #
        # # Capture and save the screenshot
        # driver.save_screenshot(screenshot_path)

    # Clicking on Category link in metadata in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div[8]/div/a"))
        )
        print("✅ Category link Found")
    except:
        print("❌ Category link not found")
        return
    else:
        element.click()
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(4)
        # Define the full path for the screenshot
        screenshot_path = os.path.join(screenshot_dir, f'category_link_dataset_info.png')

        # Capture and save the screenshot
        driver.save_screenshot(screenshot_path)

    # Clicking on Download Dataset in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/a/button"))
        )
        print("✅ Download Dataset link Found")
    except:
        print("❌ Download Dataset link not found")
        return
    else:
        element.click()
        time.sleep(4)

    # Clicking on Download Dataset in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/a/button"))
        )
        print("✅ Download Dataset link Found")
    except:
        print("❌ Download Dataset link not found")
        return
    else:
        element.click()
        time.sleep(4)

    # Clicking on Download Dataset in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/a/button"))
        )
        print("✅ Download Dataset link Found")
    except:
        print("❌ Download Dataset link not found")
        return
    else:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        time.sleep(4)

        # Clicking on Download Dataset in Datasets info page
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/main/div[2]/div/div[2]/div[1]/div[2]/div/div[4]/div[2]/a/button"))
        )
        print("✅ Download Dataset link Found")
    except:
        print("❌ Download Dataset link not found")
        return
    else:
        element.click()