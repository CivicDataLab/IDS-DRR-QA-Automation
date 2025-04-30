import time

from selenium import webdriver
import os
from dotenv import load_dotenv
from load_driver import load_driver
from component_visibility_func import check_component_visibility
from component_visibility_test import component_visibility_test

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)
# home_url = f"https://{os.getenv('HOME_URL_USERNAME')}:{os.getenv('HOME_URL_PASSWORD')}@{os.getenv('HOME_URL_4')}"


if __name__ == '__main__':
    # Load driver
    print("in the main now")
    driver = load_driver()
    # time.sleep(3)
    driver.get("https://drr.open-contracting.in/")
    component_visibility_test()


