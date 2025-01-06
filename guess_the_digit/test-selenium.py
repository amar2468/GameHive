from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class SeleniumTestGuessTheDigit(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        
        # Navigate to the page where the user can fill the form, which will allow them to create a new account
        self.browser.get(f"{self.live_server_url}/sign_up")

        # Find the form elements that will allow a user to create a new account
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
        # Checks if there is a self.browser attribute and whether the value is NOT None. If this is the case, the quit() can be executed
        if hasattr(self, 'browser'):
            if self.browser:
                self.browser.quit()

    # We are checking to see if the required divs are hidden after the game is complete. This is because these divs are no longer necessary
    # as the user has finished the round.
    def test_easy_level_hints_enabled_div_visibility_after_attempts(self):
        self.browser.get(f"{self.live_server_url}/guess_the_digit/config")