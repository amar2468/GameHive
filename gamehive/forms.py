from django import forms
from django.core.exceptions import ValidationError

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 20
RESERVED_WORDS = ['admin', 'root', 'moderator']

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
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH, required=True, validators=[validate_username])
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class ForgotPasswordForm(forms.Form):
    user_email_for_pwd_reset = forms.EmailField(required=True)

class TestimonialsForm(forms.Form):
    testimonial_message = forms.CharField(widget=forms.Textarea, required=True)
    star_rating = forms.IntegerField()

class UpdatePersonalDetails(forms.Form):
    change_first_name = forms.CharField(max_length=25, required=True)
    change_surname = forms.CharField(max_length=25, required=True)
    change_email = forms.EmailField(required=True)

class ChangePasswordForm(forms.Form):
    change_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    change_password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True)

class BuyItemForm(forms.Form):
    price_for_item_in_points = forms.IntegerField()