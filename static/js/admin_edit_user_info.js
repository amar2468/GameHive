$(document).ready(function() {
    // When on the page where the admin can view/edit the user profile, we want the "admin_dashboard" nav link to be highlighted
    $('#admin_dashboard_link').addClass('highlight_specific_navlink');

    // When the admin updates the user information, this function will be executed, passing the data to the backend, so that the
    // user profile can be updated accordingly.
    $('#edit_user_info_form').submit(function(e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#edit_user_info_form').serialize();

        // Added the current username to the form, in case the admin changes the username of this user.
        form_data += "&current_username=" + ($('#current_username').data("url"));

        // AJAX POST request, which will submit the form to update the user profile by passing the data from the form, the relevant
        // URL to call, and the CSRF token.
        $.ajax({
            type: "POST",
            url: $('#edit_user_info_form').data("url"),
            data: form_data,
            headers: {
                'X-CSRFTOKEN' : $('#csrf_token').val()
            },

            // If the form was processed correctly in the backend (no errors encountered), we will retrieve the information from the 
            // backend and present it on the page, to inform the admin of the outcome of the operation.
            success: function(response) {
                // If the user profile was updated, we will notify the admin, and show what fields were updated.
                if (response.success === true) {
                    // Clearing the previous messages from the page, as they are now irrelevant.
                    $("#paragraph_outcome_edit_user_profile_no_changes").text("");
                    $("#div_outcome_edit_user_profile_no_changes").hide();

                    // Showing the message that informs the admin that the user profile update was successful.
                    $('#paragraph_outcome_edit_user_profile_success').text(response.message);
                    $('#div_outcome_edit_user_profile_success').show();
                }
                
                // If the user profile was not updated, we will notify the admin.
                else if (response.success === false) {
                    // If no changes were made, we will just display the info on the screen.
                    if (response.message === "No changes have been made to the user profile.") {
                        // Clearing the previous messages from the page, as they are now irrelevant.
                        $("#paragraph_outcome_edit_user_profile_success").text("");
                        $("#div_outcome_edit_user_profile_success").hide();
                        
                        // Showing the message that informs the admin that no changes were made to the user profile.
                        $('#paragraph_outcome_edit_user_profile_no_changes').text(response.message);
                        $('#div_outcome_edit_user_profile_no_changes').show();
                    }

                    // If the admin entered an existing username or email for the user, we will inform the admin that the username 
                    // or email that they chose already exists on the system.
                    else {
                        // Clearing the previous messages from the page, as they are now irrelevant.
                        $("#paragraph_outcome_edit_user_profile_success").text("");
                        $("#div_outcome_edit_user_profile_success").hide();
                        
                        // Showing the message that informs the admin that no changes were made to the user profile as the username
                        // already exists on the system.
                        $('#paragraph_outcome_edit_user_profile_no_changes').text(response.message);
                        $('#div_outcome_edit_user_profile_no_changes').show();

                        // Changing the "username" input field to use to current username.
                        $('#edit_username').val($('#current_username').data("url"));

                        // Changing the "email" input field to use the current email
                        $('#edit_email').val($('#current_email').data("url"));
                    }
                }
                
                // If something unexpected occurred, we will point that out and get the admin to investigate what happened.
                else {
                    $('#paragraph_outcome_edit_user_profile_no_changes').text("Something went wrong - please contact the superadmin for assistance.");
                    $('#div_outcome_edit_user_profile_no_changes').show();
                }
            },

            // If an error occurred, the error will be logged to the console.
            error: function(error) {
                console.log(error);
            }
            
        })

    });
});