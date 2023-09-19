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
    
    def testing_incorrect_email_field(self):
        # Testing email without .com part

        data = {
            'username': 'testuser',
            'email': 'amar@gmail',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing email without gmail.com part


        data = {
            'username': 'testuser',
            'email': 'amar@',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing email with local name but without domain name

        data = {
            'username': 'testuser',
            'email': 'amar@',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing email with weird characters

        data = {
            'username': 'testuser',
            'email': '&"*"*"@gmail.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test missing @gmail part

        data = {
            'username': 'testuser',
            'email': 'amar.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing spaces in email

        data = {
            'username': 'testuser',
            'email': 'amar pla@gmail.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Excessive length emails

        data = {
            'username': 'testuser',
            'email': 'a'*1000 + '@' + 'b'*1000 + '.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing non-ASCII email

        data = {
            'username': 'testuser',
            'email': 'юзер@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())
    
    def testing_invalid_username(self):
        # Test if username length is less than required minimum length (3)

        data = {
            'username': 'te',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test if username length is more than the required maximum length (20)

        data = {
            'username': 'usernameisthebestasdf',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test if username has spaces

        data = {
            'username': 'test user',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())
        
        # Test if username has special characters

        data = {
            'username': 'test!*',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test if username contains reserved words

        data = {
            'username': 'admin',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())