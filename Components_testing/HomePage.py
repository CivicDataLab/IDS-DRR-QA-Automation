from selenium import webdriver
import os
from dotenv import load_dotenv
from load_driver import load_driver
from component_visibility_test import component_visibility_test

import test_components

options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920,1080")
# options.add_argument("start-maximized")
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)
# home_url = f"https://{os.getenv('HOME_URL_USERNAME')}:{os.getenv('HOME_URL_PASSWORD')}@{os.getenv('HOME_URL_4')}"


# if __name__ == '__main__':
    # Load driver
driver = load_driver()
dev_url = os.getenv('HOME_URL_DEV')
driver.get(dev_url)
component_visibility_test()


