from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class SeleniumTestSinglePlayerRockPaperScissors(LiveServerTestCase):
    def setUp(self):
        # Controlling Chrome browser using Chrome driver
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        # Navigate to the sign up page, so that the user account can be created
        self.browser.get(f"{self.live_server_url}/sign_up")

        # Find the form elements in the sign_up page
        username_field_sign_up = self.browser.find_element(By.NAME, "username")
        email_field_sign_up = self.browser.find_element(By.NAME, "email")
        password_field_sign_up = self.browser.find_element(By.NAME, "password")
        submit_button_sign_up = self.browser.find_element(By.XPATH, '//button[@type="submit"]')

        # We will clear the fields and then fill them in with the sign up information
        username_field_sign_up.clear()
        username_field_sign_up.send_keys("user12")
        email_field_sign_up.clear()
        email_field_sign_up.send_keys("user12@gmail.com")
        password_field_sign_up.clear()
        password_field_sign_up.send_keys("Strongpassword100!")

        # Submit the form, in order to create the new account
        submit_button_sign_up.click()

        # Navigate to the page where the user can fill the form, which will allow them to sign in
        self.browser.get(f"{self.live_server_url}/login")

        # Find the form elements that will allow a user to sign in to their account
        username_field_login = self.browser.find_element(By.NAME, "username")
        password_field_login = self.browser.find_element(By.NAME, "password")
        submit_button_login = self.browser.find_element(By.XPATH, '//button[@type="submit"]')

        # We will clear the fields and then fill them in with the login information
        username_field_login.clear()
        username_field_login.send_keys("user12")
        password_field_login.clear()
        password_field_login.send_keys("Strongpassword100!")

        # Submit the form by pressing "Enter" on the keyboard
        submit_button_login.click()

    def tearDown(self):
        # Checks if the browser is being used. If it is and this function is called, the browser will close.
        if hasattr(self, 'browser'):
            if self.browser:
                self.browser.quit()
    
    def test_single_player_rps_process(self):
        pass