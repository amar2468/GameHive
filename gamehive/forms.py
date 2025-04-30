from django import forms
from django.core.exceptions import ValidationError

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 20
RESERVED_WORDS = ['admin', 'root', 'moderator']

# Listing all the options in the "dropdown" menu for "Request Type" field in the Customer Support section.
customer_request_options = [
    ("delete_user_account", "Delete Your Account"),
    ("edit_user_account", "Edit Your Account"),
    ("cancel_user_purchase", "Cancel Your Purchase"),
    ("general_requests", "General Requests")
]

# Listing all the options in the "dropdown" menu for "User Type" field in the "Edit User Profile" section.
user_type_options = [
    ("user", "User"),
    ("admin", "Admin"),
    ("super_admin", "SuperAdmin")
]

def validate_username(username):
    if len(username) < MIN_USERNAME_LENGTH:
        raise ValidationError(f"Username must be at least {MIN_USERNAME_LENGTH} characters long.")
    if len(username) > MAX_USERNAME_LENGTH:
        raise ValidationError(f"Username must be no longer than {MAX_USERNAME_LENGTH} characters.")
    if ' ' in username or any(char.isspace() for char in username):
        raise ValidationError("Username cannot contain spaces.")
    if not username.isalnum():
        raise ValidationError("Username cannot contain special characters.")
    if username.lower() in (word.lower() for word in RESERVED_WORDS):
        raise ValidationError("Username is not allowed.")

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH, required=True, validators=[validate_username])
    name = forms.CharField(max_length=25, required=True)
    surname = forms.CharField(max_length=25, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH, required=True, validators=[validate_username])
    password = forms.CharField(required=True)

class ForgotPasswordForm(forms.Form):
    user_email_for_pwd_reset = forms.EmailField(required=True)

class TestimonialsForm(forms.Form):
    testimonial_message = forms.CharField(required=True)
    star_rating = forms.IntegerField()

class UpdatePersonalDetails(forms.Form):
    change_first_name = forms.CharField(max_length=25, required=True)
    change_surname = forms.CharField(max_length=25, required=True)
    change_email = forms.EmailField(required=True)

class ChangePasswordForm(forms.Form):
    change_password = forms.CharField(required=True)
    change_password_confirm = forms.CharField(required=True)

class BuyItemForm(forms.Form):
    price_for_item_in_points = forms.IntegerField()

class CustomerSupportForm(forms.Form):
    customer_username = forms.CharField(max_length=MAX_USERNAME_LENGTH, required=True)
    customer_email = forms.EmailField(required=True)
    customer_request_type = forms.ChoiceField(choices=customer_request_options, required=True)
    customer_title_of_request = forms.CharField(max_length=150, required=True)
    customer_ticket_description = forms.CharField(required=True)
    customer_ticket_attachments = forms.FileField(required=False)

class AdminEditUserProfileForm(forms.Form):
    edit_first_name = forms.CharField(max_length=25, required=True)
    edit_last_name = forms.CharField(max_length=25, required=True)
    edit_username = forms.CharField(max_length=MAX_USERNAME_LENGTH, required=True, validators=[validate_username])
    edit_email = forms.EmailField(required=True)
    edit_user_game_score = forms.IntegerField()
    edit_user_type = forms.ChoiceField(choices=user_type_options, required=True)