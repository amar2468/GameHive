from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import RegistrationForm,LoginForm, TestimonialsForm, ChangePasswordForm, UpdatePersonalDetails, BuyItemForm, ForgotPasswordForm, CustomerSupportForm
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from gamehive.models import CustomUser,GameUserProfile,TestimonialsModel, CustomerSupportModel
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
import json

# View that renders the homepage which allows a user to either sign up/login or play the game of their choice

def homepage(request):
    return render(request, 'index.html')

# View that handles password resets from a user who is not logged in. If the email exists on the system, an email will be sent to the
# user, with the password reset link attached.

def forgot_password(request):
    # If the user submits their email address as part of the password reset form, we will check to see if the email exists in
    # the system. If it does, an email will be sent to the user, with a password reset link attached.
    if request.method == "POST":
        # Creating an instance of the ForgotPasswordForm, so that we can validate the user input
        form = ForgotPasswordForm(request.POST)

        # Validating the password reset form, to see whether the user provided the necessary information.
        if form.is_valid():
            user_email_for_pwd_reset = form.cleaned_data['user_email_for_pwd_reset']

            # Check if the email exists in the CustomUser model. If it does, send the email with password reset link.
            try:
                user = CustomUser.objects.get(email=user_email_for_pwd_reset)

            # If the user email does not exist, send the error message back to the front-end, so the user can see what is wrong.
            except CustomUser.DoesNotExist:
                response_forget_password = {
                    'success' : "The email you entered could not be found in our system. Make sure that you have typed the email correctly.",
                    'email_sent' : False
                }

                return JsonResponse(response_forget_password)
            
            # Encoding the user's primary key (ID) so that it can be safely included in the URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Generating a token, which will be used to verify the user's identity. 
            token = default_token_generator.make_token(user)

            # Including the user's primary ID and token in the URL for the password reset, so that only a user who has requested a 
            # password reset can change their password.
            pwd_reset_link = f"http://127.0.0.1:8000{reverse('password_reset_view', kwargs={'uidb64':uid, 'token':token})}"

            # Setting a subject for the email which will contain the password reset link
            email_subject = "Password Reset Request - GameHive"

            # Setting the body for the email which will contain the password reset link
            email_body = f"Hello {user.username}. We have received a request to reset your GameHive password. Click on this link to set the new password - {pwd_reset_link}. If you did not request this, please ignore this email. Kind regards, GameHive Admin"

            # Send the email to the user, with the password reset link attached.
            send_mail(email_subject, email_body, "noreply@gamehive.com", [user_email_for_pwd_reset])

            # If the email was found and the email was sent, send the information back to the user, to inform them that they
            # need to check their email.
            response_forget_password = {
                'success' : "You have been sent an email with the password reset link. Please click on the link and enter your new password.",
                'email_sent' : True
            }

            return JsonResponse(response_forget_password)

        # If the user sent an invalid form, the error message will be sent back to the front-end, so the user can see what is wrong.
        else:
            response_forget_password = {
                'success' : "The email you have entered is not a valid one. Please make sure you have entered a valid email address.",
                'email_sent' : False
            }

            return JsonResponse(response_forget_password)
    
    # If the user is trying to perform a "GET" request on the "forget password" URL, we will display a 403 page, as the retrieving
    # of the "forget password" form is handled by HTML & JavaScript (by displaying a modal).
    else:
        return render(request, "403.html")

# View that will allow a user that is not logged in to enter their new password.
def password_reset_view(request, uidb64, token):
    # If the user is already logged in, they shouldn't be allowed to view this URL, as they can change their password in
    # the profile section.
    if request.user.is_authenticated:
        return render(request, "403.html")
    # If the user is not logged in, we will check whether the user is just trying to retrieve the page or actually submitting the
    # new password.
    else:
        # We will try to decode the user's primary key and see whether a record exists for the user in the CustomUser model
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

        # If a record of the user does not exist in the CustomUser model, we will display a 403 page.
        except (CustomUser.DoesNotExist, ValueError, TypeError):
            return render(request, "403.html")
        # If the user record exists in the CustomUser mode, we will proceed with this "else" block
        else:
            # If the user exists and the token is valid for the user, we will proceed with either the POST or GET request.
            if user is not None and default_token_generator.check_token(user, token):
                # When the user enters their new password and submits it, this block will determine whether the new password is valid.
                # If it is valid, it will set the new password. Otherwise, an error message will be sent back to the front-end.
                if request.method == "POST":
                    form = ChangePasswordForm(request.POST)

                    # If all the fields in the form were filled in using valid info, we will proceed with further checks
                    if form.is_valid():
                        # Retrieve the new password and the confirmed new password from the django form.
                        new_password = form.cleaned_data['change_password']
                        new_password_confirmed = form.cleaned_data['change_password_confirm']

                        # If the new password is equal to the new password confirmed, we will go ahead with the validation of the password
                        if new_password == new_password_confirmed:
                            
                            # If the password is valid, set it as the new password. Otherwise, retrieve the error message
                            # and display it to the user, so they can remediate.
                            try:
                                password_validation.validate_password(new_password)
                            
                            except ValidationError as e:
                                
                                response_password_reset = {
                                    'message' : e.messages,
                                    'password_changed' : False
                                }

                                return JsonResponse(response_password_reset)

                            # Setting the new password
                            user.set_password(new_password)

                            # Saving the record in the model.
                            user.save()

                            response_password_reset = {
                                'message' : "The password has been updated successfully. Please login using the new password.",
                                'password_changed' : True
                            }

                            return JsonResponse(response_password_reset)

                        else:
                            response_password_reset = {
                                'message' : "The passwords don't match. Make sure that the passwords match.",
                                'password_changed' : False
                            }

                            return JsonResponse(response_password_reset)

                    else:
                        response_password_reset = {
                            'message' : "The password is not a valid one. Make sure that the password contains at least 8 characters, with a variety of characters.",
                            'password_changed' : False
                        }

                        return JsonResponse(response_password_reset)
                # If this was a GET request, we will just retrieve the relevant HTML template, and pass the user's primary ID and token
                else:
                    return render(request, "password_reset.html", {'uidb64' : uidb64, 'token' : token})
            
            # If the user record does not exist, a 403 will be displayed.
            return render(request, "403.html")

# View that will display the admin dashboard, where admin can perform common admin activities.
def admin_dashboard(request):
    # If the user is logged in, we will then check to see if the user is an admin or super admin. If so, the
    # admin dashboard will be displayed.
    if request.user.is_authenticated:
        if request.user.account_type == "super_admin" or request.user.account_type == "admin":
            all_users = CustomUser.objects.all()
            all_testimonials = TestimonialsModel.objects.all()
            
            statistical_info_about_gamehive = {
                'number_of_users' : len(all_users),
                'number_of_testimonials' : len(all_testimonials)
            }
            
            return render(request, "admin_dashboard.html", statistical_info_about_gamehive)
        else:
            return render(request, "403.html")
    # If the user is not logged in, the page is forbidden for them.
    else:
        return render(request, "403.html")
    
# View that will show all the users, giving the admin the opportunity to perform tasks such as resetting the password, deleting the 
# account, and updating the profile
def manage_users(request):
    if request.method == "POST":
        # Gets the JSON data from the request
        data = json.loads(request.body)

        # Finds the "users_to_delete_list" array, that was stored in the JSON object.
        users_to_delete = data.get("users_to_delete_list")

        # Iterating through the users to delete and deleting them individually
        for remove_user in users_to_delete:
            # We are retrieving the user record from the CustomUser model
            user_to_remove = CustomUser.objects.get(username=remove_user)

            # Delete the user record that was retrieved above.
            user_to_remove.delete()

        # If only one user was deleted, we will notify the admin that one user was deleted.
        if len(users_to_delete) == 1:
            response_manage_users = {
                'status' : "The selected user has been removed from the system.",
                'success' : True
            }
        
        # If more than one user was deleted, we will notify the admin that more than one user was deleted.
        elif len(users_to_delete) > 1:
            response_manage_users = {
                'status' : "The selected users have been removed from the system.",
                'success' : True
            }
        
        # If no users were deleted, the admin should receive an error message, where they need to investigate the issue.
        else:
            response_manage_users = {
                'status' : "Error: No users were deleted. Please investigate why this is the case.",
                'success' : False
            }

        # Returning the response in JSON form to the front-end.
        return JsonResponse(response_manage_users)
    else:
        # If the user is logged in, we will then check to see if the user is an admin or super admin. If so, the
        # page with all the users will be displayed.
        if request.user.is_authenticated:
            if request.user.account_type == "super_admin" or request.user.account_type == "admin":
                all_users = CustomUser.objects.all()

                response_all_users = {
                    'all_users' : all_users,
                    'number_of_users' : len(all_users)
                }

                return render(request, "manage_users.html", response_all_users)
            else:
                return render(request, "403.html")
        # If the user is not logged in, the page is forbidden for them.
        else:
            return render(request, "403.html")

# View that allows an admin to view all the user requests
def user_request_mgmt(request):
    # If the user is logged in, we will then check to see if the user is an admin or super admin. If so, the
    # page with the user requests will be displayed.
    if request.user.is_authenticated:
        if request.user.account_type == "super_admin" or request.user.account_type == "admin":
            return render(request, "user_requests.html")
        else:
            return render(request, "403.html")
    # If the user is not logged in, the page is forbidden for them
    else:
        return render(request, "403.html")

# View that allows an admin to view all the testimonials
def testimonials_mgmt(request):
    if request.method == "POST":
        # Gets the JSON data from the request
        data = json.loads(request.body)

        # Finds the "testimonials_to_delete" array, that was stored in the JSON object.
        testimonials_to_delete = data.get("testimonials_to_delete")

        # Iterating through the testimonials to delete and deleting them individually
        for remove_testimonial in testimonials_to_delete:
            # Retrieve the user that created the testimonial, as this record will be used when deleting the testimonial itself.
            testimonial_author = CustomUser.objects.get(username=remove_testimonial)

            # We are retrieving the testimonial record from the TestimonialsModel model
            testimonial_to_remove = TestimonialsModel.objects.get(user=testimonial_author)

            # Delete the testimonial record that was retrieved above.
            testimonial_to_remove.delete()
        
        # If only one testimonial was deleted, we will notify the admin that one testimonial was deleted.
        if len(testimonials_to_delete) == 1:
            response_testimonials_mgmt = {
                'status' : "The selected testimonial has been removed from the system."
            }
        
        # If more than one testimonial was deleted, we will notify the admin that more than one testimonial was deleted.
        elif len(testimonials_to_delete) > 1:
            response_testimonials_mgmt = {
                'status' : "The selected testimonials have been removed from the system."
            }
        
        # If no testimonials were deleted, the admin should receive an error message, where they need to investigate the issue.
        else:
            response_testimonials_mgmt = {
                'status' : "Error: No testimonials were deleted. Please investigate why this is the case.",
                'success' : False
            }

        # Returning the response in JSON form to the front-end.
        return JsonResponse(response_testimonials_mgmt)
    else:
        # If the user is logged in, we will then check to see if the user is an admin or super admin. If so, the
        # page with all the testimonials will be displayed.
        if request.user.is_authenticated:
            if request.user.account_type == "super_admin" or request.user.account_type == "admin":
                all_testimonials = TestimonialsModel.objects.all()

                response_all_testimonials = {
                    'all_testimonials' : all_testimonials,
                    'number_of_testimonials' : len(all_testimonials)
                }

                return render(request, "testimonials_mgmt.html", response_all_testimonials)
            else:
                return render(request, "403.html")
        # If the user is not logged in, the page is forbidden for them
        else:
            return render(request, "403.html")

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

        user_details = CustomUser.objects.get(username=request.user)

        response_my_profile = {
            'leaderboard_entries' : leaderboard_entries,
            'user_details' : user_details
        }

        return render(request, 'profile.html', response_my_profile)
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
                    user_details = CustomUser.objects.get(username=request.user)

                    user_details.first_name = change_first_name

                    user_details.last_name = change_surname

                    user_details.email = change_email

                    user_details.save()
                    
                except CustomUser.DoesNotExist:
                    user_details = CustomUser(user=request.user, first_name = change_first_name, surname = change_surname, email = change_email)
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

                        user = CustomUser.objects.get(username=request.user)

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
    
def customer_support(request):
    # If the user submits the customer support request form, it will be handled in this block.
    if request.method == "POST":
        form = CustomerSupportForm(request.POST, request.FILES)

        # If the user is authenticated (logged in), we want to remove the "email" field from the form, as the username is enough
        if request.user.is_authenticated:
            # Excluding the email field, as this is only needed if the user is not logged in and has no access to view the ticket
            form.fields.pop("customer_email")
        
        # If the user is not logged in, we want to remove the "username" field from the form, as the email is enough.
        else:
            form.fields.pop("customer_username")

        # Validating the customer support form, to see whether the user provided the necessary information.
        if form.is_valid():
            # If the user is logged in and the form is valid, we will use the username for the user identifier field.
            if request.user.is_authenticated:
                # Getting all the form fields that the user filled in
                customer_username = form.cleaned_data['customer_username']
                customer_request_type = form.cleaned_data['customer_request_type']
                customer_title_of_request = form.cleaned_data['customer_title_of_request']
                customer_ticket_description = form.cleaned_data['customer_ticket_description']
                customer_ticket_attachments = form.cleaned_data['customer_ticket_attachments']

                # Populating the CustomerSupportModel with the user request information
                customer_support_ticket = CustomerSupportModel(
                    requester_username=customer_username,
                    ticket_request_type=customer_request_type,
                    ticket_title=customer_title_of_request,
                    ticket_description=customer_ticket_description,
                    ticket_attachments=customer_ticket_attachments,
                    ticket_status="Open",
                    ticket_assigned_to=""
                )

                # Saving the record in the model
                customer_support_ticket.save()

                # Creating a dictionary, which will inform the front-end that the form is valid.
                response_customer_support = {
                    'valid_form' : True,
                    'submit_form_outcome' : "Your support request was submitted successfully. We'll be in touch soon!",
                    'error_messages' : ""
                }
                
                # Returning the response above to the front-end
                return JsonResponse(response_customer_support)
            
            # If the user is NOT logged in and the form is valid, we will use the email for the user identifier field.
            else:
                # Getting all the form fields that the user filled in
                customer_username = form.cleaned_data['customer_username']
                customer_email = form.cleaned_data['customer_email']
                customer_request_type = form.cleaned_data['customer_request_type']
                customer_title_of_request = form.cleaned_data['customer_title_of_request']
                customer_ticket_description = form.cleaned_data['customer_ticket_description']
                customer_ticket_attachments = form.cleaned_data['customer_ticket_attachments']

                # Populating the CustomerSupportModel with the user request information
                customer_support_ticket = CustomerSupportModel(
                    requester_email=customer_email,
                    ticket_request_type=customer_request_type,
                    ticket_title=customer_title_of_request,
                    ticket_description=customer_ticket_description,
                    ticket_attachments=customer_ticket_attachments,
                    ticket_status="Open",
                    ticket_assigned_to=""
                )

                # Saving the record in the model
                customer_support_ticket.save()

                # Creating a dictionary, which will inform the front-end that the form is valid.
                response_customer_support = {
                    'valid_form' : True,
                    'submit_form_outcome' : "Your support request was submitted successfully. We'll be in touch soon!",
                    'error_messages' : ""
                }
                
                # Returning the response above to the front-end
                return JsonResponse(response_customer_support)
        
        # If the form is deemed to be invalid, this "else" block will be executed
        else:
            # Response informing the front-end that there were errors during the submission of the form will be returned
            response_customer_support = {
                'valid_form' : False,
                'submit_form_outcome' : "One or more errors were encountered when submitting the form. Please check the form and fix any errors.",
                'error_messages' : form.errors
            }
            
            # Returning the response above to the front-end
            return JsonResponse(response_customer_support)
            
    # If the user only tries to access this page (not submit the form), this block will be executed, retrieving the relevant template
    else:
        return render(request, "customer_support.html")

# View has the POST part, which will take the user registration details and check if they are valid, after which the password will
# be validated. Finally, the user will be added to the user model and the current score will be set to 0 as the user has only been
# created. The other part will just display the sign up page to the user (when they initially decide to sign up, not when they submit it)

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
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
                user = CustomUser.objects.create_user(username=username, first_name=name, last_name=surname, email=email, password=password, account_type="user")
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