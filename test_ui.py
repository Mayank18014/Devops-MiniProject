import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class UITest(unittest.TestCase):

    def setUp(self):
        # Ensure screenshots folder exists
        os.makedirs("screenshots", exist_ok=True)

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)

    def test_homepage(self):
        self.driver.get("http://localhost:5000")

        # Take screenshot
        self.driver.save_screenshot("screenshots/homepage.png")

        self.assertIn("Product", self.driver.title)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
