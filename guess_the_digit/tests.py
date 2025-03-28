from django.test import TestCase, Client
from .forms import GuessTheNumberInputForm
from django.urls import reverse
from unittest.mock import patch
from gamehive.models import CustomUser,GameUserProfile

# Base class contains the user sign up & login. We set up the test user, which will be used in each individual unit/integration test
class BaseTestCase(TestCase):
    def setUp(self):
        # Create the test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            first_name='test',
            last_name='user',
            email='testuser@gmail.com',
            password='Password34*',
            account_type="user"
        )

        # Initialising the client
        self.client = Client()

        # Login with the test user credentials from above
        self.client.login(username='testuser', password='Password34*')

# Unit test for "Guess the Digit" game - This class contains two tests - testing valid input & testing invalid input

class GuessTheDigitUnitTestCase(BaseTestCase):
    # Checks whether the form submission (guessing a number) will be valid or not. Takes the user guess and whether we want it to
    # assertTrue or assertFalse. assertFalse is the default, unless otherwise specified.
    def check_form_validity(self, guess_number_input_field, assert_type=False):
        # Takes in whatever data was passed by the individual test case methods
        data = {
            'guess_number_input_field' : guess_number_input_field
        }

        # Take the input and validate it using the django form
        form = GuessTheNumberInputForm(data=data)

        if assert_type == True:
            # Check whether the form is valid, which it should be
            self.assertTrue(form.is_valid())
        else:
            # Check whether the form is valid, which it shouldn't be
            self.assertFalse(form.is_valid())

    # This method will test valid input and whether the form is deemed to be valid (as expected)
    def testing_valid_input(self):
        # Creating a variable to store a valid number for the "Guess the Digit" game.
        guess_number_input_field = 4
        assert_type = True

        # Calling the method to check whether the form is valid
        self.check_form_validity(guess_number_input_field, assert_type)
    
    # Method to test if an empty string is allowed to be submitted as a guess
    def test_empty_string_character_input(self):
        # Creating a variable to store an invalid character for the "Guess the Digit" game.
        guess_number_input_field = ''

        # Calling the method to check whether the form is valid
        self.check_form_validity(guess_number_input_field)
    
    # Method to test if letters are allowed to be submitted as a guess
    def test_letters_character_input(self):
        # Testing letters in the input field, instead of integers
        guess_number_input_field = 'a'

        # Calling the method to check whether the form is valid
        self.check_form_validity(guess_number_input_field)
    
    # Method to test if special characters are allowed to be submitted as a guess
    def test_special_characters_input(self):
        # Testing special characters in the input field
        guess_number_input_field = '!*!*!*!*!*'

        # Calling the method to check whether the form is valid
        self.check_form_validity(guess_number_input_field)
    
    # Method to test if spaces are allowed to be submitted as a guess
    def test_spaces_as_character_input(self):
        # Testing spaces between numbers in the input field
        guess_number_input_field = '12 2'

        # Calling the method to check whether the form is valid
        self.check_form_validity(guess_number_input_field)

# Integration test for "Guess the Digit" game

class GuessTheDigitIntegrationTestCase(BaseTestCase):
    def create_user_profile(self):
        # Delete the user with the username "testuser" if they already exist
        GameUserProfile.objects.filter(user__username='testuser').delete()

        # Create a game user profile with the current username and the score of the game set to 0
        game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

        return game_user_profile

    def start_guess_the_digit_game(self, data):
        # Navigating to the guess the digit game page, which will then be used for the GET and POST requests
        guess_the_digit_game_url = reverse('guess_the_digit:play')

        # Make the GET request, passing the parameters so that the game can be created (what level they want and hints enabled/disabled)
        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, data['params'])

        # Check to see if 200 code was returned, which indicates success
        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200)

        return guess_the_digit_game_url

    def simulating_guess_the_digit_process(self, data):
        # Choose the correct options for the game and click on the button the start the game. This is the GET request part
        guess_the_digit_game_url = self.start_guess_the_digit_game(data)

        # Here, we are submitting the guesses. The last guess will be the correct one.
        for i in range(0, data['number_of_guesses']):
            # If there are still more guesses left, perform the following operations:
            if i < (data['number_of_guesses']-1):

                # Set the user guess as the current element in the list, which is indicated by the i in the for loop
                user_guess_data = {
                    'guess_number_input_field' : data['incorrect_guesses_from_user'][i]
                }

                # Send the data from above as part of the POST request
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, user_guess_data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], data['params']['selected_level'])

                # Checking whether the guess was correct
                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!")
            
            # If this is the last guess
            else:
                # Set the user guess to the correct number
                user_guess_data = {
                    'guess_number_input_field' : data['correct_number']
                }

                game_user_profile = self.create_user_profile()

                # Make a POST request using the data from above
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, user_guess_data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], data['params']['selected_level'])

                # If the user guessed the number correctly, do this
                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    # Set the score to the required number of points, depending on the level and if hints were enabled.
                    game_user_profile.current_score = data['correct_guess_points']
                
                # Check whether the score is set correctly
                self.assertEqual(game_user_profile.current_score, data['correct_guess_points'])
    
    # Simulating the "Guess the Digit" game using the scenario that the user chose the easy level with hints enabled
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_easy_hints_enabled(self, mock_random_number):
        # Set the correct number as 5. This is the number the user has to guess.
        mock_random_number.return_value = 5
        
        # Holds all the data that is required for the game.
        data = {
            'correct_number' : mock_random_number.return_value,
            'number_of_guesses' : 2,
            'incorrect_guesses_from_user' : [3],
            'correct_guess_points' : 5,
            'params' : {'selected_level' : 'easy', 'hints' : 'yes'}
        }

        # Calling the method that will simulate the game process, using the data from above
        self.simulating_guess_the_digit_process(data)
    
    # Simulating the "Guess the Digit" game using the scenario that the user chose the easy level with hints disabled
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_easy_hints_disabled(self, mock_random_number):
        # Set the correct number as 8. This is the number the user has to guess.
        mock_random_number.return_value = 8
        
        # Holds all the data that is required for the game.
        data = {
            'correct_number' : mock_random_number.return_value,
            'number_of_guesses' : 4,
            'incorrect_guesses_from_user' : [10,1,4],
            'correct_guess_points' : 10,
            'params' : {'selected_level' : 'easy', 'hints' : 'no'}
        }

        # Calling the method that will simulate the game process, using the data from above
        self.simulating_guess_the_digit_process(data)

    # Simulating the "Guess the Digit" game using the scenario that the user chose the medium level with hints enabled
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_medium_hints_enabled(self, mock_random_number):
        # Set the correct number as 12. This is the number the user has to guess.
        mock_random_number.return_value = 12
        
        # Holds all the data that is required for the game.
        data = {
            'correct_number' : mock_random_number.return_value,
            'number_of_guesses' : 5,
            'incorrect_guesses_from_user' : [33, 50, 26, 11],
            'correct_guess_points' : 25,
            'params' : {'selected_level' : 'medium', 'hints' : 'yes'}
        }

        # Calling the method that will simulate the game process, using the data from above
        self.simulating_guess_the_digit_process(data)

    # Simulating the "Guess the Digit" game using the scenario that the user chose the medium level with hints disabled
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_medium_hints_disabled(self, mock_random_number):
        # Set the correct number as 10. This is the number the user has to guess.
        mock_random_number.return_value = 10
        
        # Holds all the data that is required for the game.
        data = {
            'correct_number' : mock_random_number.return_value,
            'number_of_guesses' : 10,
            'incorrect_guesses_from_user' : [21, 50, 41, 17, 1, 39, 40, 5, 22],
            'correct_guess_points' : 50,
            'params' : {'selected_level' : 'medium', 'hints' : 'no'}
        }

        # Calling the method that will simulate the game process, using the data from above
        self.simulating_guess_the_digit_process(data)
    
    # Simulating the "Guess the Digit" game using the scenario that the user chose the hard level with hints enabled
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_hard_hints_enabled(self, mock_random_number):
        # Set the correct number as 69. This is the number the user has to guess.
        mock_random_number.return_value = 69
        
        # Holds all the data that is required for the game.
        data = {
            'correct_number' : mock_random_number.return_value,
            'number_of_guesses' : 11,
            'incorrect_guesses_from_user' : [11, 66, 50, 45, 100, 49, 84, 99, 27, 70],
            'correct_guess_points' : 75,
            'params' : {'selected_level' : 'hard', 'hints' : 'yes'}
        }

        # Calling the method that will simulate the game process, using the data from above
        self.simulating_guess_the_digit_process(data)

    # Simulating the "Guess the Digit" game using the scenario that the user chose the hard level with hints disabled
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_hard_hints_disabled(self, mock_random_number):
        # Set the correct number as 100. This is the number the user has to guess.
        mock_random_number.return_value = 100
        
        # Holds all the data that is required for the game.
        data = {
            'correct_number' : mock_random_number.return_value,
            'number_of_guesses' : 20,
            'incorrect_guesses_from_user' : [1, 99, 50, 25, 77, 69, 33, 66, 80, 91, 16, 9, 4, 55, 35, 12, 61, 31, 47],
            'correct_guess_points' : 100,
            'params' : {'selected_level' : 'hard', 'hints' : 'no'}
        }

        # Calling the method that will simulate the game process, using the data from above
        self.simulating_guess_the_digit_process(data)