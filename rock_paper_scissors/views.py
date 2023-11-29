from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
import random


# This view opens the game for the user, which will allow them to select an option (rock,paper, or scissors)

def play(request):
    return render(request, 'rock_paper_scissors_play.html')

# This view will allow the computer to choose a random option (rock,paper, or scissors) and inform the user of the choice
# Note: This view is STILL BEING DEVELOPED.

def rps_form_submitted(request):
    if request.method == "POST":
        computer_choice_between_rps = ["Rock", "Paper", "Scissors"]

        computer_rps_choice = random.choice(computer_choice_between_rps)

        return JsonResponse({'computer_rps_choice' : computer_rps_choice})
    return render(request, 'rock_paper_scissors_play.html')

# This view will update the personal details of the user (email, first name, and surname) - STILL BEING DEVELOPED

def update_personal_details(request):

    user_entries = User.objects.all()

    for user in user_entries:
        if user.username == request.user:
            if change_email != user.email:
                pass

    change_first_name = request.POST.get('change_first_name')
    change_surname = request.POST.get('change_surname')
    change_email = request.POST.get('change_email')

    return render(request, 'profile.html')

# This view will update the passsword of the user - STILL BEING DEVELOPED

def change_password(request):
    change_password = request.POST.get('change_password')
    change_password_confirm = request.POST.get('change_password_confirm')

    print(change_password)
    print(change_password_confirm)
    
    return render(request, 'profile.html')