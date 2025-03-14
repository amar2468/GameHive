from django.shortcuts import render
from .forms import GuessTheNumberInputForm
import random
from gamehive.models import GameUserProfile

# Guess the digit game functionality in the view below
def guess_the_digit_game(request):
    if request.user.is_authenticated:
        global number_of_guesses
        global level
        global specific_hint
        if request.method == "POST":

            form = GuessTheNumberInputForm(request.POST)

            if form.is_valid():
                # Take the guess from the user
                user_guess = int(request.POST.get('guess_number_input_field', ''))

                # Extract the random number that will be the correct number
                correct_number = request.session.get('correct_number')

                # Creating a result string which will hold the prompt from the program (whether user has guessed right or not)
                result = ""

                if user_guess == correct_number:
                    result = "Correct guess! Well done!"

                    if level == "easy":
                        # No hints were enabled, so user gets the full score
                        if specific_hint == "":
                            try:
                                game_user_profile = GameUserProfile.objects.get(user=request.user)
                            except GameUserProfile.DoesNotExist:
                                game_user_profile = GameUserProfile(user=request.user)
                            
                            game_user_profile.current_score += 10
                            game_user_profile.save()
                        # Hints were enabled, half the score, regardless of level
                        else:
                            try:
                                game_user_profile = GameUserProfile.objects.get(user=request.user)
                            except GameUserProfile.DoesNotExist:
                                game_user_profile = GameUserProfile(user=request.user)
                            
                            game_user_profile.current_score += 5
                            game_user_profile.save()

                    elif level == "medium":

                        # No hints were enabled, so user gets the full score
                        if specific_hint == "":
                            try:
                                game_user_profile = GameUserProfile.objects.get(user=request.user)
                            except GameUserProfile.DoesNotExist:
                                game_user_profile = GameUserProfile(user=request.user)

                            game_user_profile.current_score += 50      
                            game_user_profile.save()   

                        # Hints were enabled, half the score, regardless of level
                        else:
                            try:
                                game_user_profile = GameUserProfile.objects.get(user=request.user)
                            except GameUserProfile.DoesNotExist:
                                game_user_profile = GameUserProfile(user=request.user)
                            
                            game_user_profile.current_score += 25
                            game_user_profile.save()

                    elif level == "hard":
                        # No hints were enabled, so user gets the full score
                        if specific_hint == "":
                            try:
                                game_user_profile = GameUserProfile.objects.get(user=request.user)
                            except GameUserProfile.DoesNotExist:
                                game_user_profile = GameUserProfile(user=request.user)

                            game_user_profile.current_score += 100
                            game_user_profile.save()

                        # Hints were enabled, half the score, regardless of level
                        else:
                            try:
                                game_user_profile = GameUserProfile.objects.get(user=request.user)
                            except GameUserProfile.DoesNotExist:
                                game_user_profile = GameUserProfile(user=request.user)
                            
                            game_user_profile.current_score += 75
                            game_user_profile.save()

                elif user_guess != correct_number and number_of_guesses != 0:
                    number_of_guesses -= 1

                    if number_of_guesses != 0:
                        result = "Wrong guess! Try again!"
                    else:
                        result = "Game over! The correct number was " + str(correct_number)
                        request.session.pop('correct_number', None)
                
                try:
                    game_user_profile = GameUserProfile.objects.get(user=request.user)
                except GameUserProfile.DoesNotExist:
                    game_user_profile = GameUserProfile(user=request.user)
                    game_user_profile.save()

                # The result is stored in the context so it can be returned back to the html template
                
                context = {
                    'result': result,
                    'latest_score': game_user_profile.current_score,
                    'specific_hint' : specific_hint,
                    'level' : level,
                    'correct_number' : correct_number
                }


                return render(request, 'home.html', context)
        
        level = request.GET.get('selected_level')

        hints = request.GET.get('hints')

        correct_number = request.session.get('correct_number')

        # Generate the hint (if number is odd or even) depending on the current_score condition
        def create_hint(odd_or_even):
            if hints == "yes":
                if odd_or_even % 2 == 0:
                    return "The number is even"
                else:
                    return "The number is odd"
            else:
                return ""

        # Check if the correct number has been specified in the current_score session
        if 'correct_number' not in request.session:

            # If the level is easy, generate a random number between 1 and 10
            if level == 'easy':
                request.session['correct_number'] = random.randint(1,10)

                specific_hint = create_hint(request.session['correct_number'])

                if specific_hint == "":
                    number_of_guesses = 4
                else:
                    number_of_guesses = 2
            
            # If the level is medium, generate a random number between 1 and 50
            elif level == 'medium':
                request.session['correct_number'] = random.randint(1,50)

                specific_hint = create_hint(request.session['correct_number'])

                if specific_hint == "":
                    number_of_guesses = 10
                else:
                    number_of_guesses = 5

            # If the level is hard, generate a random number between 1 and 100
            elif level == 'hard':
                request.session['correct_number'] = random.randint(1,100)

                specific_hint = create_hint(request.session['correct_number'])

                if specific_hint == "":
                    number_of_guesses = 20
                else:
                    number_of_guesses = 11
                    
        # If the correct number has already been specified, it needs to be re-generated
        if 'correct_number' in request.session:

            # If the level is easy, generate a random number between 1 and 10
            if level == 'easy':
                request.session.pop('correct_number', None)
                request.session['correct_number'] = random.randint(1,10)

                specific_hint = create_hint(request.session['correct_number'])

                if specific_hint == "":
                    number_of_guesses = 4
                else:
                    number_of_guesses = 2
            
            # If the level is medium, generate a random number between 1 and 50
            elif level == 'medium':
                request.session.pop('correct_number', None)
                request.session['correct_number'] = random.randint(1,50)
                
                specific_hint = create_hint(request.session['correct_number'])

                if specific_hint == "":
                    number_of_guesses = 10
                else:
                    number_of_guesses = 5

            # If the level is hard, generate a random number between 1 and 100
            elif level == 'hard':
                request.session.pop('correct_number', None)
                request.session['correct_number'] = random.randint(1,100)

                specific_hint = create_hint(request.session['correct_number'])

                if specific_hint == "":
                    number_of_guesses = 20
                else:
                    number_of_guesses = 11
        
        try:
            game_user_profile = GameUserProfile.objects.get(user=request.user)

            latest_score = game_user_profile.current_score
        except GameUserProfile.DoesNotExist:
            latest_score = 0
        
        correct_number = request.session['correct_number']

        context = {
            'specific_hint' : specific_hint,
            'level' : level,
            'latest_score' : latest_score,
            'correct_number' : correct_number
        }

        return render(request, 'home.html', context)
    else:
        return render(request, '403.html')

# View that presents the configuration page for the guessing game
def guess_the_digit_config(request):
    if request.user.is_authenticated:
        return render(request, 'guessing_game_config.html')
    else:
        return render(request, '403.html')