from django.test import TestCase, Client
from django.urls import reverse
from .forms import RegistrationForm, TestimonialsForm, UpdatePersonalDetails, ChangePasswordForm
from gamehive.models import CustomUser
import json


# Unit test in the "RegistrationTestCase" class below

class RegistrationTestCase(TestCase):
    def testing_valid_reg_form(self):
        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
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
            'name': 'test',
            'surname': 'user',
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
            'name': 'test',
            'surname': 'user',
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
            'name': 'test',
            'surname': 'user',
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
            'name': 'test',
            'surname': 'user',
            'email': 'amar@gmail',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing email without gmail.com part


        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing email with local name but without domain name

        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing email with weird characters

        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': '&"*"*"@gmail.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test missing @gmail part

        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': 'amar.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing spaces in email

        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': 'amar pla@gmail.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Excessive length emails

        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': 'a'*1000 + '@' + 'b'*1000 + '.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Testing non-ASCII email

        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': 'юзер@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())
    
    def testing_invalid_username(self):
        # Test if username length is less than required minimum length (3)

        data = {
            'username': 'te',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test if username length is more than the required maximum length (20)

        data = {
            'username': 'usernameisthebestasdf',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test if username has spaces

        data = {
            'username': 'test user',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())
        
        # Test if username has special characters

        data = {
            'username': 'test!*',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

        # Test if username contains reserved words

        data = {
            'username': 'admin',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@example.com',
            'password': 'Strongpassword12!'
        }

        form = RegistrationForm(data=data)

        self.assertFalse(form.is_valid())

# Integration test for the registration functionality is below

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
                                                          'name': 'test',
                                                          'surname': 'user',
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
                                                          'name': 'test',
                                                          'surname': 'user',
                                                          'email': 'amar@gmail.com',
                                                          'password': strong_password
                                                      })
        
        # Verify that there are no password validation errors in the response
        self.assertNotContains(response_for_strong_password, "This password is too short.")

    def test_user_created_in_database(self):
        # Defining data to put into post

        data = {
            'username': 'testuser',
            'name': 'test',
            'surname': 'user',
            'email': 'amar@gmail.com',
            'password': 'StrOngp@assword'
        }

        # Making a POST request for registration view

        registration_url = reverse('sign_up')

        # Making a POST request for registration url, adding data and setting follow to True which enables HTTP redirects
        response_registration = self.client.post(registration_url, data, follow=True)

        # Verify that user was created
        self.assertEqual(response_registration.status_code, 200) # Check to see if 200 code was returned, which indicates success

        self.assertTrue(CustomUser.objects.filter(username='testuser').exists()) # See if user exists in database

# Integration test for the login functionality is below

class LoginIntegrationTestCase(TestCase):
    
    def test_for_login_process(self):

        # Created test user to attempt the login process
        self.user = CustomUser.objects.create_user(
            username='david12',
            first_name='test',
            last_name='user',
            password='Whatis12!',
            account_type="user"
        )

        # Login data below
        data = {
            'username': 'david12',
            'password': 'Whatis12!'
        }

        # POST request for login process
        login_url = reverse('login')

        response_for_login = self.client.post(login_url, data, follow=True)

        # Saving the content that was returned from the POST request
        response_for_login_content = response_for_login.content

        # As this is a b-string, we need to change it to a string
        response_for_login_content_str = response_for_login_content.decode("utf-8")

        # Converting the str to a dict, so that we can access the "success" key.
        response_for_login_content_dict = json.loads(response_for_login_content_str)

        # Check to see if login was successful
        self.assertEqual(response_for_login_content_dict.get("success"),"You have logged in successfully. Redirecting to the homepage...")

# Unit test in the "TestimonialsForm" class below

class TestimonialsFormTestCase(TestCase):
    def testing_valid_testimonials_form(self):
        data = {
            'testimonial_message' : 'Hello there!',
            'star_rating' : '5'
        }

        form = TestimonialsForm(data=data)

        self.assertTrue(form.is_valid())

    def testing_invalid_testimonials_form(self):
        data = {}

        form = TestimonialsForm(data=data)

        self.assertFalse(form.is_valid())

    def testing_empty_testimonial_message_field(self):

        data = {
            'testimonial_message' : ''
        }

        form = TestimonialsForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn('testimonial_message', form.errors)
        self.assertEqual(form.errors['testimonial_message'], ['This field is required.'])

# Integration test for the "TestimonialsForm" functionality is below

class TestimonialsFormIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', password='Password34*', account_type="user")
        self.client = Client()
    
    def test_for_testimonials_form_process(self):

        self.client.login(username='testuser', password='Password34*')

        # Data for the testimonial form is below. This will be tested.

        data = {
            'testimonial_message' : 'Hello there!'
        }

        # POST request for "testimonial form" process
        testimonials_url = reverse('testimonials_page')

        response_for_testimonials_url = self.client.post(testimonials_url, data, follow=True)

        # Verify for redirect

        self.assertEqual(response_for_testimonials_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

# Unit test in the "UpdatePersonalDetails" class below

class UpdatePersonalDetailsTestCase(TestCase):
    def test_update_personal_details_form(self):
        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'amar@gmail.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertTrue(form.is_valid())
    
    def test_empty_first_name_personal_details_form(self):
        data = {
            'change_first_name' : '',
            'change_surname' : 'Plakalo',
            'change_email' : 'amar@gmail.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())
    
    def test_empty_surname_personal_details_form(self):
        data = {
            'change_first_name' : 'Amar',
            'change_surname' : '',
            'change_email' : 'amar@gmail.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())
    
    def test_empty_email_personal_details_form(self):
        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : ''
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

    def test_empty_invalid_email_personal_details_form(self):
        
        # Testing email without .com part

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'amar@gmail'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

        # Testing email without gmail.com part

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'amar@'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

        # Testing email with weird characters

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : '&"*"*"@gmail.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

        # Test missing @gmail part

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'amar.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

        # Testing spaces in email

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'amar pla@gmail.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

        # Testing excessive length emails

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'a'*1000 + '@' + 'b'*1000 + '.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

        # Testing non-ASCII email

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'юзер@example.com'
        }

        form = UpdatePersonalDetails(data=data)

        self.assertFalse(form.is_valid())

# Integration test for the "UpdatePersonalDetails" functionality is below

class UpdatePersonalDetailsIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', password='Password34*', account_type="user")
        self.client = Client()
    
    def test_for_update_personal_details_process(self):

        self.client.login(username='testuser', password='Password34*')
        
        # Data for the update personal details form is below. This will be tested.

        data = {
            'change_first_name' : 'Amar',
            'change_surname' : 'Plakalo',
            'change_email' : 'amar@gmail.com'
        }

        # POST request for "Update Personal Details" process
        update_personal_details_url = reverse('update_personal_details')

        response_for_update_personal_details_url = self.client.post(update_personal_details_url, data, follow=True)

        # Verify for redirect

        self.assertEqual(response_for_update_personal_details_url.status_code, 200) # Check to see if 200 code was returned, which indicates success

# Unit test in the "ChangePasswordForm" class below

class ChangePasswordFormTestCase(TestCase):
    def testing_change_password_form(self):
        data = {
            'change_password' : 'Testpassword12!',
            'change_password_confirm' : 'Testpassword12!'
        }

        form = ChangePasswordForm(data=data)

        self.assertTrue(form.is_valid())

# Integration test for the "ChangePasswordForm" functionality is below

class ChangePasswordFormIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', password='Password34*', account_type="user")
        self.client = Client()
    
    def test_for_change_password_process(self):

        self.client.login(username='testuser', password='Password34*')

        # Data for the change password form is below. This will be tested.

        data = {
            'change_password' : 'Testpassword12!',
            'change_password_confirm' : 'Testpassword12!'
        }

        # POST request for "ChangePasswordForm" process
        change_password_form_url = reverse('change_password')

        response_for_change_password_form_url = self.client.post(change_password_form_url, data, follow=True)

        # Verify for redirect

        self.assertEqual(response_for_change_password_form_url.status_code, 200) # Check to see if 200 code was returned, which indicates success