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
        elif user_guess != correct_number and number_of_guesses != 0:
            number_of_guesses -= 1

            if number_of_guesses != 0:
                result = "Wrong guess! Try again!"
            else:
                result = "Game over! The correct number was " + str(correct_number)
                request.session.pop('correct_number', None)
        
        # The result is stored in the context so it can be returned back to the html template
        context = {
            'result': result
        }

        return render(request, 'home.html', context)
    
    number_of_guesses = int(request.GET.get('number_of_guesses', ''))
    level = request.GET.get('selected_level')

    # Check if the correct number has been specified in the current session
    if 'correct_number' not in request.session:

        # If the level is easy, generate a random number between 1 and 10
        if level == 'easy':
            request.session['correct_number'] = random.randint(1,10)
        
        # If the level is medium, generate a random number between 1 and 50
        elif level == 'medium':
            request.session['correct_number'] = random.randint(1,50)

        # If the level is hard, generate a random number between 1 and 100
        elif level == 'hard':
            request.session['correct_number'] = random.randint(1,100)
    # If the correct number has already been specified, it needs to be re-generated
    if 'correct_number' in request.session:

        # If the level is easy, generate a random number between 1 and 10
        if level == 'easy':
            request.session.pop('correct_number', None)
            request.session['correct_number'] = random.randint(1,10)
        
        # If the level is medium, generate a random number between 1 and 50
        elif level == 'medium':
            request.session.pop('correct_number', None)
            request.session['correct_number'] = random.randint(1,50)

        # If the level is hard, generate a random number between 1 and 100
        elif level == 'hard':
            request.session.pop('correct_number', None)
            request.session['correct_number'] = random.randint(1,100)

    return render(request, 'home.html')

# View that presents the configuration page for the guessing game
def guess_the_digit_config(request):
    return render(request, 'guessing_game_config.html')