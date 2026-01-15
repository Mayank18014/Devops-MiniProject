from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:5000")
    time.sleep(3)

    if "Product" in driver.page_source or "Scanner" in driver.page_source:
        print("UI Test Passed")
    else:
        raise Exception("UI Test Failed")

finally:
    driver.quit()
