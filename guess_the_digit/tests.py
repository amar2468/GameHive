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
    # This function will test valid input and whether the form is deemed to be valid (as expected)
    def testing_valid_input(self):
        # User chooses the number 4 as their guess
        data = {
            'guess_number_input_field' : 4
        }

        # Take the input and validate it using the django form
        form = GuessTheNumberInputForm(data=data)

        # Check whether the form is valid, which it should be
        self.assertTrue(form.is_valid())

    # This function will have multiple cases of invalid input and checks whether the form is not valid (as expected)
    def testing_invalid_input(self):
        # Testing whitespace in the input field, instead of integers
        data = {
            'guess_number_input_field' : ''
        }

        # Take the input and validate it using the django form
        form = GuessTheNumberInputForm(data=data)

        # Check whether the form is valid, which it shouldn't be
        self.assertFalse(form.is_valid())

        # Testing letters in the input field, instead of integers
        data = {
            'guess_number_input_field' : 'a'
        }

        # Take the input and validate it using the django form
        form = GuessTheNumberInputForm(data=data)

        # Check whether the form is valid, which it shouldn't be
        self.assertFalse(form.is_valid())

        # Testing special characters in the input field

        data = {
            'guess_number_input_field' : '!*!*!*!*!*'
        }

        # Take the input and validate it using the django form
        form = GuessTheNumberInputForm(data=data)

        # Check whether the form is valid, which it shouldn't be
        self.assertFalse(form.is_valid())

        # Testing spaces between numbers in the input field

        data = {
            'guess_number_input_field' : '12 2'
        }

        # Take the input and validate it using the django form
        form = GuessTheNumberInputForm(data=data)

        # Check whether the form is valid, which it shouldn't be
        self.assertFalse(form.is_valid())


# Integration test for "Guess the Digit" game

class GuessTheDigitIntegrationTestCase(BaseTestCase):
    
    # Simulating the "Guess the Digit" game using the scenario that the user chose the easy level with hints enabled
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_easy_hints_enabled(self, mock_random_number):

        # Set the correct number as 5. This is the number the user has to guess.
        mock_random_number.return_value = 5

        # Navigating to the guess the digit game page, which will then be used for the GET and POST requests
        guess_the_digit_game_url = reverse('guess_the_digit:play')

        # GET Request - WHEN HINTS ARE ENABLED

        # Set the parameters according to user preference. This will be sent as data when performing the GET request
        params = {'selected_level' : 'easy', 'hints' : 'yes'}

        # Make the GET request, passing the parameters so that the game can be created (what level they want and hints enabled/disabled)
        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        # Check to see if 200 code was returned, which indicates success
        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200)

        # Set the number of guesses the user has, so that cases can be created, which will simulate the process of the game
        number_of_guesses = 2

        # Creating a list to hold all the incorrect guesses from the user
        incorrect_guesses_from_user = [3]

        # POST Request - WHEN HINTS ARE ENABLED

        # This for loop will loop for the number of guesses that was set initially
        for i in range(0, number_of_guesses):
            # If there are still more guesses left, perform the following operations:
            if i < (number_of_guesses-1):

                # Set the user guess as the current element in the list, which is indicated by the i in the for loop
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                # Send the data from above as part of the POST request
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy")

                # Checking whether the guess was correct
                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!")
            
            # If this is the last guess
            else:
                # Set the user guess as 5, which is the correct number
                data = {
                    'guess_number_input_field' : 5
                }

                # Delete the user with the username "testuser" if they already exist
                GameUserProfile.objects.filter(user__username='testuser').delete()

                # Create a game user profile with the current username and the score of the game set to 0
                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

                # Make a POST request using the data from above
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy")

                # If the user guessed the number correctly, do this
                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    # Set the score to 5
                    game_user_profile.current_score = 5
                
                # Check whether the score is 5
                self.assertEqual(game_user_profile.current_score, 5)
    
    # Simulating the "Guess the Digit" game using the scenario that the user chose the easy level with hints disabled

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_easy_hints_disabled(self, mock_random_number):
        # Set the correct number as 8. This is the number the user has to guess.
        mock_random_number.return_value = 8

        # Navigating to the guess the digit game page, which will then be used for the GET and POST requests
        guess_the_digit_game_url = reverse('guess_the_digit:play')

        # GET Request - WHEN HINTS ARE DISABLED

        # Set the parameters according to user preference. This will be sent as data when performing the GET request
        params = {'selected_level' : 'easy', 'hints' : 'no'}

        # Make the GET request, passing the parameters so that the game can be created (what level they want and hints enabled/disabled)
        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        # Check to see if 200 code was returned, which indicates success
        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200)

        # Set the number of guesses the user has, so that cases can be created, which will simulate the process of the game
        number_of_guesses = 4

        # Creating a list to hold all the incorrect guesses from the user
        incorrect_guesses_from_user = [10,1,4]

        # POST Request - WHEN HINTS ARE DISABLED

        # This for loop will loop for the number of guesses that was set initially
        for i in range(0, number_of_guesses):
            # If there are still more guesses left, perform the following operations:
            if i < (number_of_guesses-1):

                # Set the user guess as the current element in the list, which is indicated by the i in the for loop
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                # Send the data from above as part of the POST request
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy")

                # Checking whether the guess was correct
                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!")
            
            # If this is the last guess
            else:
                # Set the user guess as 8, which is the correct number
                data = {
                    'guess_number_input_field' : 8
                }

                # Delete the user with the username "testuser" if they already exist
                GameUserProfile.objects.filter(user__username='testuser').delete()

                # Create a game user profile with the current username and the score of the game set to 0
                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

                # Make a POST request using the data from above
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy")

                # If the user guessed the number correctly, do this
                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    # Set the score to 10
                    game_user_profile.current_score = 10
                
                # Check whether the score is 10
                self.assertEqual(game_user_profile.current_score, 10)

    # Simulating the "Guess the Digit" game using the scenario that the user chose the medium level with hints enabled

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_medium_hints_enabled(self, mock_random_number):
        # Set the correct number as 12. This is the number the user has to guess.
        mock_random_number.return_value = 12

        # Navigating to the guess the digit game page, which will then be used for the GET and POST requests
        guess_the_digit_game_url = reverse('guess_the_digit:play')

        # GET Request - WHEN HINTS ARE ENABLED

        # Set the parameters according to user preference. This will be sent as data when performing the GET request
        params = {'selected_level' : 'medium', 'hints' : 'yes'}

        # Make the GET request, passing the parameters so that the game can be created (what level they want and hints enabled/disabled)
        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        # Check to see if 200 code was returned, which indicates success
        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200)

        # Set the number of guesses the user has, so that cases can be created, which will simulate the process of the game
        number_of_guesses = 5

        # Creating a list to hold all the incorrect guesses from the user
        incorrect_guesses_from_user = [33, 50, 26, 11]

        # POST Request - WHEN HINTS ARE ENABLED

        # This for loop will loop for the number of guesses that was set initially
        for i in range(0, number_of_guesses):
            # If there are still more guesses left, perform the following operations:
            if i < (number_of_guesses-1):

                # Set the user guess as the current element in the list, which is indicated by the i in the for loop
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                # Send the data from above as part of the POST request
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium")

                # Checking whether the guess was correct
                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!")
            
            # If this is the last guess
            else:
                # Set the user guess as 12, which is the correct number
                data = {
                    'guess_number_input_field' : 12
                }

                # Delete the user with the username "testuser" if they already exist
                GameUserProfile.objects.filter(user__username='testuser').delete()

                # Create a game user profile with the current username and the score of the game set to 0
                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

                # Make a POST request using the data from above
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium")

                # If the user guessed the number correctly, do this
                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    # Set the score to 25
                    game_user_profile.current_score = 25
                
                # Check whether the score is 25
                self.assertEqual(game_user_profile.current_score, 25)

    # Simulating the "Guess the Digit" game using the scenario that the user chose the medium level with hints disabled

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_medium_hints_disabled(self, mock_random_number):
        # Set the correct number as 10. This is the number the user has to guess.
        mock_random_number.return_value = 10
        
        # Navigating to the guess the digit game page, which will then be used for the GET and POST requests
        guess_the_digit_game_url = reverse('guess_the_digit:play')

        # GET Request - WHEN HINTS ARE DISABLED

        # Set the parameters according to user preference. This will be sent as data when performing the GET request
        params = {'selected_level' : 'medium', 'hints' : 'no'}

        # Make the GET request, passing the parameters so that the game can be created (what level they want and hints enabled/disabled)
        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        # Check to see if 200 code was returned, which indicates success
        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200)

        # Set the number of guesses the user has, so that cases can be created, which will simulate the process of the game
        number_of_guesses = 10

        # Creating a list to hold all the incorrect guesses from the user
        incorrect_guesses_from_user = [21, 50, 41, 17, 1, 39, 40, 5, 22]

        # POST Request - WHEN HINTS ARE DISABLED

        # This for loop will loop for the number of guesses that was set initially
        for i in range(0, number_of_guesses):
            # If there are still more guesses left, perform the following operations:
            if i < (number_of_guesses-1):

                # Set the user guess as the current element in the list, which is indicated by the i in the for loop
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                # Send the data from above as part of the POST request
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium")

                # Checking whether the guess was correct
                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!")
            
            # If this is the last guess
            else:
                # Set the user guess as 10, which is the correct number
                data = {
                    'guess_number_input_field' : 10
                }

                # Delete the user with the username "testuser" if they already exist
                GameUserProfile.objects.filter(user__username='testuser').delete()

                # Create a game user profile with the current username and the score of the game set to 0
                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

                # Make a POST request using the data from above
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium")

                # If the user guessed the number correctly, do this
                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    # Set the score to 50
                    game_user_profile.current_score = 50
                
                # Check whether the score is 50
                self.assertEqual(game_user_profile.current_score, 50)
    
    # Simulating the "Guess the Digit" game using the scenario that the user chose the hard level with hints enabled

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_hard_hints_enabled(self, mock_random_number):
        # Set the correct number as 69. This is the number the user has to guess.
        mock_random_number.return_value = 69

        # Navigating to the guess the digit game page, which will then be used for the GET and POST requests
        guess_the_digit_game_url = reverse('guess_the_digit:play')

        # GET Request - WHEN HINTS ARE ENABLED

        # Set the parameters according to user preference. This will be sent as data when performing the GET request
        params = {'selected_level' : 'hard', 'hints' : 'yes'}

        # Make the GET request, passing the parameters so that the game can be created (what level they want and hints enabled/disabled)
        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        # Check to see if 200 code was returned, which indicates success
        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200)

        # Set the number of guesses the user has, so that cases can be created, which will simulate the process of the game
        number_of_guesses = 11

        # Creating a list to hold all the incorrect guesses from the user
        incorrect_guesses_from_user = [11, 66, 50, 45, 100, 49, 84, 99, 27, 70]

        # POST Request - WHEN HINTS ARE ENABLED

        # This for loop will loop for the number of guesses that was set initially
        for i in range(0, number_of_guesses):
            # If there are still more guesses left, perform the following operations:
            if i < (number_of_guesses-1):

                # Set the user guess as the current element in the list, which is indicated by the i in the for loop
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                # Send the data from above as part of the POST request
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard")

                # Checking whether the guess was correct
                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!")
            
            # If this is the last guess
            else:
                # Set the user guess as 69, which is the correct number
                data = {
                    'guess_number_input_field' : 69
                }

                # Delete the user with the username "testuser" if they already exist
                GameUserProfile.objects.filter(user__username='testuser').delete()

                # Create a game user profile with the current username and the score of the game set to 0
                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

                # Make a POST request using the data from above
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard")

                # If the user guessed the number correctly, do this
                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    # Set the score to 75
                    game_user_profile.current_score = 75
                
                # Check whether the score is 75
                self.assertEqual(game_user_profile.current_score, 75)

    # Simulating the "Guess the Digit" game using the scenario that the user chose the hard level with hints disabled

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_hard_hints_disabled(self, mock_random_number):
        # Set the correct number as 100. This is the number the user has to guess.
        mock_random_number.return_value = 100

        # Navigating to the guess the digit game page, which will then be used for the GET and POST requests
        guess_the_digit_game_url = reverse('guess_the_digit:play')

        # GET Request - WHEN HINTS ARE DISABLED

        # Set the parameters according to user preference. This will be sent as data when performing the GET request
        params = {'selected_level' : 'hard', 'hints' : 'no'}

        # Make the GET request, passing the parameters so that the game can be created (what level they want and hints enabled/disabled)
        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        # Check to see if 200 code was returned, which indicates success
        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200)

        # Set the number of guesses the user has, so that cases can be created, which will simulate the process of the game
        number_of_guesses = 20

        # Creating a list to hold all the incorrect guesses from the user
        incorrect_guesses_from_user = [1, 99, 50, 25, 77, 69, 33, 66, 80, 91, 16, 9, 4, 55, 35, 12, 61, 31, 47]

        # POST Request - WHEN HINTS ARE DISABLED

        # This for loop will loop for the number of guesses that was set initially
        for i in range(0, number_of_guesses):
            # If there are still more guesses left, perform the following operations:
            if i < (number_of_guesses-1):

                # Set the user guess as the current element in the list, which is indicated by the i in the for loop
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                # Send the data from above as part of the POST request
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard")

                # Checking whether the guess was correct
                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!")
            
            # If this is the last guess
            else:
                # Set the user guess as 100, which is the correct number
                data = {
                    'guess_number_input_field' : 100
                }

                # Delete the user with the username "testuser" if they already exist
                GameUserProfile.objects.filter(user__username='testuser').delete()

                # Create a game user profile with the current username and the score of the game set to 0
                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

                # Make a POST request using the data from above
                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                # Check to see if 200 code was returned, which indicates success
                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200)
                
                # Checking whether the level was set correctly
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard")

                # If the user guessed the number correctly, do this
                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    # Set the score to 100
                    game_user_profile.current_score = 100
                
                # Check whether the score is 100
                self.assertEqual(game_user_profile.current_score, 100)