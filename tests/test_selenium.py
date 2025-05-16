import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSeleniumUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Make sure chromedriver is installed and in PATH
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_title_and_content(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.assertIn("SpotifyDash", self.driver.title)
        # Check if welcome message exists on the page
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Welcome to SpotifyDash", body)

if __name__ == "__main__":
    unittest.main() 