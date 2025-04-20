$(document).ready(function() {
    $('[data-bs-toggle="tooltip"]').tooltip();

    // When we are on the login page, we want the "sign_up" nav link to be highlighted and the "homepage" nav link to be unhighlighted.
    $('#sign_up_link').addClass('highlight_specific_navlink');
    $('#homepage_link').addClass('unhighlight_nav_links');

    // If the user clicks on the "forgot your password?" link in the login page, we will display the modal that will allow
    // the user to enter the email address where they want the password reset link to be sent.
    $('#forgot_password_link').click(function() {
        $('#forgot_password_modal').modal("show");
    });

    // When the user submits their email address as part of the password reset process, this will get executed.
    $('#submit_email_for_password_reset_btn').click(function(e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#forgot_password_form').serialize();

        // AJAX POST request, which will attempt to send the user an email with the password reset link & deliver the outcome 
        // (success or failure) to the user
        $.ajax({
            type: 'POST',
            url: $('#forgot_password_form').data("url"),
            data: form_data,

            success: function(response) {
                // If the user's email exists when they enter it in the "forget password" form, we will display a message
                // to say that an email was sent, containing the link for the password reset.
                if (response.email_sent === true) {
                    // Clearing the text for the success message, and hiding both divs (success & failure) if they haven't been hidden.
                    $('#paragraph_outcome_email_exists_success').text("");
                    $('#div_outcome_email_exists_success').hide();
                    $('#div_outcome_email_exists_failure').hide();
                    
                    // Populating the success message into the success paragraph and displaying the div that shows the success message
                    $('#paragraph_outcome_email_exists_success').text(response.success);
                    $('#div_outcome_email_exists_success').show();

                    // Hiding all the other elements in the form, as they are not necessary anymore.
                    $('#forgot_password_info').hide();
                    $('#forgot_password_form').hide();
                }
                
                // If the user's email does not exist when they enter it in the "forget password" form, we will display a message
                // to say that there was an issue encountered.
                else if (response.email_sent === false) {
                    // Clearing the text for the failure message, and hiding both divs (success & failure) if they haven't been hidden.
                    $('#paragraph_outcome_email_exists_failure').text("");
                    $('#div_outcome_email_exists_failure').hide();
                    $('#div_outcome_email_exists_success').hide();

                    // Populating the failure message into the failure paragraph and displaying the div that shows the failure message
                    $('#paragraph_outcome_email_exists_failure').text(response.success);
                    $('#div_outcome_email_exists_failure').show();
                }
            },

            error: function(error) {
                console.log(error);
            }
        });
    });

    // If the form is submitted, this will perform an AJAX call and send the login info to the backend.
    // Then, it will be sent back to the client-side, so that it can be displayed.
    $('#login_form').submit(function (e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#login_form').serialize();

        // AJAX POST request, which will attempt to login a user and deliver the outcome (success or failure) to the user
        $.ajax({
            type : "POST",
            url : $('#login_form').data("url"),
            data : form_data,

            success: function(response) {
                // Hiding the error messages and resetting them so that previous errors don't show up
                $('#div_login_form').hide();
                $('#login_error_messages').text("");
                $('#login_form_success').text("");

                // If the user manages to login successfully, display the success message of the screen
                if (response.error_message === "")
                {
                    // If the user managed to login successfully, we will display the success message on the screen using
                    // this if statement
                    if (response.success != "")
                    {
                        // Disabling the submit button in the login form, so that a user cannot click it while the request
                        // is being processed
                        $('#submitButton').prop("disabled", true);

                        // Adding the success message to the specific list that will be displayed on the screen.
                        $('#login_form_success').text(response.success);
                        $('#login_form_success').show();
                        
                        // After 1.5 seconds of the user signing in successfully, redirect to the homepage.
                        setTimeout(function () {
                            window.location.href = $('#link_to_homepage').data("url");
                        }, 1500);
                    }
                }

                // If the user encounters an error when signing in, this "else" block will add the error message
                // to a list and display it on the screen using the div.
                else
                {
                    // If the error message returned is in the form of an object, we will need a for loop to access each error
                    if ($.type(response.error_message) === "object")
                    {
                        // Go through each error and display it in the error list
                        for (let element in response.error_message)
                        {
                            response.error_message[element].forEach(error => {
                                $('#login_error_messages').append(`<li>${element} is required.</li>`);
                            });
                        }

                        // Display the div that stores the error list
                        $('#div_login_form').show();
                    }

                    // If the error message is a simple string, we can just append it to the list normally.
                    else
                    {         
                        // Adding the error message to the list that holds the error messages
                        $('#login_error_messages').append(`<li>${response.error_message}</li>`);

                        // Displaying the div that holds the list that stores the error messages, which will display the error
                        // messages to the screen
                        $('#div_login_form').show();
                    }
                }
            },

            // If an error occurred while submitting the form, this will just print the error to the console, to help with
            // debugging the issue.
            error: function(error) {
                console.log(error);
            }
        });

    });
});