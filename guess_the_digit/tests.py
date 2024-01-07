from django.test import TestCase, Client
from .forms import GuessTheNumberInputForm
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from gamehive.models import GameUserProfile

# Unit test for "Guess the Digit" game

class GuessTheDigitTestCase(TestCase):
    # Create the user so that the unit tests for the game can be carried out
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password34*')
        self.client = Client()
    
    # This function will test valid input and whether the form is deemed to be valid (as expected)
    def testing_valid_input(self):
        self.client.login(username='testuser', password='Password34*')

        data = {
            'guess_number_input_field' : 4
        }

        form = GuessTheNumberInputForm(data=data)

        self.assertTrue(form.is_valid())

    # This function will have multiple cases of invalid input and checks whether the form is not valid (as expected)
    def testing_invalid_input(self):
        self.client.login(username='testuser', password='Password34*')

        # Testing letters in the input field, instead of integers
        data = {
            'guess_number_input_field' : 'a'
        }

        form = GuessTheNumberInputForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing special characters in the input field

        data = {
            'guess_number_input_field' : '!*!*!*!*!*'
        }

        form = GuessTheNumberInputForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing spaces between numbers in the input field

        data = {
            'guess_number_input_field' : '12 2'
        }

        form = GuessTheNumberInputForm(data=data)

        self.assertFalse(form.is_valid())


# Integration test for "Guess the Digit" game

class GuessTheDigitIntegrationTestCase(TestCase):
    # Create the user so that the integration test for the game can be carried out
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='Password34*')
        self.client = Client()
    
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_easy_hints_enabled(self, mock_random_number):
        self.client.login(username='testuser', password='Password34*')

        mock_random_number.return_value = 5

        guess_the_digit_game_url = reverse('play')

        # GET Request - WHEN HINTS ARE ENABLED

        params = {'selected_level' : 'easy', 'hints' : 'yes'}

        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

        number_of_guesses = 2

        incorrect_guesses_from_user = [3]

        # POST Request - WHEN HINTS ARE ENABLED

        for i in range(0, number_of_guesses):
            if i < (number_of_guesses-1):
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy") # Checking whether the level was set correctly

                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!") # Checking whether the guess was correct
            else:
                data = {
                    'guess_number_input_field' : 5
                }

                GameUserProfile.objects.filter(user__username='testuser').delete()

                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score_guess_number_game=0)

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy") # Checking whether the level was set correctly

                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    game_user_profile.current_score_guess_number_game = 5
                
                self.assertEqual(game_user_profile.current_score_guess_number_game, 5)

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_easy_hints_disabled(self, mock_random_number):

        self.client.login(username='testuser', password='Password34*')

        mock_random_number.return_value = 8

        guess_the_digit_game_url = reverse('play')

        # GET Request - WHEN HINTS ARE DISABLED

        params = {'selected_level' : 'easy', 'hints' : 'no'}

        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

        number_of_guesses = 4

        incorrect_guesses_from_user = [10,1,4]

        # POST Request - WHEN HINTS ARE DISABLED

        for i in range(0, number_of_guesses):
            if i < (number_of_guesses-1):
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy") # Checking whether the level was set correctly

                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!") # Checking whether the guess was correct
            else:
                data = {
                    'guess_number_input_field' : 8
                }

                GameUserProfile.objects.filter(user__username='testuser').delete()

                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score_guess_number_game=0)

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "easy") # Checking whether the level was set correctly

                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    game_user_profile.current_score_guess_number_game = 10
                
                self.assertEqual(game_user_profile.current_score_guess_number_game, 10)

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_medium_hints_enabled(self, mock_random_number):
        self.client.login(username='testuser', password='Password34*')

        mock_random_number.return_value = 12

        guess_the_digit_game_url = reverse('play')

        # Get request for guess the digit game. This will be executed when the user initially opens the "Guess the Digit" game
        # GET Request - WHEN HINTS ARE ENABLED

        params = {'selected_level' : 'medium', 'hints' : 'yes'}

        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

        number_of_guesses = 5

        incorrect_guesses_from_user = [33, 50, 26, 11]

        # POST Request - WHEN HINTS ARE ENABLED

        for i in range(0, number_of_guesses):
            if i < (number_of_guesses-1):
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium") # Checking whether the level was set correctly

                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!") # Checking whether the guess was correct
            else:
                data = {
                    'guess_number_input_field' : 12
                }

                GameUserProfile.objects.filter(user__username='testuser').delete()

                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score_guess_number_game=0)

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium") # Checking whether the level was set correctly

                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    game_user_profile.current_score_guess_number_game = 25
                
                self.assertEqual(game_user_profile.current_score_guess_number_game, 25)

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_medium_hints_disabled(self, mock_random_number):
        self.client.login(username='testuser', password='Password34*')

        mock_random_number.return_value = 10

        guess_the_digit_game_url = reverse('play')

        # Get request for guess the digit game. This will be executed when the user initially opens the "Guess the Digit" game
        # GET Request - WHEN HINTS ARE DISABLED

        params = {'selected_level' : 'medium', 'hints' : 'no'}

        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

        number_of_guesses = 10

        incorrect_guesses_from_user = [21, 50, 41, 17, 1, 39, 40, 5, 22]

        # POST Request - WHEN HINTS ARE DISABLED

        for i in range(0, number_of_guesses):
            if i < (number_of_guesses-1):
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium") # Checking whether the level was set correctly

                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!") # Checking whether the guess was correct
            else:
                data = {
                    'guess_number_input_field' : 10
                }

                GameUserProfile.objects.filter(user__username='testuser').delete()

                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score_guess_number_game=0)

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "medium") # Checking whether the level was set correctly

                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    game_user_profile.current_score_guess_number_game = 50
                
                self.assertEqual(game_user_profile.current_score_guess_number_game, 50)
    
    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_hard_hints_enabled(self, mock_random_number):
        self.client.login(username='testuser', password='Password34*')

        mock_random_number.return_value = 69

        guess_the_digit_game_url = reverse('play')

        # Get request for guess the digit game. This will be executed when the user initially opens the "Guess the Digit" game
        # GET Request - WHEN HINTS ARE ENABLED

        params = {'selected_level' : 'hard', 'hints' : 'yes'}

        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

        number_of_guesses = 11

        incorrect_guesses_from_user = [11, 66, 50, 45, 100, 49, 84, 99, 27, 70]

        # POST Request - WHEN HINTS ARE ENABLED

        for i in range(0, number_of_guesses):
            if i < (number_of_guesses-1):
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard") # Checking whether the level was set correctly

                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!") # Checking whether the guess was correct
            else:
                data = {
                    'guess_number_input_field' : 69
                }

                GameUserProfile.objects.filter(user__username='testuser').delete()

                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score_guess_number_game=0)

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard") # Checking whether the level was set correctly

                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    game_user_profile.current_score_guess_number_game = 50
                
                self.assertEqual(game_user_profile.current_score_guess_number_game, 50)

    @patch('guess_the_digit.views.random.randint')
    def test_for_guess_the_digit_process_level_hard_hints_disabled(self, mock_random_number):
        self.client.login(username='testuser', password='Password34*')

        mock_random_number.return_value = 100

        guess_the_digit_game_url = reverse('play')

        # Get request for guess the digit game. This will be executed when the user initially opens the "Guess the Digit" game
        # GET Request - WHEN HINTS ARE DISABLED

        params = {'selected_level' : 'hard', 'hints' : 'no'}

        get_response_for_guess_digit_game_url = self.client.get(guess_the_digit_game_url, params)

        self.assertEqual(get_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

        number_of_guesses = 20

        incorrect_guesses_from_user = [1, 99, 50, 25, 77, 69, 33, 66, 80, 91, 16, 9, 4, 55, 35, 12, 61, 31, 47]

        # POST Request - WHEN HINTS ARE DISABLED

        for i in range(0, number_of_guesses):
            if i < (number_of_guesses-1):
                data = {
                    'guess_number_input_field' : incorrect_guesses_from_user[i]
                }

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard") # Checking whether the level was set correctly

                self.assertEqual(post_response_for_guess_digit_game_url.context['result'], "Wrong guess! Try again!") # Checking whether the guess was correct
            else:
                data = {
                    'guess_number_input_field' : 100
                }

                GameUserProfile.objects.filter(user__username='testuser').delete()

                game_user_profile = GameUserProfile.objects.create(user=self.user, current_score_guess_number_game=0)

                post_response_for_guess_digit_game_url = self.client.post(guess_the_digit_game_url, data, follow=True)

                self.assertEqual(post_response_for_guess_digit_game_url.status_code, 200) # Check to see if 200 code was returned, which indicates success
                
                self.assertEqual(post_response_for_guess_digit_game_url.context['level'], "hard") # Checking whether the level was set correctly

                if post_response_for_guess_digit_game_url.context['result'] == "Correct guess! Well done!":
                    game_user_profile.current_score_guess_number_game = 100
                
                self.assertEqual(game_user_profile.current_score_guess_number_game, 100)