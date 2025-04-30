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
                console.log(response);
            },

            // If an error occurred, the error will be logged to the console.
            error: function(error) {
                console.log(error);
            }
            
        })

    });
});