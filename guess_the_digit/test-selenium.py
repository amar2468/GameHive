from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random

class SeleniumTestGuessTheDigit(LiveServerTestCase):
    def setUp(self):

        # Try/Except to install and start the browser, so that if it fails, an error message is displayed in the console.
        try:
            self.browser = webdriver.Chrome(ChromeDriverManager().install())
        except Exception as e:
            self.fail(f"Failed to start the browser: {e}")
        
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
    
    # This is a private helper function which will check if the divs are hidden at the end of the game. The level, number of rounds, and
    # whether the hints are enabled/disabled is passed to it and it verifies whether the divs are hidden, as they should be, at the end of the game.
    def _assert_divs_hidden(self, level, hints, no_of_rounds, level_guess_range, hidden_div_level):
        # Opens the config page for the "Guess the Digit" game, where the user can choose their level and whether hints are enabled
        self.browser.get(f"{self.live_server_url}/guess_the_digit/config")

        # Find the form elements that will allow the user to play the game using the information that the user supplied
        game_difficulty = self.browser.find_element(By.NAME, "selected_level")
        are_hints_enabled = self.browser.find_element(By.NAME, "hints")
        start_guess_the_digit_game = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
        
        # Locate the button to play the game, which will appear in the modal that pops up when user clicks on the submit button on the form. This is sort of a confirmation button before the game commences.
        modal_play_game_button = self.browser.find_element(By.ID, "play_game")

        # Fill them in using the information below.
        game_difficulty.send_keys(level)
        are_hints_enabled.send_keys(hints)
        time.sleep(3)

        # Submit the form, so that the game can commence.
        start_guess_the_digit_game.click()
        modal_play_game_button.click()

        number_of_rounds = no_of_rounds
        guess_range = level_guess_range

        for i in range(0, number_of_rounds):
            # Find the form elements which will simulate the game
            user_guess_field = self.browser.find_element(By.NAME, "guess_number_input_field")
            submit_guess_button = self.browser.find_element(By.XPATH, '//button[@type="submit"]')

            # We are generating a random number (from 1-10) which will represent the user's guess & submitting the user guess
            guess_from_user = random.randint(1,guess_range)
            user_guess_field.clear()
            user_guess_field.send_keys(guess_from_user)
            submit_guess_button.click()

            # For the first round, we will take what the correct number is and store it in a variable
            if i == 0:
                # Extract the correct number for this game, so that it can be compared against the user guess
                correct_number = self.browser.find_element(By.ID, "correct_number")
                correct_number = correct_number.get_attribute("value")
                correct_number = int(correct_number)

            # If the user guess is correct, we want to break out of the for loop, as there is no need to continue tracking the guesses
            if guess_from_user == correct_number:
                break
        
        # Divs that will be tested, to see whether they are hidden after the game is done.
        guess_range_div = self.browser.find_element(By.ID, hidden_div_level)
        guess_number_input_field = self.browser.find_element(By.ID, "guess_number_input_field")
        guess_number_button = self.browser.find_element(By.ID, "guess_number_button")

        # If the div, that shows the range that the user can guess, is still visible, an error will be raised.
        if guess_range_div.is_displayed():
            raise Exception(
                f"The guess range div is visible when level = {game_difficulty}, "
                f"and hints = {are_hints_enabled}, but should be hidden when the user ends the game."
            )
        
        # If it is hidden, no need to do anything as this is what we want.
        else:
            print(f"Hidden for level = {game_difficulty} and hints = {are_hints_enabled}")
        
        # If the div, that allows the user to input a number, is still visible, an error will be raised.
        if guess_number_input_field.is_displayed():
            raise Exception(
                f"The input field is visible when level = {game_difficulty}, and hints = {are_hints_enabled},"
                f"but should be hidden when the user ends the game."
            )
        
        # If it is hidden, no need to do anything as this is what we want.
        else:
            print(f"Hidden for level = {game_difficulty} and hint = {are_hints_enabled}")

        # If the div, that allows the user to submit their guess, is still visible, an error will be raised.
        if guess_number_button.is_displayed():
            raise Exception(
                f"The submit button is visible for level = {game_difficulty} and hints = {are_hints_enabled},"
                f"but should be hidden when the user ends the game."
            )
        
        # If it is hidden, no need to do anything as this is what we want.
        else:
            print(f"Hidden for level = {game_difficulty} and hints = {are_hints_enabled}")
        
        # If the hints were enabled, we want to check if the div that shows the hint is hidden at the end of the game.
        if hints == "yes":
            # We are extracting the div that shows the hint from the HTML template, to see whether it is visible or hidden.
            hint_div = self.browser.find_element(By.ID, "hint_div")

            # If the div the shows the hint is visible, it will raise an exception and the test will fail.
            if hint_div.is_displayed():
                raise Exception(
                    f"The hint div is visible for level = {game_difficulty}," 
                    f"but should be hidden when the user ends the game."
                )
            
            # If it is hidden, no need to do anything as this is what we want.
            else:
                print(f"Hidden for level = {game_difficulty}")

    # We are checking to see if the required divs are hidden after the game is complete. This is because these divs are no longer necessary
    # as the user has finished the game. Below are individual tests that verify this, based on factors such as different levels, hints enabled, etc...
    
    # Testing for easy level and hints enabled. We are calling the function which will test if the divs are hidden at the end of the game.
    def test_easy_level_hints_enabled_div_visibility_after_attempts(self):
        self._assert_divs_hidden("easy", "yes", 2, 10, "easy_level_div")

    # Testing for easy level and hints disabled. We are calling the function which will test if the divs are hidden at the end of the game.
    def test_easy_level_hints_disabled_div_visibility_after_attempts(self):
        self._assert_divs_hidden("easy", "no", 4, 10, "easy_level_div")

    # Testing for medium level and hints enabled. We are calling the function which will test if the divs are hidden at the end of the game.
    def test_medium_level_hints_enabled_div_visibility_after_attempts(self):
        self._assert_divs_hidden("medium", "yes", 5, 50, "medium_level_div")

    # Testing for medium level and hints disabled. We are calling the function which will test if the divs are hidden at the end of the game.
    def test_medium_level_hints_disabled_div_visibility_after_attempts(self):
        self._assert_divs_hidden("medium", "no", 10, 50, "medium_level_div")
    
    # Testing for hard level and hints enabled. We are calling the function which will test if the divs are hidden at the end of the game.
    def test_hard_level_hints_enabled_div_visibility_after_attempts(self):
        self._assert_divs_hidden("hard", "yes", 11, 100, "hard_level_div")
    
    # Testing for hard level and hints disabled. We are calling the function which will test if the divs are hidden at the end of the game.
    def test_hard_level_hints_disabled_div_visibility_after_attempts(self):
        self._assert_divs_hidden("hard", "no", 20, 100, "hard_level_div")