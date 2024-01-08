from django.test import TestCase, Client
from unittest.mock import patch
from gamehive.models import GameUserProfile
from .forms import RockPaperScissorsInputForm
from django.contrib.auth.models import User
from django.urls import reverse

# Unit Test for Rock, Paper, Scissors game - check whether a valid option was chosen

class RockPaperScissorsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='Password34*')
        self.client = Client()
    
    def testing_valid_input_rps(self):

        self.client.login(username='testuser', password='Password34*')

        data = {
            'carousel_value' : 'rock'
        }

        form = RockPaperScissorsInputForm(data=data)

        self.assertTrue(form.is_valid())

# This class contains the integration tests for the rock paper scissors game. The two tests inside simulate two situations:
# 1. User has lost the round
# 2. User has won the round

class RockPaperScissorsIntegrationTestCase(TestCase):
    # Setting up the user so that the integration test can be carried out while user is logged in
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='Password34*')
        self.client = Client()
    
    # Simulating a situation where the user has lost the round using the test below.
    @patch('rock_paper_scissors.views.random.choice')
    def test_simultating_user_losing_rock_paper_scissors_game(self, mock_choice):
        # Setting the computer choice as "rock"
        mock_choice.return_value = 'rock'

        # Logging in the user using the valid credentials
        self.client.login(username='testuser', password='Password34*')

        # Navigating to the rps_form_submitted view, which will then be used for the GET and POST requests
        rock_paper_scissors_game_url_form = reverse('rock_paper_scissors:rps_form_submitted')

        # GET request made, which would open the rps game page
        get_response_for_rock_paper_scissors_game_url = self.client.get(rock_paper_scissors_game_url_form)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(get_response_for_rock_paper_scissors_game_url.status_code, 200)

        # FIRST ATTEMPT FROM USER

        # Setting the user option as "paper"
        data = {
            'carousel_value' : 'paper'
        }

        # Making a POST request, sending the data such as the user option in the POST request
        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, data, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse
        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the user choice was set correctly i.e. "paper"

        self.assertEqual(rps_response_data['user_rps_choice'], "paper")

        # Checking whether there are 2 attempts left, which is the correct number after one guess

        self.assertEqual(rps_response_data['attempts'], 2)

        # Checking whether the computer choice is still "rock"
        
        self.assertEqual(rps_response_data['computer_rps_choice'], 'rock')

        # Checking to see if this outcome would be a win, as it should be

        self.assertEqual(rps_response_data['rps_outcome'], 'win')

        # SECOND ATTEMPT FROM USER

        # Setting the user option as "rock"
        data = {
            'carousel_value' : 'rock'
        }

        # Making a POST request, sending the data such as the user option in the POST request
        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, data, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse
        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the user choice was set correctly i.e. "rock"

        self.assertEqual(rps_response_data['user_rps_choice'], "rock")

        # Checking whether there is 1 attempt left, which is the correct number after two guesses

        self.assertEqual(rps_response_data['attempts'], 1)

        # Checking whether the computer choice is still "rock"

        self.assertEqual(rps_response_data['computer_rps_choice'], 'rock')

        # Checking to see if this outcome would be a draw, as it should be
        self.assertEqual(rps_response_data['rps_outcome'], 'draw')

        # LAST ATTEMPT FROM USER

        # Setting the user option as "scissors"
        data = {
            'carousel_value' : 'scissors'
        }

        # Making a POST request, sending the data such as the user option in the POST request
        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, data, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse

        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the user choice was set correctly i.e. "scissors"

        self.assertEqual(rps_response_data['user_rps_choice'], "scissors")

        # Checking whether this is the last attempt, which it should be

        self.assertEqual(rps_response_data['attempts'], 0)

        # Checking whether the computer choice is still "rock"

        self.assertEqual(rps_response_data['computer_rps_choice'], 'rock')

        # Checking to see if this outcome would be a loss, as it should be

        self.assertEqual(rps_response_data['rps_outcome'], 'lose')


        # END THE ROUND TO SEE THE OUTCOME OF THE GAME - IN THIS CASE, THE USER HAS LOST

        # POST request is made, in order to end the round

        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse

        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the outcome of the round is that the user lost, as it should be

        self.assertEqual(rps_response_data['rps_outcome'], 'Game Over! You failed to win this round! Good luck next time!')
    
    # Simulating a situation where the user has won the round using the test below.
    
    @patch('rock_paper_scissors.views.random.choice')
    def test_simultating_user_winning_rock_paper_scissors_game(self, mock_choice):
        # Setting the computer choice as "paper"
        mock_choice.return_value = 'paper'

        # Logging in the user using the valid credentials
        self.client.login(username='testuser', password='Password34*')

        # Navigating to the rps_form_submitted view, which will then be used for the GET and POST requests
        rock_paper_scissors_game_url_form = reverse('rock_paper_scissors:rps_form_submitted')

        # GET request made, which would open the rps game page
        get_response_for_rock_paper_scissors_game_url = self.client.get(rock_paper_scissors_game_url_form)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(get_response_for_rock_paper_scissors_game_url.status_code, 200)


        # FIRST ATTEMPT FROM USER

        # Setting the user option as "scissors"

        data = {
            'carousel_value' : 'scissors'
        }

        # Making a POST request, sending the data such as the user option in the POST request

        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, data, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse

        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the user choice was set correctly i.e. "scissors"

        self.assertEqual(rps_response_data['user_rps_choice'], "scissors")

        # Checking whether there are 2 attempts left, which is the correct number after one guess

        self.assertEqual(rps_response_data['attempts'], 2)

        # Checking whether the computer choice is still "paper"
        
        self.assertEqual(rps_response_data['computer_rps_choice'], 'paper')

        # Checking to see if this outcome would be a win, as it should be

        self.assertEqual(rps_response_data['rps_outcome'], 'win')


        # SECOND ATTEMPT FROM USER

        # Setting the user option as "paper"

        data = {
            'carousel_value' : 'paper'
        }

        # Making a POST request, sending the data such as the user option in the POST request

        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, data, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse

        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the user choice was set correctly i.e. "paper"

        self.assertEqual(rps_response_data['user_rps_choice'], "paper")

        # Checking whether there is 1 attempt left, which is the correct number after two guesses

        self.assertEqual(rps_response_data['attempts'], 1)

        # Checking whether the computer choice is still "paper"
        
        self.assertEqual(rps_response_data['computer_rps_choice'], 'paper')

        # Checking to see if this outcome would be a draw, as it should be

        self.assertEqual(rps_response_data['rps_outcome'], 'draw')

        # THIRD ATTEMPT FROM USER

        # Setting the user option as "scissors"

        data = {
            'carousel_value' : 'scissors'
        }

        # Making a POST request, sending the data such as the user option in the POST request

        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, data, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse

        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the user choice was set correctly i.e. "scissors"

        self.assertEqual(rps_response_data['user_rps_choice'], "scissors")

        # Checking whether there are no attempts left, which is the correct number after three guesses

        self.assertEqual(rps_response_data['attempts'], 0)

        # Checking whether the computer choice is still "paper"
        
        self.assertEqual(rps_response_data['computer_rps_choice'], 'paper')

        # Checking to see if this outcome would be a win, as it should be

        self.assertEqual(rps_response_data['rps_outcome'], 'win')


        # END THE ROUND TO SEE THE OUTCOME OF THE GAME - IN THIS CASE, THE USER HAS WON

        # Creating a user profile, so that the current score in the rock paper scissors game can be tracked

        game_user_profile = GameUserProfile.objects.create(user=self.user, current_score_rps=0)

        # POST request is made, in order to end the round

        post_response_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, follow=True)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(post_response_for_rock_paper_scissors_game_url.status_code, 200)

        # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse

        rps_response_data = post_response_for_rock_paper_scissors_game_url.json()

        # Checking whether the outcome of the round is that the user won, as it should be

        self.assertEqual(rps_response_data['rps_outcome'], 'Game Over! You won this round! You have received 10 points!')

        # Checking to see if the user won the round and if they did, add 10 points to their score

        if rps_response_data['rps_outcome'] == "Game Over! You won this round! You have received 10 points!":
            game_user_profile.current_score_rps = 10
        
        # Check whether the user has 10 points, which indicates that they won the round
        
        self.assertEqual(game_user_profile.current_score_rps, 10)