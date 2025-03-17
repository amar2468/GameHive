from django.test import TestCase, Client
from unittest.mock import patch
from gamehive.models import CustomUser,GameUserProfile
from .forms import RockPaperScissorsInputForm
from django.urls import reverse

# Unit Test for Rock, Paper, Scissors game - check whether a valid option was chosen

class RockPaperScissorsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser',
            email='testuser@gmail.com',
            password='Password34*',
            account_type="user"
        )

        self.client = Client()

        self.client.login(username='testuser', password='Password34*')
    
    # Testing whether the form is valid if the user chooses "rock"
    def testing_valid_input_rps_rock(self):
        data = {
            'carousel_value' : 'rock'
        }

        form = RockPaperScissorsInputForm(data=data)

        self.assertTrue(form.is_valid())

    # Testing whether the form is valid if the user chooses "paper"
    def testing_valid_input_rps_paper(self):
        data = {
            'carousel_value' : 'paper'
        }

        form = RockPaperScissorsInputForm(data=data)

        self.assertTrue(form.is_valid())
    
    # Testing whether the form is valid if the user chooses "scissors"
    def testing_valid_input_rps_scissors(self):
        data = {
            'carousel_value' : 'scissors'
        }

        form = RockPaperScissorsInputForm(data=data)

        self.assertTrue(form.is_valid())

# This class contains the integration tests for the rock paper scissors game. The two tests inside simulate two situations:
# 1. User has lost the round
# 2. User has won the round

class RockPaperScissorsIntegrationTestCase(TestCase):
    # Setting up the user so that the integration test can be carried out while user is logged in
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

        # Logging in the user using the valid credentials
        self.client.login(username='testuser', password='Password34*')
    
    def create_user_game_profile(self):
        # Delete the game record for the user before adding the new information, ensuring we have a clean slate after each time this
        # test is run. Otherwise, we will get an integrity error.
        GameUserProfile.objects.filter(user=self.user).delete()

        # Creating the game user profile and assigning a score of 0 for the user
        game_user_profile = GameUserProfile.objects.create(user=self.user, current_score=0)

        return game_user_profile
    
    # Method - simulating a situation where the user has lost the game
    @patch('rock_paper_scissors.views.random.choice')
    def test_simultating_user_losing_rock_paper_scissors_game(self, mock_choice):
        # Added failed attempts from the user. This is because we are simulating a game where the user lost.
        user_attempts = ["scissors", "rock", "scissors"]

        # Adding successful attempts from the computer, as the computer has to win in this scenario.
        computer_attempts = ["rock", "paper", "rock"]

        mock_choice.return_value = computer_attempts[0]

        # Navigating to the rps_form_submitted view, which will then be used for the GET and POST requests
        rock_paper_scissors_game_url_form = reverse('rock_paper_scissors:rps_form_submitted')

        # GET request made, which would open the rps game page
        get_response_for_rock_paper_scissors_game_url = self.client.get(rock_paper_scissors_game_url_form)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(get_response_for_rock_paper_scissors_game_url.status_code, 200)

        for i in range(0, len(user_attempts)):
            # Setting the RPS option for the computer, as per the computer_attempts list.
            mock_choice.return_value = computer_attempts[i]

            # Setting the RPS option for the user, as per the user_attempts list.
            user_data = {
                'carousel_value' : user_attempts[i]
            }

            # Making a POST request, sending the data such as the user option in the POST request
            post_resp_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, user_data, follow=True)

            # Check to see if 200 code was returned, which indicates success

            self.assertEqual(post_resp_for_rock_paper_scissors_game_url.status_code, 200)

            # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse
            rps_response_data = post_resp_for_rock_paper_scissors_game_url.json()

            # Checking whether the user choice was set correctly

            self.assertEqual(rps_response_data['user_rps_choice'], user_attempts[i])

            # Checking whether the computer choice was set correctly
            
            self.assertEqual(rps_response_data['computer_rps_choice'], computer_attempts[i])

            # Checking to see if this outcome would be a loss, as it should be

            self.assertEqual(rps_response_data['rps_round_outcome'], 'lose')

        # Checking whether the outcome of the game is that the user lost, as it should be

        self.assertEqual(rps_response_data['rps_end_of_game'], 'Game Over! You failed to win this game! Good luck next time!')
    
    # Method - simulating a situation where the user has won the game
    @patch('rock_paper_scissors.views.random.choice')
    def test_simultating_user_winning_rock_paper_scissors_game(self, mock_choice):
        # Added successful attempts from the user. This is because we are simulating a game where the user wins.
        user_attempts = ["paper", "scissors", "rock"]

        # Adding failed attempts from the computer, as the computer has to lose in this scenario.
        computer_attempts = ["rock", "paper", "scissors"]

        mock_choice.return_value = computer_attempts[0]

        # Navigating to the rps_form_submitted view, which will then be used for the GET and POST requests
        rock_paper_scissors_game_url_form = reverse('rock_paper_scissors:rps_form_submitted')

        # GET request made, which would open the rps game page
        get_response_for_rock_paper_scissors_game_url = self.client.get(rock_paper_scissors_game_url_form)

        # Check to see if 200 code was returned, which indicates success

        self.assertEqual(get_response_for_rock_paper_scissors_game_url.status_code, 200)

        for i in range(0, len(user_attempts)):
            # Setting the RPS option for the computer, as per the computer_attempts list.
            mock_choice.return_value = computer_attempts[i]

            # Setting the RPS option for the user, as per the user_attempts list.
            user_data = {
                'carousel_value' : user_attempts[i]
            }

            # Making a POST request, sending the data such as the user option in the POST request
            post_resp_for_rock_paper_scissors_game_url = self.client.post(rock_paper_scissors_game_url_form, user_data, follow=True)

            # Check to see if 200 code was returned, which indicates success

            self.assertEqual(post_resp_for_rock_paper_scissors_game_url.status_code, 200)

            # In order to assert whether the values are equal to the expected ones, we need to use json so that it is easy to parse
            rps_response_data = post_resp_for_rock_paper_scissors_game_url.json()

            # Checking whether the user choice was set correctly

            self.assertEqual(rps_response_data['user_rps_choice'], user_attempts[i])

            # Checking whether the computer choice was set correctly
            
            self.assertEqual(rps_response_data['computer_rps_choice'], computer_attempts[i])

            # Checking to see if this outcome would be a loss, as it should be

            self.assertEqual(rps_response_data['rps_round_outcome'], 'win')

        # Checking whether the outcome of the game is that the user won, as it should be

        self.assertEqual(rps_response_data['rps_end_of_game'], 'Game Over! You won this game! You have received 10 points!')

        game_user_profile = self.create_user_game_profile()

        # Checking whether the outcome of the game is that the user won, as it should be

        self.assertEqual(rps_response_data['rps_end_of_game'], 'Game Over! You won this game! You have received 10 points!')

        # Checking to see if the user won the game and if they did, add 10 points to their score

        if rps_response_data['rps_end_of_game'] == "Game Over! You won this game! You have received 10 points!":
            game_user_profile.current_score = 10
        
        # Check whether the user has 10 points, which indicates that they won the game
        
        self.assertEqual(game_user_profile.current_score, 10)