$(document).ready(function () {

    // When the user enters the new password and clicks the submit button, we will try to initiate a POST request using AJAX.
    $('#submit_password_reset_form').click(function (e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();
        
        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#password_reset_form').serialize();

        // AJAX call where we are performing a POST request, using the relevant URL for the password reset view, and displaying
        // the outcome of the operation to the page.
        $.ajax({
            type : 'POST',
            url : $("#password_reset_form").data("url"),
            data : form_data,
            
            // If there were no errors encountered when the POST request was made, we will then determine whether the 
            // password was changed or not in the backend.
            success : function(response) {
                // If the password was changed successfully, we will display that message to the page and redirect
                // the user to the login page.
                if (response.password_changed === true) {
                    // Hiding the password reset form, as we don't want the user to interact with it after password change
                    $('#password_reset_form').hide();
                    
                    // Making sure any error messages from potentially previous password change attempts are cleared from the page
                    $('#paragraph_outcome_password_reset_failure').text("");
                    $('#div_outcome_password_reset_failure').hide();

                    // Displaying the success message to the page, so that the user knows that the password was updated.
                    $('#paragraph_outcome_password_reset_success').text(response.message);
                    $('#div_outcome_password_reset_success').show();
                    
                    // Displaying a loading spinner, so that the user knows that the page will redirect soon.
                    $('#loading_redirect_to_login_after_pwd_reset').show();
                    
                    // In 1.5 seconds time, the user will be redirected to the login page. We are hiding the loading spinner, as
                    // there is no need to have it when the page redirects.
                    setTimeout(function() {
                        window.location.href = $('#link_to_login_page_after_pwd_reset').data("url");
                        $('#loading_redirect_to_login_after_pwd_reset').hide();
                    }, 1500);
                }
                
                // If the password change was unsuccessful, the exact issue will be presented on the screen, so that 
                // the user can figure out what to do.
                else if (response.password_changed === false) {
                    $('#paragraph_outcome_password_reset_failure').text(response.message);
                    $('#div_outcome_password_reset_failure').show();
                }
            },
            
            // If there was an error encountered when the POST request was made, we will log the error to the console.
            error : function(error) {
                console.log(error);
            }
        });
    });

});