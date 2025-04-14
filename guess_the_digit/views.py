from django.shortcuts import render
from .forms import GuessTheNumberInputForm
import random
from gamehive.models import GameUserProfile
import redis
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

# Guess the digit game functionality in the view below
def guess_the_digit_game(request):
    if request.user.is_authenticated:
        # Function that will retrieve the current score for the user, which will be displayed on the page.
        def retrieve_latest_user_score():
            try:
                game_user_profile = GameUserProfile.objects.get(user=request.user)

                latest_score = game_user_profile.current_score

                redis_client.hset(request.user.username, "latest_score", latest_score)
            except GameUserProfile.DoesNotExist:
                latest_score = 0

                redis_client.hset(request.user.username, "latest_score", latest_score)

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
            redis_client.hset(request.user.username, "correct_number", number_range)
            correct_number = redis_client.hget(request.user.username, "correct_number")

            specific_hint = create_hint(int(correct_number))

            if specific_hint == "":
                number_of_guesses = attempts_easy_level_enabled
            else:
                number_of_guesses = attempts_easy_level_disabled
            
            redis_client.hset(request.user.username, "number_of_guesses", number_of_guesses)
            redis_client.hset(request.user.username, "specific_hint", specific_hint)
            number_of_guesses = redis_client.hget(request.user.username, "number_of_guesses")
            specific_hint = redis_client.hget(request.user.username, "specific_hint")
        
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

        load_dotenv()

        redis_url = os.getenv("REDIS_URL")

        url = urlparse(redis_url)

        # Creating an instance of the Redis client
        redis_client = redis.Redis(host=url.hostname, password=url.password, port=url.port, ssl=True, decode_responses=True)
        
        # This block below will execute when the user fills in the form (which asks for the level and if hints should be enabled)
        if request.method == "GET":
            # Creating a hash entry for the specific user and populating it with the variables below
            redis_client.hset(request.user.username, "number_of_guesses", 0)
            redis_client.hset(request.user.username, "specific_hint", "")

            # Setting the level for the game inside the hash entry for the user and retrieving the value, so that it can be used.
            redis_client.hset(request.user.username, "level", request.GET.get('selected_level'))
            level = redis_client.hget(request.user.username, "level")

            # Setting the variable that determines whether hints are enabled or disabled
            redis_client.hset(request.user.username, "hints", request.GET.get('hints'))
            hints = redis_client.hget(request.user.username, "hints")

            # Generate the hint (if number is odd or even) depending on the current_score condition
            def create_hint(odd_or_even):
                if hints == "yes":
                    if odd_or_even % 2 == 0:
                        return "The number is even"
                    else:
                        return "The number is odd"
                else:
                    return ""

            # If the level is "easy", we will call the function, passing in the random number in the guess range, number of attempts
            # when hints are disabled, and number of attempts when hints are enabled. From there, depending on whether the user
            # chose to enable/disable hints, the number of guesses will be generated.
            if level == EASY_LEVEL:
                generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,10), EASY_LEVEL_ATTEMPTS_HINTS_DISABLED, EASY_LEVEL_ATTEMPTS_HINTS_ENABLED
                )
            
            # If the level is "medium", we will call the function, passing in the random number in the guess range, number of attempts
            # when hints are disabled, and number of attempts when hints are enabled. From there, depending on whether the user
            # chose to enable/disable hints, the number of guesses will be generated.
            elif level == MEDIUM_LEVEL:
                generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,50), MEDIUM_LEVEL_ATTEMPTS_HINTS_DISABLED, MEDIUM_LEVEL_ATTEMPTS_HINTS_ENABLED
                )

            # If the level is "hard", we will call the function, passing in the random number in the guess range, number of attempts
            # when hints are disabled, and number of attempts when hints are enabled. From there, depending on whether the user
            # chose to enable/disable hints, the number of guesses will be generated.
            elif level == HARD_LEVEL:
                generate_correct_number_and_set_no_of_attempts(
                    random.randint(1,100), HARD_LEVEL_ATTEMPTS_HINTS_DISABLED, HARD_LEVEL_ATTEMPTS_HINTS_ENABLED
                )
            
            # Retrieving the current score for the user
            retrieve_latest_user_score()

            # Saving the "latest score" in a variable, so that it can be passed to the front-end, to be displayed on screen.
            latest_score = redis_client.hget(request.user.username, "latest_score")
            
            # Retrieving the "specific_hint" and "correct_number" from Redis, so that this info can be passed to the front-end.
            specific_hint = redis_client.hget(request.user.username, "specific_hint")
            correct_number = redis_client.hget(request.user.username, "correct_number")
            correct_number = int(correct_number)

            # The variables are stored in the context so that they can be returned back to the html template
            context = {
                'specific_hint' : specific_hint,
                'level' : level,
                'latest_score' : latest_score,
                'correct_number' : correct_number
            }

            return render(request, 'home.html', context)

        # When the user submits the request, this will be executed.
        elif request.method == "POST":
            form = GuessTheNumberInputForm(request.POST)

            if form.is_valid():
                # Take the guess from the user
                user_guess = int(request.POST.get('guess_number_input_field', ''))

                # Extract the random number that will be the correct number
                correct_number = redis_client.hget(request.user.username, "correct_number")
                correct_number = int(correct_number)

                # Retrieving the level that the user chose for this game, as this is needed in the code
                level = redis_client.hget(request.user.username, "level")

                # Retrieving the "specific hint" for this game, as this is needed in the code
                specific_hint = redis_client.hget(request.user.username, "specific_hint")

                # Retrieving the "number of guesses" that the user has for the game, so that we can track how many attempts the user
                # has to get the correct answer.
                number_of_guesses = redis_client.hget(request.user.username, "number_of_guesses")
                number_of_guesses = int(number_of_guesses)

                # Creating a result string which will hold the prompt from the program (whether user has guessed right or not)
                result = ""
                
                # If the user guessed the correct number, we will update the score accordingly.
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

                # If the user didn't guess the correct number, the "number of guesses" are decreased by 1 and an error message is
                # displayed on screen (front-end)
                elif user_guess != correct_number:
                    number_of_guesses -= 1

                    # Saving the decreased "number of guesses" and retrieving the value, so that we can see if the user has more
                    # attempts left or if this was the last attempt.
                    redis_client.hset(request.user.username, "number_of_guesses", number_of_guesses)
                    number_of_guesses = redis_client.hget(request.user.username, "number_of_guesses")
                    number_of_guesses = int(number_of_guesses)

                    # If the user has more attempts left, just display the "wrong guess" message on the page.
                    if number_of_guesses != 0:
                        result = "Wrong guess! Try again!"
                    
                    # If this was the user's last guess, inform them of the correct number
                    else:
                        result = "Game over! The correct number was " + str(correct_number)
                        redis_client.hdel(request.user.username, "correct_number")

                # Calling the function to retrieve the latest score for the game, so that it can be passed to the front-end to process
                retrieve_latest_user_score()
                latest_score = redis_client.hget(request.user.username, "latest_score")

                # The variables are stored in the context so that they can be returned back to the html template
                context = {
                    'result': result,
                    'latest_score': latest_score,
                    'specific_hint' : specific_hint,
                    'level' : level,
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