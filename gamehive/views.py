from django.shortcuts import render, redirect
from .forms import RegistrationForm

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
            return redirect('')
    else:
        form = RegistrationForm()
    return render(request, 'sign_up.html', {'form': form})
        