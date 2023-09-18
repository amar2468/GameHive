from django.test import TestCase
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib.auth.models import User

class RegistrationTestCase(TestCase):
    def testing_valid_reg_form(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        form = RegistrationForm(data=data)

        self.assertTrue(form.is_valid())
    
    def testing_invalid_reg_form(self):
        data = {}

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())
    
    def testing_empty_username_field(self):

        data = {
            'username': '', # empty username
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['This field is required.'])
    
    def testing_empty_email_field(self):

        data = {
            'username': 'testuser',
            'email': '', # empty email
            'password': 'testpassword'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def testing_empty_password_field(self):

        data = {
            'username': 'testuser',
            'email': '',
            'password': '' # empty password
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'], ['This field is required.'])