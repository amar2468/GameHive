from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

def homepage(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')

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

            User.objects.create_user(username=username, email=email, password=password)

            return render(request, 'login.html')
        if not form.is_valid():
            print(form.errors)
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
            print(form.errors)
    else:
        form = LoginForm()

    return render(request, 'login.html')
        