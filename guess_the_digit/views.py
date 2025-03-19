from django.shortcuts import render
from .forms import GuessTheNumberInputForm
import random
from gamehive.models import GameUserProfile

# Guess the digit game functionality in the view below
def guess_the_digit_game(request):
    if request.user.is_authenticated:

        # If the user wins a game, this function will be executed, taking in the number of points that the user won and saving it
        # to their record.
        def update_user_score(user_points_win):
            try:
                game_user_profile = GameUserProfile.objects.get(user=request.user)
            except GameUserProfile.DoesNotExist:
                game_user_profile = GameUserProfile(user=request.user)
            
            game_user_profile.current_score += user_points_win
            game_user_profile.save()
        
        # This function will take the guess range and the number of attempts depending on whether the hints were enabled
        # or disabled. Then, we will specify the exact number of attempts the user should get, depending on whether hints were
        # enabled or disabled.
        def generate_correct_number_and_set_no_of_attempts(number_range, attempts_easy_level_enabled, attempts_easy_level_disabled):
            request.session['correct_number'] = number_range

            specific_hint = create_hint(request.session['correct_number'])

            if specific_hint == "":
                number_of_guesses = attempts_easy_level_enabled
            else:
                number_of_guesses = attempts_easy_level_disabled
            
            response_obj = {
                'number_of_guesses' : number_of_guesses,
                'specific_hint' : specific_hint
            }

            return response_obj

        # Creating constant variables that will store each of the three levels in the game
        EASY_LEVEL = "easy"
        MEDIUM_LEVEL = "medium"
        HARD_LEVEL = "hard"

        # Defining the points won for each level and whether hints were enabled/disabled.
        EASY_LEVEL_HINTS_ENABLED_POINTS = 5
        EASY_LEVEL_HINTS_DISABLED_POINTS = 10

        MEDIUM_LEVEL_HINTS_ENABLED_POINTS = 25
        MEDIUM_LEVEL_HINTS_DISABLED_POINTS = 50

        HARD_LEVEL_HINTS_ENABLED_POINTS = 75
        HARD_LEVEL_HINTS_DISABLED_POINTS = 100

        # Defining the number of guesses, depending on the level and whether hints were enabled/disabled.

        EASY_LEVEL_ATTEMPTS_HINTS_ENABLED = 2
        EASY_LEVEL_ATTEMPTS_HINTS_DISABLED = 4

        MEDIUM_LEVEL_ATTEMPTS_HINTS_ENABLED = 5
        MEDIUM_LEVEL_ATTEMPTS_HINTS_DISABLED = 10

        HARD_LEVEL_ATTEMPTS_HINTS_ENABLED = 11
        HARD_LEVEL_ATTEMPTS_HINTS_DISABLED = 20

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

                    if level == EASY_LEVEL:
                        # No hints were enabled, so user gets the full score
                        if specific_hint == "":
                            # Calling the function which will update the user score with the required number of points
                            update_user_score(EASY_LEVEL_HINTS_DISABLED_POINTS)
                        # Hints were enabled, half the score, regardless of level
                        else:
                            # Calling the function which will update the user score with the required number of points
                            update_user_score(EASY_LEVEL_HINTS_ENABLED_POINTS)

                    elif level == MEDIUM_LEVEL:

                        # No hints were enabled, so user gets the full score
                        if specific_hint == "":
                            # Calling the function which will update the user score with the required number of points
                            update_user_score(MEDIUM_LEVEL_HINTS_DISABLED_POINTS) 

                        # Hints were enabled, half the score, regardless of level
                        else:
                            # Calling the function which will update the user score with the required number of points
                            update_user_score(MEDIUM_LEVEL_HINTS_ENABLED_POINTS)

                    elif level == HARD_LEVEL:
                        # No hints were enabled, so user gets the full score
                        if specific_hint == "":
                            # Calling the function which will update the user score with the required number of points
                            update_user_score(HARD_LEVEL_HINTS_DISABLED_POINTS)

                        # Hints were enabled, half the score, regardless of level
                        else:
                            # Calling the function which will update the user score with the required number of points
                            update_user_score(HARD_LEVEL_HINTS_ENABLED_POINTS)

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

            # If the level is "easy", a random number in the guess range, number of attempts when hints are disabled, and number of
            # attempts when hints are enabled will be sent to the function. From there, depending on whether the user chose to
            # enable/disable hints, the number of guesses will be generated. We are returning the number of guesses, as well as if
            # the hint was enabled or disabled.
            if level == EASY_LEVEL:
                response_obj = generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,10), EASY_LEVEL_ATTEMPTS_HINTS_DISABLED, EASY_LEVEL_ATTEMPTS_HINTS_ENABLED
                )
            # If the level is "medium", a random number in the guess range, number of attempts when hints are disabled, and number of
            # attempts when hints are enabled will be sent to the function. From there, depending on whether the user chose to
            # enable/disable hints, the number of guesses will be generated. We are returning the number of guesses, as well as if
            # the hint was enabled or disabled.
            # If the level is medium, generate a random number between 1 and 50
            elif level == MEDIUM_LEVEL:
                response_obj = generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,50), MEDIUM_LEVEL_ATTEMPTS_HINTS_DISABLED, MEDIUM_LEVEL_ATTEMPTS_HINTS_ENABLED
                )

            # If the level is "hard", a random number in the guess range, number of attempts when hints are disabled, and number of
            # attempts when hints are enabled will be sent to the function. From there, depending on whether the user chose to
            # enable/disable hints, the number of guesses will be generated. We are returning the number of guesses, as well as if
            # the hint was enabled or disabled.
            elif level == HARD_LEVEL:
                response_obj = generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,100), HARD_LEVEL_ATTEMPTS_HINTS_DISABLED, HARD_LEVEL_ATTEMPTS_HINTS_ENABLED
                )
                    
        # If the correct number has already been specified, it needs to be re-generated
        if 'correct_number' in request.session:

            # If the level is "easy", we will first remove the correct number from the session as we need to generate it again.
            # Then, we are calling the function, passing in the random number in the guess range, number of attempts when hints
            # are disabled, and number of attempts when hints are enabled. From there, depending on 
            # whether the user chose to enable/disable hints, the number of guesses will be generated. We are returning the number
            # of guesses, as well as if the hint was enabled or disabled.
            if level == EASY_LEVEL:
                request.session.pop('correct_number', None)

                response_obj = generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,10), EASY_LEVEL_ATTEMPTS_HINTS_DISABLED, EASY_LEVEL_ATTEMPTS_HINTS_ENABLED
                )
            
            # If the level is "medium", we will first remove the correct number from the session as we need to generate it again.
            # Then, we are calling the function, passing in the random number in the guess range, number of attempts when hints
            # are disabled, and number of attempts when hints are enabled. From there, depending on 
            # whether the user chose to enable/disable hints, the number of guesses will be generated. We are returning the number
            # of guesses, as well as if the hint was enabled or disabled.
            elif level == MEDIUM_LEVEL:
                request.session.pop('correct_number', None)
                
                response_obj = generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,50), MEDIUM_LEVEL_ATTEMPTS_HINTS_DISABLED, MEDIUM_LEVEL_ATTEMPTS_HINTS_ENABLED
                )

            # If the level is "hard", we will first remove the correct number from the session as we need to generate it again.
            # Then, we are calling the function, passing in the random number in the guess range, number of attempts when hints
            # are disabled, and number of attempts when hints are enabled. From there, depending on 
            # whether the user chose to enable/disable hints, the number of guesses will be generated. We are returning the number
            # of guesses, as well as if the hint was enabled or disabled.
            elif level == HARD_LEVEL:
                request.session.pop('correct_number', None)

                response_obj = generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,100), HARD_LEVEL_ATTEMPTS_HINTS_DISABLED, HARD_LEVEL_ATTEMPTS_HINTS_ENABLED
                )
        number_of_guesses = response_obj['number_of_guesses']
        
        try:
            game_user_profile = GameUserProfile.objects.get(user=request.user)

            latest_score = game_user_profile.current_score
        except GameUserProfile.DoesNotExist:
            latest_score = 0
        
        correct_number = request.session['correct_number']
        specific_hint = response_obj['specific_hint']

        context = {
            'specific_hint' : response_obj['specific_hint'],
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