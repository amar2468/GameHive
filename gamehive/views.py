from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm,LoginForm, TestimonialsForm, ChangePasswordForm, UpdatePersonalDetails
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from gamehive.models import GameUserProfile,TestimonialsModel
from django.http import JsonResponse

# View that renders the homepage which allows a user to either sign up/login or play the game of their choice

def homepage(request):
    return render(request, 'index.html')

# Displays relevant information about the company

def about(request):
    return render(request, 'about.html')

# First part of this view is the POST method, which saves a testimonial to the relevant custom model. The else part will just display
# the page to the user without submitting any forms

def testimonials_page(request):
    if request.method == "POST":

        # Uses the TestimonialsForm in forms.py file which indicates the constraints (i.e. max length, validation)
        form = TestimonialsForm(request.POST)

        # If the form is valid (everything is filled in), the data that is posted (name,surname,testimonial message) will be 
        # cleaned and inserted into the testimonials model which will hold all the testimonials by users

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            testimonials_message = form.cleaned_data['testimonial_message']

            new_testimonial = TestimonialsModel(
                name=first_name,
                surname=last_name,
                message=testimonials_message,
            )

            new_testimonial.save()

            return render(request, 'testimonials.html')
        else:
            # This will iterate through the errors that have occurred (user entered a name that is too long, sent an empty form, etc..)
            # These errors will then be displayed in the testimonials page, so user can fix their errors and submit a valid form.

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return render(request, 'testimonials.html', {'form':form})
    else:
        return render(request, 'testimonials.html')

# View that will present the current leaderboard for all users

def my_profile(request):
    if request.user.is_authenticated:
        leaderboard_entries = GameUserProfile.objects.all().order_by('-current_score')
        return render(request, 'profile.html', {'leaderboard_entries': leaderboard_entries})
    else:
        return render(request, '403.html')
    
# This view will update the personal details of the user (email, first name, and surname) - STILL BEING DEVELOPED

def update_personal_details(request):
    if request.method == "POST":
        form = UpdatePersonalDetails(request.POST)

        if form.is_valid():
            change_first_name = form.cleaned_data['change_first_name']
            change_surname = form.cleaned_data['change_surname']
            change_email = form.cleaned_data['change_email']

            user_entries = User.objects.all()

            for user in user_entries:
                if user.username == request.user:
                    if change_email != user.email:
                        pass

            return render(request, 'profile.html')
    return render(request, 'profile.html')

# This view will update the passsword of the user - STILL BEING DEVELOPED

def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            change_password = form.cleaned_data['change_password']
            change_password_confirm = form.cleaned_data['change_password_confirm']

            if change_password != change_password_confirm:
                response_info_for_password = {
                    'passwords_match' : False
                }

            else:
                response_info_for_password = {
                    'passwords_match' : True
                }

            return JsonResponse(response_info_for_password)
            
    return render(request, 'profile.html')

# View has the POST part, which will take the user registration details and check if they are valid, after which the password will
# be validated. Finally, the user will be added to the user model and the current score will be set to 0 as the user has only been
# created. The other part will just display the sign up page to the user (when they initially decide to sign up, not when they submit it)

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return render(request, 'sign_up.html', {'form':form})

            user = User.objects.create_user(username=username, email=email, password=password)

            game_user_profile = GameUserProfile.objects.get_or_create(user=user)
            game_user_profile = game_user_profile[0]
            game_user_profile.current_score = 0
            game_user_profile.save()

            return render(request, 'login.html')
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return render(request, 'sign_up.html', {'form':form})
    else:
        form = RegistrationForm()
    if request.user.is_authenticated:
        return render(request, '403.html')
    else:
        return render(request, 'sign_up.html', {'form': form})

# Sign in view has the POST method, which will take the login form as submitted by user and check if it is valid, after which 
# authentication will occur. If a user is found, it will login the user. Otherwise, the login will not work and the user will be
# redirected back to the login page

def sign_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = LoginForm()

    if request.user.is_authenticated:
        return render(request, '403.html')
    else:
        return render(request, 'login.html')

# Logout functionality which simply logs out the user

def log_out(request):

    # Checks if user is logged in and will perform logout in that case
    if request.user.is_authenticated:
        # The user will be logged out after this method is executed
        logout(request)

        # Return to the homepage
        return redirect('homepage')
    
    # If user isn't logged in, the logout will not be allowed
    else:
        return render(request, '403.html')