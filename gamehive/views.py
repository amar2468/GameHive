from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign_up.html')