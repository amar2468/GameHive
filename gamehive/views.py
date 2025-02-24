from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .forms import RegistrationForm,LoginForm, TestimonialsForm, ChangePasswordForm, UpdatePersonalDetails, BuyItemForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from gamehive.models import GameUserProfile,TestimonialsModel, PersonalDetails
from django.http import JsonResponse

# View that renders the homepage which allows a user to either sign up/login or play the game of their choice

def homepage(request):
    return render(request, 'index.html')

# Displays relevant information about the company

def about(request):
    return render(request, 'about.html')

# First part of this view is the POST method, which saves a testimonial to the relevant custom model. The else part will just display
# the page to the user without submitting any forms

def testimonials_page(request):
    if request.method == "POST":

        # Uses the TestimonialsForm in forms.py file which indicates the constraints (i.e. max length, validation)
        form = TestimonialsForm(request.POST)

        # If the form is valid (everything is filled in), the data that is posted (username, testimonial message) will be 
        # cleaned and inserted into the testimonials model which will hold all the testimonials by users

        if form.is_valid():
            try:
                testimonial_form_exists = TestimonialsModel.objects.get(user=request.user)
            except TestimonialsModel.DoesNotExist:
                testimonials_message = form.cleaned_data['testimonial_message']
                star_rating = form.cleaned_data['star_rating']

                new_testimonial = TestimonialsModel(
                    user=request.user,
                    message=testimonials_message,
                    star_rating=star_rating,
                )

                new_testimonial.save()

                response_info_testimonials_form = {
                    'success' : "You have added your testimonial successfully.",
                    'error_messages' : ""
                }

                return JsonResponse(response_info_testimonials_form)

            else:
                response_info_testimonials_form = {
                    'success' : "",
                    'error_messages' : "You have already submitted a testimonial. You are allowed to submit only one."
                }

                return JsonResponse(response_info_testimonials_form)

        else:
            response_info_testimonials_form = {
                'success' : "",
                'error_messages' : form.errors
            }

            return JsonResponse(response_info_testimonials_form)
    else:
        testimonials_model_objs = TestimonialsModel.objects.all()

        return render(request, 'testimonials.html', {'testimonials_model_objs' : testimonials_model_objs})

# View that deals with deleting a testimonial message. It will check whether the current user has a testimonimal message record and
# will delete it. If it doesn't exist, an error message will be returned.
def remove_testimonial(request):
    # If the user is logged in, this block will execute
    if request.user.is_authenticated:
        # If the user clicked on the "delete" icon on their testimonial, this block will get executed.
        if request.method == "POST":

            # Try part will attempt to get the user's testimonial message
            try:
                # Find the current user's testimonial message
                user_testimonial_to_delete = TestimonialsModel.objects.get(user=request.user)
            
            # If the user's testimonial message isn't there, we will return an error message back to the front-end
            except:
                # Creating a response dictionary which will store information on whether the testimonial was deleted
                response_testimonial_status = {
                    'success' : "no",
                    'testimonial_status' : 'You do not have a testimonial to delete.'
                }

                # Return the response dictionary back to the front-end
                return JsonResponse(response_testimonial_status)

            # Delete the current user's testimonial message
            user_testimonial_to_delete.delete()

            # Creating a response dictionary which will store information on whether the testimonial was deleted
            response_testimonial_status = {
                'success' : "yes",
                'testimonial_status' : 'You have deleted your testimonial. Redirecting...'
            }
            
            # Return the response dictionary back to the front-end
            return JsonResponse(response_testimonial_status)
        # If it was a GET request, we will display a 403 error page
        else:
            return render(request, "403.html")
    # If the user is not logged in, we will display a 403 error page
    else:
        return render(request, "403.html")

# View that will present the current leaderboard for all users, as well as provide the user the option to update their personal info

def my_profile(request):
    if request.user.is_authenticated:
        leaderboard_entries = GameUserProfile.objects.all().order_by('-current_score')

        try:
            user_details = PersonalDetails.objects.get(user=request.user)
        except PersonalDetails.DoesNotExist:
            user_details = PersonalDetails(user=request.user)
            user_details.save()

        return render(request, 'profile.html', {'leaderboard_entries': leaderboard_entries, 'user_details' : user_details})
    else:
        return render(request, '403.html')

# This view will update the personal details of the user (email, first name, and surname). This view uses a custom model, which will
# have a one-to-one relationship with the built-in User model. It updates the personal information of the user.

def update_personal_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            form = UpdatePersonalDetails(request.POST)

            if form.is_valid():
                change_email = form.cleaned_data['change_email']
                change_first_name = form.cleaned_data['change_first_name']
                change_surname = form.cleaned_data['change_surname']

                try:
                    user_details = PersonalDetails.objects.get(user=request.user)

                    user_details.first_name = change_first_name

                    user_details.surname = change_surname

                    user_details.user.email = change_email

                    user_details.save()

                    user_details.user.save()
                    
                except PersonalDetails.DoesNotExist:
                    user_details = PersonalDetails(user=request.user, first_name = change_first_name, surname = change_surname)
                    user_details.save()
                    
                response_info_update_personal_details = {
                    'success' : "Personal details updated successfully.",
                    'error_messages' : ""
                }

                return JsonResponse(response_info_update_personal_details)
            
            else:
                response_info_update_personal_details = {
                    'success' : "",
                    'error_messages' : form.errors
                }
                return JsonResponse(response_info_update_personal_details)
        else:
            return render(request, 'profile.html')
    else:
        return render(request, '403.html')

# This view will update the passsword of the user. The password will be validated, to see if it matches the requirements for a password
# If it does, a value of True will be returned back to jQuery. Otherwise, false will be returned and the user will be told what they
# need to improve for the password to be considered "strong"

def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.POST)

            if form.is_valid():
                change_password = form.cleaned_data['change_password']
                change_password_confirm = form.cleaned_data['change_password_confirm']

                if change_password != change_password_confirm:
                    response_info_for_password = {
                        'passwords_match' : False,
                        'error_messages' : "Passwords don't match. Please enter the passwords again."
                    }

                else:
                    try:
                        password_validation.validate_password(change_password)
                    except ValidationError as e:
                        
                        response_info_for_password = {
                            'passwords_match' : False,
                            'error_messages' : e.messages
                        }

                        return JsonResponse(response_info_for_password)
                    else:

                        user = User.objects.get(username=request.user)

                        user.set_password(change_password)

                        user.save()

                        response_info_for_password = {
                            'passwords_match' : True,
                            'error_messages' : ""
                        }

                return JsonResponse(response_info_for_password)

            else:
                response_info_for_password = {
                    'passwords_match' : '',
                    'error_messages' : form.errors
                }
                return JsonResponse(response_info_for_password)
                
        return render(request, 'profile.html')
    else:
        return render(request, '403.html')

# View that deals with redeeming points. When a user redeems a certain number of points, they will be able to buy useful things using
# those points. 

def redeeming_points(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BuyItemForm(request.POST)

            if form.is_valid():
                price_for_item_in_points = form.cleaned_data['price_for_item_in_points']

                try:
                    game_user_profile = GameUserProfile.objects.get(user=request.user)
                except GameUserProfile.DoesNotExist:
                    game_user_profile = GameUserProfile(user=request.user)

                if price_for_item_in_points <= game_user_profile.current_score:
                    game_user_profile.current_score -= price_for_item_in_points
                    game_user_profile.save()

                    response_info_redeeming_points = {
                        'outcome_from_attempted_purchase' : "Purchase completed successfully!"
                    }

                    return JsonResponse(response_info_redeeming_points)

                response_info_redeeming_points = {
                    'outcome_from_attempted_purchase' : "Not enough points to complete the purchase!"
                }

                return JsonResponse(response_info_redeeming_points)
        else:
            return render(request, 'profile.html')
    else:
        return render(request, '403.html')

# View has the POST part, which will take the user registration details and check if they are valid, after which the password will
# be validated. Finally, the user will be added to the user model and the current score will be set to 0 as the user has only been
# created. The other part will just display the sign up page to the user (when they initially decide to sign up, not when they submit it)

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                response_info_sign_up = {
                    'success' : "",
                    'error_messages' : e.messages
                }

                return JsonResponse(response_info_sign_up)

            # This try/except block looks for whether the username entered in the "sign up" page is unique. If it is, it will allow
            # for the creation of the account. However, if the username already exists, the user will get an error message telling them
            # to pick a unique username.
            
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
            except IntegrityError as e:
                if 'UNIQUE constraint failed: auth_user.username' in str(e):
                    error_message = "Username already exists. Please choose a different username."
                    response_info_sign_up = {
                        'success' : "",
                        'error_messages' : error_message
                    }

                    return JsonResponse(response_info_sign_up)
                
                error_message = "Error when creating the user. Please try again."
                response_info_sign_up = {
                    'success' : "",
                    'error_messages' : error_message
                }

                return JsonResponse(response_info_sign_up)

            game_user_profile = GameUserProfile.objects.get_or_create(user=user)
            game_user_profile = game_user_profile[0]
            game_user_profile.current_score = 0
            game_user_profile.save()

            response_info_sign_up = {
                'success' : "Account has been created successfully. Redirecting you to the login page...",
                'error_messages' : ""
            }

            return JsonResponse(response_info_sign_up)
        if not form.is_valid():
            response_info_sign_up = {
                'success' : "",
                'error_messages' : form.errors
            }

            return JsonResponse(response_info_sign_up)
    else:
        form = RegistrationForm()
    if request.user.is_authenticated:
        return render(request, '403.html')
    else:
        return render(request, 'sign_up.html', {'form': form})

# Sign in view has the POST method, which will take the login form as submitted by user and check if it is valid, after which 
# authentication will occur. If a user is found, it will login the user. Otherwise, the login will not work and the user will be
# redirected back to the login page

def sign_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request, user)
                
                response_info_login = {
                    'success' : "You have logged in successfully. Redirecting to the homepage...",
                    'error_message' : ""
                }

                return JsonResponse(response_info_login)
            else:
                response_info_login = {
                    'success' : "",
                    'error_message' : "Incorrect username or password."
                }
                
                return JsonResponse(response_info_login)
        
        else:
            response_info_login = {
                'success' : "",
                'error_message' : form.errors
            }
            return JsonResponse(response_info_login)
    else:
        form = LoginForm()

    if request.user.is_authenticated:
        return render(request, '403.html')
    else:
        return render(request, 'login.html')

# Logout functionality which simply logs out the user

def log_out(request):

    # Checks if user is logged in and will perform logout in that case
    if request.user.is_authenticated:
        # The user will be logged out after this method is executed
        logout(request)

        # Return to the homepage
        return redirect('homepage')
    
    # If user isn't logged in, the logout will not be allowed
    else:
        return render(request, '403.html')

# If the user types in a URL that does not exist, the 404 template will be displayed, informing the user that the page doesn't exist
def page_does_not_exist(request, exception):
    return render(request, '404.html', status=404)