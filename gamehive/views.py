from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from gamehive.models import GameUserProfile

def homepage(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def testimonials_page(request):
    return render(request, 'testimonials.html')

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
    return render(request, 'sign_up.html', {'form': form})

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

    return render(request, 'login.html')

# Logout functionality
def log_out(request):

    # The user will be logged out after this method is executed
    logout(request)

    # Return to the homepage
    return redirect('homepage')