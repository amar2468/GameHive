from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
import random


# This view opens the game for the user, which will allow them to select an option (rock,paper, or scissors)

def play(request):
    return render(request, 'rock_paper_scissors_play.html')

# This view will allow the computer to choose a random option (rock,paper, or scissors) and inform the user of the choice.
# Additionally, the user's choice is compared against the computer's choice and an outcome is returned to the user (win,lose,draw)
# Note: This view is STILL BEING DEVELOPED.

def rps_form_submitted(request):
    if request.method == "POST":

        user_rps_choice = request.POST.get('carousel_value', '')

        # Determine all the possible outcomes for the rock, paper, scissors game
        rps_outcomes = {
            'rock' : {'paper' : 'lose', 'scissors' : 'win'},
            'paper' : {'rock' : 'win', 'scissors' : 'lose'},
            'scissors' : {'rock' : 'lose', 'paper' : 'win'}
        }

        computer_choice_between_rps = ["rock", "paper", "scissors"]

        # Pick a random item from the rock,paper,scissors list (presented as computer's choice)
        computer_rps_choice = random.choice(computer_choice_between_rps)

        # Using the rps_outcomes dictionary, the key (user's choice) will be found and the value (the computer's choice)
        # will be the value in the dictionary. If it is a draw, a draw will be returned
        rps_outcome = rps_outcomes[user_rps_choice].get(computer_rps_choice, 'draw')

        # Adding the user's choice, computer's choice, and the outcome of the round back to the user so they are informed
        response_info = {
            'computer_rps_choice' : computer_rps_choice,
            'user_rps_choice' : user_rps_choice,
            'rps_outcome': rps_outcome
        }

        # Returning the dictionary in JSON format to jQuery, which will then be inserted into the HTML template
        return JsonResponse(response_info)
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