$(document).ready(function() {
    $('[data-bs-toggle="tooltip"]').tooltip();

    $('#sign_up_link').addClass('highlight_sign_up_nav_link_in_login_page');
    $('#homepage_link').addClass('unhighlight_nav_links');

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