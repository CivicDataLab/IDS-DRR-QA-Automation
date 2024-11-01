from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
import report_gen
from dotenv import load_dotenv
import requests  # Add requests to check HTTP response codes


def load_driver():
    load_dotenv()
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    
    if os.getenv('LOCAL') == 'false':
        options.add_argument('--headless')  
        driver = webdriver.Remote(os.getenv('REMOTE_LINK'), options=options)
    else:
        options.add_argument("start-maximized")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
    return driver


# Construct the home URL using environment variables

driver = load_driver()
home_url = f"https://{os.getenv('HOME_URL_USERNAME')}:{os.getenv('HOME_URL_PASSWORD')}@{os.getenv('HOME_URL_4')}"
driver.get(home_url)
driver.get(os.getenv('URL'))

# Wait for the page to load completely
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href]")))

Site_Links = []
elems = driver.find_elements(By.XPATH, "//a[@href]")
for elem in elems:
    Site_Links.append(elem.get_attribute("href"))

data = {
    'title': 'comprehensive_links_and_validation_report',
    'time_stamp': datetime.now(),
    'urls_checked': {},
    'broken_links': [],
    'validation_issues': [],
}


def validate_page_elements(url):
    # Check if the link starts with "https://medium.com/"
    if url.startswith(os.getenv('MEDIUM_URL')):
        return  # Skip this link

    # Check if the page is accessible (status code 200)
    try:
        response = requests.head(url, allow_redirects=True)  # Use HEAD request to check status
        if response.status_code != 200:
            data['broken_links'].append(url)  # Add to broken links
            data['urls_checked'][url] = 'Broken'
            return  # Skip further validation if the link is broken
    except requests.RequestException:
        data['broken_links'].append(url)  # Add to broken links
        data['urls_checked'][url] = 'Broken'
        return

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "button")))

        # Find all buttons on the page
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            try:
                button_text = button.text if button.text else "No text"
                # Process button_text as needed
            except StaleElementReferenceException:
                continue

        # Find all text fields on the page
        text_fields = driver.find_elements(By.TAG_NAME, "input")
        for text_field in text_fields:
            try:
                if text_field.is_displayed():
                    # Process editable or visible text fields
                    pass
                else:
                    # Process non-editable or invisible text fields
                    pass
            except StaleElementReferenceException:
                continue

        # If no issues, mark as valid
        data['urls_checked'][url] = 'Valid'

    except Exception as e:
        data['validation_issues'].append(f"Issue with {url}: {str(e)}")


# Iterate through collected links and validate each one
for url in Site_Links:
    validate_page_elements(url)

# Generate report
report_gen.pdf_gen(data)

driver.quit()
