from django.test import TestCase, Client
from .forms import GuessTheNumberInputForm
from django.urls import reverse
from django.contrib.auth.models import User

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