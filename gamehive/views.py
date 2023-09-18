from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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

            User.objects.create_user(username=username, email=email, password=password)

            return render(request, 'login.html')
        if not form.is_valid():
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'sign_up.html', {'form': form})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'about.html')
    return render(request, 'login.html')
        