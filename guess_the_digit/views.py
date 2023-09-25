from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random

# Guess the digit game functionality in the view below

@login_required
def guess_the_digit_game(request):
    global number_of_guesses
    if request.method == "POST":

        # Take the guess from the user
        user_guess = int(request.POST.get('guess_number_input_field', ''))

        # Extract the random number that will be the correct number
        correct_number = request.session.get('correct_number')

        # Creating a result string which will hold the prompt from the program (whether user has guessed right or not)
        result = ""

        if user_guess == correct_number:
            result = "Correct guess! Well done!"
        elif user_guess != correct_number and number_of_guesses == 0:
            result = "Game over! The correct number was " + str(correct_number)
            request.session.pop('correct_number', None)
        elif user_guess != correct_number and number_of_guesses != 0:
            result = "Wrong guess! Try again!"
            number_of_guesses -= 1
        
        # The result is stored in the context so it can be returned back to the html template
        context = {
            'result': result
        }

        return render(request, 'home.html', context)
    
    # Check if the correct number has been specified in the current session
    if 'correct_number' not in request.session:
        request.session['correct_number'] = random.randint(1,10)

    number_of_guesses = int(request.GET.get('number_of_guesses', ''))
    level = request.GET.get('selected_level')
    return render(request, 'home.html')

# View that presents the configuration page for the guessing game
def guess_the_digit_config(request):
    return render(request, 'guessing_game_config.html')