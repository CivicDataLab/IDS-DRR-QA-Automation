import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

exceptions = []
screenshot_dir = './screenshots/datasets'

def consumer_dataset_flow_test(driver):
    # Create the directory if it doesn't exist
    os.makedirs(screenshot_dir, exist_ok=True)