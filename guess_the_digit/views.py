from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def check_if_works(request):
    return render(request, 'home.html')