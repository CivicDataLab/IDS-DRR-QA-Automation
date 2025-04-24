import os
from dotenv import load_dotenv
from selenium import webdriver

def load_driver():
    global driver, exceptions
    load_dotenv()
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument('--headless')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    if os.getenv('LOCAL') == 'false':
        driver = webdriver.Remote(os.getenv('REMOTE_LINK'), options=options)
    else:
        driver = webdriver.Chrome(options=options)
    return driver
