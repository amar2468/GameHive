from django.test import TestCase, Client
from .forms import RockPaperScissorsInputForm
from django.contrib.auth.models import User

# Unit Test for Rock, Paper, Scissors game

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