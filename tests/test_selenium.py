import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


class TestUserInteractions(unittest.TestCase):
    def setUp(self):
        if not os.path.exists("tests/screenshots"):
            os.makedirs("tests/screenshots")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:5000"
        self.driver.get(self.base_url)

    def tearDown(self):
        if hasattr(self, "driver") and self.driver:
            self.driver.save_screenshot(
                f"tests/screenshots/test_failure_{time.time()}.png"
            )
            self.driver.quit()

    def test_login_flow(self):
        """Test user login process"""
        try:
            # Click login button
            login_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a.border-2.border-green-500[href*='login']")
                )
            )
            login_link.click()

            # Verify we're on login page
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-4xl"))
            )
            assert "Sign In" in self.driver.page_source

            # Find form elements using WTForms generated IDs
            email_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            remember_me = self.driver.find_element(By.ID, "remember_me")
            submit_button = self.driver.find_element(By.ID, "submit")

            # Fill form
            email_input.send_keys("test@gmail.com")
            password_input.send_keys("test111")
            remember_me.click()

            # Submit form
            submit_button.click()

            # Verify successful login by checking for My account link
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a.border-2.border-green-500[href*='profile']")
                )
            )

        except Exception as e:
            self.driver.save_screenshot(
                f"tests/screenshots/login_failure_{time.time()}.png"
            )
            raise e

    def test_registration_flow(self):
        """Test user registration"""
        try:
            # Go to login page first
            login_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a.border-2.border-green-500[href*='login']")
                )
            )
            login_link.click()

            # Click register link
            register_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='register']"))
            )
            register_link.click()

            # Verify we're on register page
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-4xl"))
            )
            assert "Register" in self.driver.page_source

            # Find form elements using WTForms generated IDs
            username_input = self.driver.find_element(By.ID, "username")
            email_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            password2_input = self.driver.find_element(By.ID, "password2")
            submit_button = self.driver.find_element(By.ID, "submit")

            # Generate unique username/email using timestamp
            timestamp = int(time.time())
            username_input.send_keys(f"newuser_{timestamp}")
            email_input.send_keys(f"new{timestamp}@example.com")
            password_input.send_keys("password123")
            password2_input.send_keys("password123")

            # Submit form
            submit_button.click()

            # Wait for success message or redirect
            WebDriverWait(self.driver, 10).until(
                lambda driver: "account has been created" in driver.page_source.lower()
                or "sign in" in driver.page_source.lower()
            )

        except Exception as e:
            self.driver.save_screenshot(
                f"tests/screenshots/register_failure_{time.time()}.png"
            )
            raise e

    def test_registration_validation(self):
        """Test registration form validation"""
        try:
            # Navigate to register page
            self.driver.get(f"{self.base_url}/auth/register")

            # Find form elements
            username_input = self.driver.find_element(By.ID, "username")
            email_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            password2_input = self.driver.find_element(By.ID, "password2")
            submit_button = self.driver.find_element(By.ID, "submit")

            # Test password mismatch
            username_input.send_keys("testuser")
            email_input.send_keys("test@example.com")
            password_input.send_keys("password123")
            password2_input.send_keys("different123")
            submit_button.click()

            # Check for error message
            WebDriverWait(self.driver, 10).until(
                lambda driver: "passwords must match" in driver.page_source.lower()
            )

        except Exception as e:
            self.driver.save_screenshot(
                f"tests/screenshots/validation_failure_{time.time()}.png"
            )
            raise e

    def test_form_styles(self):
        """Test form styling classes"""
        try:
            self.driver.get(f"{self.base_url}/auth/login")

            # Check for Tailwind classes
            form = self.driver.find_element(By.TAG_NAME, "form")
            assert "flex" in form.get_attribute("class")
            assert "flex-col" in form.get_attribute("class")

            # Check form control styling
            email_input = self.driver.find_element(By.ID, "email")
            assert "form-control" in email_input.get_attribute("class")

            # Check button styling
            submit_button = self.driver.find_element(By.ID, "submit")
            assert "btn" in submit_button.get_attribute("class")

        except Exception as e:
            self.driver.save_screenshot(
                f"tests/screenshots/style_failure_{time.time()}.png"
            )
            raise e

    def wait_for_element(self, by, value, timeout=10):
        """Helper method to wait for element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            self.driver.save_screenshot(
                f"tests/screenshots/wait_failure_{time.time()}.png"
            )
            raise e

    def login(self):
        """Helper method to log in"""
        try:
            # Check if already logged in
            try:
                profile_link = self.driver.find_element(
                    By.CSS_SELECTOR, "a.border-2.border-green-500[href*='profile']"
                )
                if profile_link.is_displayed():
                    return  # Already logged in
            except:
                pass  # Not logged in, continue with login process

            # Go to login page
            self.driver.get(f"{self.base_url}/auth/login")
            time.sleep(2)  # Wait for page load

            # Find elements by name attribute
            email_input = self.wait_for_element(By.NAME, "email")
            password_input = self.wait_for_element(By.NAME, "password")
            submit_button = self.wait_for_element(
                By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
            )

            # Fill and submit form
            email_input.send_keys("test@example.com")
            password_input.send_keys("password123")
            submit_button.click()

            # Wait for login to complete
            self.wait_for_element(
                By.CSS_SELECTOR, "a.border-2.border-green-500[href*='profile']"
            )

        except Exception as e:
            print(f"Login failed: {str(e)}")
            self.driver.save_screenshot("tests/screenshots/login_failure.png")
            raise

    def test_upload_page(self):
        """Test upload page functionality and instructions"""
        try:
            # Login first
            self.login()
            # Navigate to upload page
            self.driver.get(f"{self.base_url}/account/upload")

            # Check page title and description
            title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "p.text-4xl.font-extrabold")
                )
            )
            assert "Upload Your Streaming History" in title.text

            # Check file input elements
            file_input = self.driver.find_element(By.ID, "fileInput")
            file_label = self.driver.find_element(By.ID, "fileLabel")
            upload_button = self.driver.find_element(By.ID, "upload-btn")
            status_div = self.driver.find_element(By.ID, "status")

            # Verify initial state
            assert "hidden" in file_input.get_attribute("class")
            assert "Choose a file" in file_label.text
            assert "Upload" in upload_button.text

            # Check instruction sections
            instruction_sections = [
                "How to Get Your Streaming History from Spotify?",
                "1. Request Your Data from Spotify",
                "2. Confirm Your Request",
                "3. Wait for Your Data",
                "4. Download and Extract the Files",
            ]

            for section in instruction_sections:
                assert section in self.driver.page_source

        except Exception as e:
            self.driver.save_screenshot(
                f"tests/screenshots/upload_failure_{time.time()}.png"
            )
            raise e


if __name__ == "__main__":
    unittest.main()
