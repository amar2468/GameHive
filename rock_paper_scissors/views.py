from django.shortcuts import render
from django.http import JsonResponse
from gamehive.models import GameUserProfile
import random


# This view allows a user to play single player mode, which will load the relevant template

def single_player_rps(request):
    if request.user.is_authenticated:
        return render(request, 'rock_paper_scissors_play.html')
    else:
        return render(request, '403.html')

# This view allows a user to open the config page, so that they can select the room id, in order to set up the game
def multiplayer_rps_config(request):
    if request.user.is_authenticated:
        return render(request, 'config_rock_paper_scissors_multiplayer.html')
    else:
        return render(request, '403.html')

# This view sends the user to the multiplayer game page
def multiplayer_rps_start_game(request):
    if request.user.is_authenticated:
        room_id = request.POST.get('room_id', '1')

        return render(request, "multiplayer_rock_paper_scissors_play.html", {"room_id": room_id})
    else:
        return render(request, '403.html')

# This view will allow the computer to choose a random option (rock,paper, or scissors) and inform the user of the choice.
# Additionally, the user's choice is compared against the computer's choice and an outcome is returned to the user (win,lose,draw)

def rps_form_submitted(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            attempts = request.session.get('attempts', 3)

            total_wins = request.session.get('total_wins', 0)

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

            if attempts > 0:
                attempts -= 1
                request.session['attempts'] = attempts

                # Using the rps_outcomes dictionary, the key (user's choice) will be found and the value (the computer's choice)
                # will be the value in the dictionary. If it is a draw, a draw will be returned
                rps_outcome = rps_outcomes[user_rps_choice].get(computer_rps_choice, 'draw')

                if rps_outcome == "win":
                    total_wins += 1
                    request.session['total_wins'] = total_wins

                # Adding the user's choice, computer's choice, and the outcome of the round back to the user so they are informed
                response_info = {
                    'computer_rps_choice' : computer_rps_choice,
                    'user_rps_choice' : user_rps_choice,
                    'rps_outcome': rps_outcome,
                    'attempts' : attempts
                }
            else:
                # Remove the "attempts" session variable as the round has finished so it should be reset back to 3 attempts for the new one

                del request.session['attempts']

                # In every round, the user has three attempts. If they get 2 or more attempts correct, they won that round. Hence 10
                # points would be added to their total score

                if 'total_wins' in request.session:
                    if request.session['total_wins'] >= 2:
                            rps_outcome = "Game Over! You won this round! You have received 10 points!"
                            try:
                                game_user_profile = GameUserProfile.objects.get(user=request.user)
                            except GameUserProfile.DoesNotExist:
                                game_user_profile = GameUserProfile(user=request.user)
                            game_user_profile.current_score += 10
                            game_user_profile.save()
                    else:
                        rps_outcome = "Game Over! You failed to win this round! Good luck next time!"

                    # Remove the "total_score" session variable as the score has been saved in the GameUserProfile custom model
                
                    del request.session['total_wins']
                
                else:
                    rps_outcome = "Game Over! You failed to win this round! Good luck next time!"

                # Adding the user's choice, computer's choice, and informing user that the round is over
                response_info = {
                    'computer_rps_choice' : computer_rps_choice,
                    'user_rps_choice' : user_rps_choice,
                    'rps_outcome': rps_outcome
                }

            # Returning the dictionary in JSON format to jQuery, which will then be inserted into the HTML template
            return JsonResponse(response_info)
        return render(request, 'rock_paper_scissors_play.html')
    else:
        return render(request, '403.html')