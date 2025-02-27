$(document).ready(function() {

    // Implementing a datatable for the leaderboard, so that we can get features such as sorting columns, pagination, and search.
    new DataTable('#leaderboard_table');

    $('#update_personal_info_link').css("color", "yellow");

    $('#hide_sidebar_btn').click(function() {
        $('#sidebar_div').toggle();
    });

    $('[data-bs-toggle="tooltip"]').tooltip();

    // If the user clicks on the update personal information link, it will hide all the other pages and just display this one.
    $('#update_personal_info_link').click(function() {
        $('#update_personal_info_link').css("color", "yellow");
        $('#change_password_link').css("color", "#FFFFFF");
        $('#leaderboard_link').css("color", "#FFFFFF");
        $('#redeem_points_link').css("color", "#FFFFFF");

        $('#personal_details_div').show();
        $('#change_password_div').hide();
        $('#leaderboard_div').hide();
        $('#reedem_points_div').hide();

        // Hide the divs that display errors/success messages, whenever a new page is opened
        $('#update_personal_details_errors_div').hide();
        $('#update_password_errors_div').hide();
        $('#update_details_success').hide();
    });

    // If the user clicks on the change password link, it will hide all the other pages and just display this one.
    $('#change_password_link').click(function(){
        $('#update_personal_info_link').css("color", "#FFFFFF");
        $('#change_password_link').css("color", "yellow");
        $('#leaderboard_link').css("color", "#FFFFFF");
        $('#redeem_points_link').css("color", "#FFFFFF");

        $('#personal_details_div').hide();
        $('#leaderboard_div').hide();
        $('#reedem_points_div').hide();
        $('#change_password_div').show();

        // Hide the divs that display errors/success messages, whenever a new page is opened
        $('#update_personal_details_errors_div').hide();
        $('#update_password_errors_div').hide();
        $('#update_details_success').hide();
    });

    // If the user clicks on the leaderboard link, it will hide all the other pages and just display this one.
    $('#leaderboard_link').click(function(){
        $('#update_personal_info_link').css("color", "#FFFFFF");
        $('#change_password_link').css("color", "#FFFFFF");
        $('#leaderboard_link').css("color", "yellow");
        $('#redeem_points_link').css("color", "#FFFFFF");

        $('#personal_details_div').hide();
        $('#change_password_div').hide();
        $('#reedem_points_div').hide();
        $('#leaderboard_div').show();

        // Hide the divs that display errors/success messages, whenever a new page is opened
        $('#update_personal_details_errors_div').hide();
        $('#update_password_errors_div').hide();
        $('#update_details_success').hide();

    });

    // If the user clicks on the reedem points link, it will hide all the other pages and just display this one.
    $('#redeem_points_link').click(function(){
        $('#update_personal_info_link').css("color", "#FFFFFF");
        $('#change_password_link').css("color", "#FFFFFF");
        $('#leaderboard_link').css("color", "#FFFFFF");
        $('#redeem_points_link').css("color", "yellow");

        $('#personal_details_div').hide();
        $('#change_password_div').hide();
        $('#leaderboard_div').hide();
        $('#reedem_points_div').show();
        
        // Hide the divs that display errors/success messages, whenever a new page is opened
        $('#update_personal_details_errors_div').hide();
        $('#update_password_errors_div').hide();
        $('#update_details_success').hide();

    });

    // We are going to perform an AJAX call if the update personal details form submitted, so that we can prevent the 
    // page being reloaded and deliver the information from the backend using JavaScript/jQeury
    $('#update_details_form').submit(function(e) {
        // Preventing the submission of the form, which will prevent the reloading of the page
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#update_details_form').serialize();

        // AJAX POST request, which will attempt to update the personal details and deliver the outcome (success or failure) to the user
        $.ajax({
            type: 'POST',
            url: $('#update_details_form').data("url"),
            data: form_data,

            // If no errors occurred in the backend, this will be executed.
            success: function(response) {

                // Clearing any previous errors, so only new errors are displayed.
                $('#update_personal_details_errors_unordered_list').text("");
                
                // If there was an issue with updating the personal details, such as an empty form being submitted,
                // this will display all the error messages in a list fashion.
                if (response.success === "")
                {
                    // Iterating through each error message and displaying it in the required list, so user can correct their
                    // actions
                    for (let element in response.error_messages)
                    {
                        response.error_messages[element].forEach(error => {
                            $('#update_personal_details_errors_unordered_list').append(`<li>${element} : ${error}</li>`);
                        });
                    }

                    // Displays the div, which holds the list of errors
                    $('#update_personal_details_errors_div').show();

                }

                // If the personal details were updated successfully, the div will be populated with that message and
                // the div will be visible to the user, informing them of the successful outcome.
                else
                {
                    $('#update_details_success').text(response.success);
                    $('#update_details_success').show();

                    setTimeout(function() {
                        $('#update_details_success').text("");
                        $('#update_details_success').hide();
                    }, 2000);
                }
            },

            // If an error occurred while submitting the form, this will just print the error to the console, to help with
            // debugging the issue.
            error: function(error) {
                console.error(error);
            }
        });
    });

    // We are going to perform an AJAX call if the update password form is submitted, so that we can prevent the page being 
    // reloaded and deliver the information from the backend using JavaScript/jQeury

    $('#update_password_form').submit(function(e) {
        // Preventing the submission of the form, which will prevent the reloading of the page
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#update_password_form').serialize();

        // AJAX POST request, which will attempt to change the password and deliver the outcome (success or failure) to the user
        $.ajax({
            type: 'POST',
            url: $('#update_password_form').data("url"),
            data: form_data,

            // If no errors occurred in the backend, this will be executed.
            success: function(response) {
                // Hiding the divs that show success/failure messages, as we don't want older records to be displayed
                $('#update_password_errors_div').hide();
                $('#update_password_success').hide();

                // Clearing any previous text in the two elements below, so that only new error messages/success messages appear
                $('#update_password_success').text("");
                $('#error_messages_unordered_list').text("");

                // If the new password that the user enters matches the one that they entered in the field where you confirm
                // your new password, the user will be informed that the password has been updated.
                if (response.passwords_match === true)
                {
                    window.alert("HELLO");
                    $('#update_password_success').text("Password has been updated successfully!");
                    $('#update_password_success').show();

                    setTimeout(function() {
                        $('#update_password_success').text("");
                        $('#update_password_success').hide();

                        window.location.href = $('#homepage_redirect').data("url");
                    }, 2000);
                }

                // If the new password that the user enters does not match the one that they entered in the field where 
                // you confirm your new password, the user will be informed that the passwords don't match.
                else if (response.passwords_match === false)
                {
                    // If the error messages are stored in an array, we will just loop through each and display
                    if ($.type(response.error_messages) === "array")
                    {
                        for (let element in response.error_messages)
                        {
                            $('#error_messages_unordered_list').append(`<li>${response.error_messages[element]}</li>`);
                        }
                        
                        $('#update_password_errors_div').show();
                    }

                    // If the error message is stored in a string, we will just display it.
                    else
                    {
                        $('#error_messages_unordered_list').append(`<li>${response.error_messages}</li>`);
                        $('#update_password_errors_div').show();
                    }
                }

                // If there are errors in the form, we will set the value that detects whether the passwords match to ''
                // We do this because the user sent an empty form and we want to inform them that they have to enter a password
                // in both fields as it is required.
                else if (response.passwords_match === '')
                {

                    // We are populating the list that holds the error messages with each error message that was detected by 
                    // the backend, specifically Django forms.
                    for (let element in response.error_messages)
                    {
                        response.error_messages[element].forEach(error => {
                            $('#error_messages_unordered_list').append(`<li>${element}: ${error}</li>`);
                        });
                    }

                    // We are displaying the errors from above on the screen.
                    $('#update_password_errors_div').show();
                }
            },

            // If an error occurred while submitting the form, this will just print the error to the console, to help with
            // debugging the issue.
            error: function(error) {
                console.error(error);
            }
        });
    });

    $('.buy_item_link').submit(function(e) {
        e.preventDefault();

        form_data = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $('.buy_item_link').data("url"),
            data: form_data,

            success: function(response) {
                $('#selected-value').text(response.outcome_from_attempted_purchase);
                $('#redeem_points_modal').modal('show');
            },

            error: function(error) {
                console.log(error);
            }
        })
    });
});