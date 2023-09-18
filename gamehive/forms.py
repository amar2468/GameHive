from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=25, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)