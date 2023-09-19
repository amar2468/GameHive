from django.test import TestCase
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


# Unit test in the "RegistrationTestCase" class below

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

# Integration test in the "RegistrationIntegrationTestCase" class below

class RegistrationIntegrationTestCase(TestCase):
    def test_user_registration_process(self):
        # Defining strong & weak password for testing
        strong_password = "StrOngp@sswOrd1"
        weak_password = "weak"

        # Set up sign up view URL

        registration_url = reverse('sign_up')

        # |Checking Whether Weak Password Is Detected |

        # Making a POST request with the vulnerable password

        response_for_weak_password = self.client.post(registration_url,
                                                      {
                                                          'username': 'testuser',
                                                          'email': 'amar@gmail.com',
                                                          'password': weak_password
                                                      })
        
        # Verify if there are any password validation errors in the response
        self.assertContains(response_for_weak_password, "This password is too short.")

        # |Checking Whether Strong Password Is Detected |

        # Making a POST request with the strong password

        response_for_strong_password = self.client.post(registration_url,
                                                      {
                                                          'username': 'testuser',
                                                          'email': 'amar@gmail.com',
                                                          'password': strong_password
                                                      })
        
        # Verify that there are no password validation errors in the response
        self.assertNotContains(response_for_strong_password, "This password is too short.")

    def test_user_created_in_database(self):
        # Defining data to put into post

        data = {
            'username': 'testuser',
            'email': 'amar@gmail.com',
            'password': 'StrOngp@assword'
        }

        # Making a POST request for registration view

        registration_url = reverse('sign_up')

        # Making a POST request for registration url, adding data and setting follow to True which enables HTTP redirects
        response_registration = self.client.post(registration_url, data, follow=True)

        # Verify that user was created
        self.assertEqual(response_registration.status_code, 200) # Check to see if 200 code was returned, which indicates success

        self.assertTrue(User.objects.filter(username='testuser').exists()) # See if user exists in database
