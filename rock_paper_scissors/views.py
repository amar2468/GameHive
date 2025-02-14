from django.shortcuts import render
from django.http import JsonResponse
from gamehive.models import GameUserProfile
import random

# Creating a variable that stores the total number of wins required to win the game
WINS_REQUIRED_TO_WIN_GAME = 3

# This view allows a user to play single player mode, which will load the relevant template

def single_player_rps(request):
    # If the user is logged in, this block will be run.
    if request.user.is_authenticated:
        # Try to remove "rounds", "user_total_wins", and "computer_wins" session variables, as they should be reset after every game.
        try:
            if 'rounds' in request.session:
                del request.session['rounds']
            if 'user_total_wins' in request.session:
                del request.session['user_total_wins']
            if 'computer_wins' in request.session:
                del request.session['computer_wins']
        # If the session variable "rounds" does not exist, we will just move on with the code
        except KeyError:
            print("Error: One or more of the session variable(s) do not exist.")
        
        return render(request, 'rock_paper_scissors_play.html')
    else:
        return render(request, '403.html')

# This view sends the user to the multiplayer game page
def multiplayer_rps_start_game(request):
    if request.user.is_authenticated:
        return render(request, "multiplayer_rock_paper_scissors_play.html")
    else:
        return render(request, '403.html')

# This view will allow the computer to choose a random option (rock,paper, or scissors) and inform the user of the choice.
# Additionally, the user's choice is compared against the computer's choice and an outcome is returned to the user (win,lose,draw)

def rps_form_submitted(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            rounds = request.session.get('rounds', 0)

            user_total_wins = request.session.get('user_total_wins', 0)

            computer_wins = request.session.get('computer_wins', 0)

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
            rps_round_outcome = rps_outcomes[user_rps_choice].get(computer_rps_choice, 'draw')

            if rps_round_outcome == "win":
                user_total_wins += 1
                request.session['user_total_wins'] = user_total_wins
            elif rps_round_outcome == "lose":
                computer_wins += 1
                request.session['computer_wins'] = computer_wins
            
            # Increasing the round number
            rounds += 1
            request.session['rounds'] = rounds

            # If the user has managed to win 3 rounds first, the points will be added to their account.
            if 'user_total_wins' in request.session and request.session['user_total_wins'] == WINS_REQUIRED_TO_WIN_GAME:
                rps_end_of_game = ""
                rps_end_of_game = "Game Over! You won this game! You have received 10 points!"
                try:
                    game_user_profile = GameUserProfile.objects.get(user=request.user)
                except GameUserProfile.DoesNotExist:
                    game_user_profile = GameUserProfile(user=request.user)
                game_user_profile.current_score += 10
                game_user_profile.save()

                # Remove the "user_total_wins" session variable as the score has been saved in the GameUserProfile custom model
                # and we don't want the number of wins to be remembered in the new game that gets loaded.
                del request.session['user_total_wins']

                if 'computer_wins' in request.session:
                    # Remove the "computer_wins" session variable as we don't want the number of wins to be remembered
                    # in the new game that gets loaded.
                    del request.session['computer_wins']

                response_info = {
                    'round_number' : rounds,
                    'computer_rps_choice' : computer_rps_choice,
                    'user_rps_choice' : user_rps_choice,
                    'user_total_wins' : user_total_wins,
                    'computer_wins' : computer_wins,
                    'rps_round_outcome': rps_round_outcome,
                    'rps_end_of_game': rps_end_of_game
                }
            
            # If the computer won three rounds before the user, the user will get a message that they lost.
            elif 'computer_wins' in request.session and request.session['computer_wins'] == WINS_REQUIRED_TO_WIN_GAME:
                rps_end_of_game = ""        
                rps_end_of_game = "Game Over! You failed to win this game! Good luck next time!"

                if 'user_total_wins' in request.session:
                    # Remove the "user_total_wins" session variable as the score has been saved in the GameUserProfile custom model
                    # and we don't want the number of wins to be remembered in the new game that gets loaded.
                    del request.session['user_total_wins']

                # Remove the "computer_wins" session variable as we don't want the number of wins to be remembered
                # in the new game that gets loaded.
                del request.session['computer_wins']

                response_info = {
                    'round_number' : rounds,
                    'computer_rps_choice' : computer_rps_choice,
                    'user_rps_choice' : user_rps_choice,
                    'user_total_wins' : user_total_wins,
                    'computer_wins' : computer_wins,
                    'rps_round_outcome': rps_round_outcome,
                    'rps_end_of_game': rps_end_of_game
                }
            
            else:
                # Sending multiple variables back to the front-end, so that they can be displayed on the screen.
                response_info = {
                    'computer_rps_choice' : computer_rps_choice,
                    'user_rps_choice' : user_rps_choice,
                    'rps_round_outcome': rps_round_outcome,
                    'user_total_wins' : user_total_wins,
                    'computer_wins' : computer_wins,
                    'round_number' : rounds,
                    'rps_end_of_game' : ""
                }
            
            # Returning the dictionary in JSON format to jQuery, which will then be inserted into the HTML template
            return JsonResponse(response_info)

        else:
            return render(request, 'rock_paper_scissors_play.html')
    else:
        return render(request, '403.html')