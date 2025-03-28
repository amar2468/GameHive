from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class SeleniumTestGuessTheDigit(LiveServerTestCase):
    def setUp(self):

        # Try/Except to install and start the browser, so that if it fails, an error message is displayed in the console.
        try:
            self.browser = webdriver.Chrome()
        except Exception as e:
            self.fail(f"Failed to start the browser: {e}")
        
        # Navigate to the page where the user can fill the form, which will allow them to create a new account
        self.browser.get(f"{self.live_server_url}/sign_up")

        # Find the form elements that will allow a user to create a new account
        first_name_field_sign_up = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "name"))
        )

        last_name_field_sign_up = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "surname"))
        )

        username_field_sign_up = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "username"))
        )

        email_field_sign_up = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "email"))
        )

        password_field_sign_up = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "password"))
        )

        submit_button_sign_up = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))
        )

        # We will clear the fields and then fill them in with the sign up information
        first_name_field_sign_up.clear()
        first_name_field_sign_up.send_keys("Joe")

        last_name_field_sign_up.clear()
        last_name_field_sign_up.send_keys("Bloggs")

        username_field_sign_up.clear()
        username_field_sign_up.send_keys("user45")

        email_field_sign_up.clear()
        email_field_sign_up.send_keys("user45@gmail.com")

        password_field_sign_up.clear()
        password_field_sign_up.send_keys("Strongpassword100!")
        
        # We are scrolling to the bottom of the page, so that the submit button can be clicked, to register the user
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.2)

        # Saving the current URL, so that we can compare it with the login URL (if the current URL saved is not the login URL,
        # we will be redirected to the login page)
        current_url = self.browser.current_url

        # Click the submit button, to register the user
        submit_button_sign_up.click()

        # Wait until the URL changes (indicating a new page)
        WebDriverWait(self.browser, 20).until(lambda driver: driver.current_url != current_url)

        # Navigate to the page where the user can fill the form, which will allow them to sign in
        self.browser.get(f"{self.live_server_url}/login")

        # Find the form elements that will allow a user to sign in to their account
        username_field_login = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "username"))
        )

        password_field_login = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "password"))
        )

        submit_button_login = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))
        )

        # We will clear the fields and then fill them in with the login information
        username_field_login.clear()
        username_field_login.send_keys("user45")
        
        password_field_login.clear()
        password_field_login.send_keys("Strongpassword100!")

        # Saving the current URL, so that we can compare it with the homepage URL (if the current URL saved is not the homepage URL,
        # we will be redirected to the login page)
        current_url = self.browser.current_url

        # Submit the form by pressing "Enter" on the keyboard
        submit_button_login.click()
        
        # Wait until the URL changes (indicating a new page)
        WebDriverWait(self.browser, 20).until(lambda driver: driver.current_url != current_url)
    
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
        game_difficulty = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "selected_level"))
        )

        are_hints_enabled = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "hints"))
        )

        start_guess_the_digit_game = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))
        )

        # Fill them in using the information below.
        game_difficulty.send_keys(level)
        are_hints_enabled.send_keys(hints)

        # Waiting for the button to submit your game choices to be clickable - click it once it is clickable
        WebDriverWait(self.browser, 20).until(
            expected_conditions.element_to_be_clickable((start_guess_the_digit_game))
        ).click()

        # Locate the button to play the game, which will appear in the modal that pops up and click it. This commences the game.
        WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.ID, "play_game"))
        ).click()

        number_of_rounds = no_of_rounds
        guess_range = level_guess_range

        for i in range(0, number_of_rounds):
            # Find the form elements which will simulate the game
            user_guess_field = WebDriverWait(self.browser, 20).until(
                expected_conditions.presence_of_element_located((By.NAME, "guess_number_input_field"))
            )

            submit_guess_button = WebDriverWait(self.browser, 20).until(
                expected_conditions.presence_of_element_located((By.ID, "guess_number_button"))
            )

            correct_number = WebDriverWait(self.browser, 20).until(
                expected_conditions.presence_of_element_located((By.ID, "correct_number"))
            )

            # Retrieving the correct number and converting it into an integer, so that we can compare it against the user guess
            correct_number = correct_number.get_attribute("value")
            correct_number = int(correct_number)

            # We are generating a random number (from 1-10) which will represent the user's guess & submitting the user guess
            guess_from_user = random.randint(1,guess_range)

            # Find the input field where the user submits their guess
            user_guess_field = WebDriverWait(self.browser, 20).until(
                expected_conditions.presence_of_element_located((By.NAME, "guess_number_input_field"))
            )

            # Clear the input field and enter the user guess
            user_guess_field.clear()
            user_guess_field.send_keys(guess_from_user)

            # Click the button to submit the user's guess
            WebDriverWait(self.browser, 20).until(
                expected_conditions.element_to_be_clickable((submit_guess_button))
            ).click()

            # If the user guess is correct, we want to break out of the for loop, as there is no need to 
            # continue tracking the guesses
            if guess_from_user == correct_number:
                break
        
        # Divs that will be tested, to see whether they are hidden after the game is done.
        guess_range_div = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.ID, hidden_div_level))
        )

        user_guess_field = WebDriverWait(self.browser, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, "guess_number_input_field"))
        )

        # If the div, that shows the range that the user can guess, is still visible, an error will be raised.
        if guess_range_div.is_displayed():
            raise Exception(
                f"The guess range div is visible when level = {level}, "
                f"and hints = {hints}, but should be hidden when the user ends the game."
            )
        
        # If it is hidden, no need to do anything as this is what we want.
        else:
            print(f"The guess range div is hidden for level = {level} and hints = {hints}, which is the desired behaviour!")
        
        # If the div, that allows the user to input a number, is still visible, an error will be raised.
        if user_guess_field.is_displayed():
            raise Exception(
                f"The input field is visible when level = {level}, and hints = {hints},"
                f"but should be hidden when the user ends the game."
            )
        
        # If it is hidden, no need to do anything as this is what we want.
        else:
            print(f"The input field is hidden for level = {level} and hint = {hints}, which is the desired behaviour!")

        # If the div, that allows the user to submit their guess, is still visible, an error will be raised.
        if user_guess_field.is_displayed():
            raise Exception(
                f"The submit button is visible for level = {level} and hints = {hints},"
                f"but should be hidden when the user ends the game."
            )
        
        # If it is hidden, no need to do anything as this is what we want.
        else:
            print(f"The submit button is hidden for level = {level} and hints = {hints}, which is the desired behaviour!")
        
        # If the hints were enabled, we want to check if the div that shows the hint is hidden at the end of the game.
        if hints == "yes":
            # We are extracting the div that shows the hint from the HTML template, to see whether it is visible or hidden.

            hint_div = WebDriverWait(self.browser, 20).until(
                expected_conditions.presence_of_element_located((By.ID, "hint_div"))
            )
            

            # If the div the shows the hint is visible, it will raise an exception and the test will fail.
            if hint_div.is_displayed():
                raise Exception(
                    f"The hint div is visible for level = {level}," 
                    f"but should be hidden when the user ends the game."
                )
            
            # If it is hidden, no need to do anything as this is what we want.
            else:
                print(f"The hint div is hidden for level = {level}, which is the desired behaviour!")

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