from django import forms

class GuessTheNumberInputForm(forms.Form):
    guess_number_input_field = forms.IntegerField()