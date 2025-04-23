import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()
options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920,1080")
# options.add_argument("start-maximized")
# options.add_experimental_option("detach", True)
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)
home_url = f"https://{os.getenv('HOME_URL_USERNAME')}:{os.getenv('HOME_URL_PASSWORD')}@{os.getenv('HOME_URL_4')}"
driver.get(home_url)
# driver.find_element(By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]").click()

