from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random

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

        time.sleep(3)

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

        time.sleep(10)

    def tearDown(self):
        # Checks if the browser is being used. If it is and this function is called, the browser will close.
        if hasattr(self, 'browser'):
            if self.browser:
                self.browser.quit()
    
    # This view will go through the process of playing the single player rock,paper,scissors game
    def test_single_player_rps_process(self):
        # Navigating to the single player rock,paper,scissors game
        self.browser.get(f"{self.live_server_url}/rock_paper_scissors/single_player_rps/")

        while True:
            # Get all the possible options from rock,paper,scissors game (which would be the rock,paper,scissor choices)
            rock_paper_scissors_options = self.browser.find_elements(By.CLASS_NAME, "carousel-item")

            # Find the next button, which will move through the different rock,paper,scissor choices
            next_button = self.browser.find_element(By.CLASS_NAME, "carousel-control-next")

            # We are generating a random number of clicks on the next button (ranging from 0-2), which will pick one of the options randomly
            no_of_clicks_on_next_button_random = random.randint(0, len(rock_paper_scissors_options) - 1)

            for _ in range(no_of_clicks_on_next_button_random):
                time.sleep(1)
                next_button.click()

            time.sleep(2)

            # Find the choice that the user chose on the screen
            active_rps_choice = self.browser.find_element(By.CLASS_NAME, "carousel-item.active")

            time.sleep(1)

            # Click on the choice that the user chose
            active_rps_choice.find_element(By.CLASS_NAME, "selected_rps").click()
            
            time.sleep(3)

            # Getting the modal element from the HTML template
            rps_end_of_game_info_modal = self.browser.find_element(By.ID, "rps_end_of_game_info_modal")

            time.sleep(2)

            # Trying to see if the modal is being displayed on screen - if it is, it means that the game is over and we can end our test
            if rps_end_of_game_info_modal.is_displayed():
                break