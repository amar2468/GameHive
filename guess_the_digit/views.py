from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random


guess = 3

# Guess the digit game functionality in the view below

@login_required
def guess_the_digit_game(request):
    global guess
    if request.method == "POST":

        user_guess = int(request.POST.get('guess_number_input_field', ''))

        correct_number = request.session.get('correct_number')

        result = ""

        if user_guess == correct_number:
            result = "Correct guess! Well done!"
        elif user_guess != correct_number and guess == 0:
            result = "Game over! The correct number was " + str(correct_number)
            request.session.pop('correct_number', None)
        elif user_guess != correct_number and guess != 0:
            result = "Wrong guess! Try again!"
            guess -= 1
        
        context = {
            'result': result
        }

        return render(request, 'home.html', context)
    
    if 'correct_number' not in request.session:
        request.session['correct_number'] = random.randint(1,10)
    return render(request, 'home.html')