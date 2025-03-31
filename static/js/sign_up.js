// When the template is loaded, the user will be able to see the tooltip text
$(document).ready(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();

    $('#forgot_password_link').click(function() {
        $('#forgot_password_modal').modal("show");
    });

    $('#submit_email_for_password_reset_btn').click(function(e) {
        e.preventDefault();

        form_data = $('#forgot_password_form').serialize();

        $.ajax({
            type: 'POST',
            url: $('#forgot_password_form').data("url"),
            data: form_data,

            success: function(response) {
                window.alert(response.success);
            },

            error: function(error) {
                console.log(error);
            }
        });
    });

    // If the form is submitted, this will perform an AJAX call and send the registration info to the backend.
    // Then, it will be sent back to the client-side, so that it can be displayed.
    $('#registration_form').submit(function (e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#registration_form').serialize();

        // AJAX POST request, which will attempt to create an account for the user and
        // deliver the outcome (success or failure) to the user
        $.ajax({
            type: 'POST',
            url: $('#registration_form').data("url"),
            data: form_data,

            success: function(response) {

                // If the account has not been created successfully, it will display the error messages on the screen.
                if (response.success === "")
                {
                    if (response.error_messages != "")
                    {
                        // Clearing any previous errors, so only new errors are displayed.
                        $('#reg_form_error_messages').text("");

                        // Making sure the div that shows the error messages is hidden.
                        $('#div_for_reg_form_errors').hide();

                        if ($.type(response.error_messages) === "array")
                        {
                            // Iterating through each error message and displaying it in the required list, so user can correct their
                            // actions
                            for (let element in response.error_messages)
                            {
                                $('#reg_form_error_messages').append(`<li>${response.error_messages[element]}</li>`);
                            }
                        }

                        else if ($.type(response.error_messages) === "object")
                        {
                            // Iterating through each error message and displaying it in the required list, so user can correct their
                            // actions
                            for (let element in response.error_messages)
                            {
                                response.error_messages[element].forEach(error => {
                                    $('#reg_form_error_messages').append(`<li>${element} is required.</li>`);
                                });
                            }
                        }

                        else
                        {
                            // Adding the error message to the element that holds the error messages
                            $('#reg_form_error_messages').text(`${response.error_messages}`);
                        }

                        // Displays the div, which holds the list of errors
                        $('#div_for_reg_form_errors').show();
                    }
                }

                // If the account has been successfully created, the message will be displayed on the screen.
                else
                {
                    // Disabling the submit button in the sign up form, so that a user cannot click it while the request
                    // is being processed
                    $('#submitButton').prop("disabled", true);

                    // Making sure the div that shows the error messages is hidden.
                    $('#div_for_reg_form_errors').hide();

                    $('#reg_form_success').text(response.success);
                    $('#reg_form_success').show();

                    // After 1.5 seconds of the user signing in successfully, redirect to the login page.
                    setTimeout(function () {
                        window.location.href = $('#link_to_login_page').data("url");
                    }, 1500);
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