from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest
import time
import os

class UITest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://localhost:5000")
        time.sleep(3)

    def test_homepage(self):
        try:
            self.assertIn("Product", self.driver.page_source)
        except:
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot("screenshots/failure.png")
            raise

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
