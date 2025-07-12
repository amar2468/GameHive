$(document).ready(function() {

    // Highlighting the "Admin Dashboard" nav-link, to indicate that we are on that page
    $('#admin_dashboard_link').addClass('highlight_specific_navlink');

    // If the button to toggle the sidebar is clicked, we want to show/hide ticket info
    $(document).on("click", "#toggle_sidebar", function() {
        // If the ticket info is not being displayed, clicking the toggle button will display it.
        if ($('.row').css("display") === 'none') {
            $('.row').removeClass("d-none");
        }

        // If the ticket info is being displayed, clicking the toggle button will hide it.
        else {
            $('.row').addClass("d-none");
        }
    });

    // When the user submits the comment in the ticket via the comment form, this will get executed.
    $(document).on("submit", "#add_comment_in_ticket_form", function(e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#add_comment_in_ticket_form').serialize();

        // AJAX POST request, which will attempt to submit the comment within the ticket to the backend and deliver the outcome 
        // (success or failure) to the user
        $.ajax({
            type : 'POST',
            url : $('#add_comment_in_ticket_form').data("url"),
            data : form_data,

            // If the form submission was successful and the backend returns a response, this will be executed.
            success: function(response) {
                // If the comment was successfully added, we will tell the user that it was successfully done.
                if (response.success === true) {
                    // Shows the success alert, to notify the user that the comment was successfully added.
                    $('#paragraph_outcome_comment_success').text(response.status);
                    $('#div_outcome_comment_success').show();

                    // Disable the button to submit the reply (preventing user from submitting the form multiple times in a row)
                    $('#reply_to_ticket').prop("disabled", true);

                    // Setting a timeout of 1.5 seconds, in which the success alert will disappear from the page and the
                    // page will reload.
                    setTimeout(function() {
                        $('#div_outcome_comment_success').hide();

                        // Re-enabling the button.
                        $('#reply_to_ticket').prop("disabled", false);

                        location.reload(true);
                    }, 1500);
                }

                // If there was an issue with adding the comment, the user will be notified about it.
                else {
                    // Shows the failure alert, to notify the user that the comment was NOT added.
                    $('#paragraph_outcome_comment_failure').text(response.status);
                    $('#div_outcome_comment_failure').show();

                    // Disable the button to submit the reply (preventing user from submitting the form multiple times in a row)
                    $('#reply_to_ticket').prop("disabled", true);

                    // Setting a timeout of 1.5 seconds, in which the failure alert will disappear from the page and the
                    // page will reload.
                    setTimeout(function() {
                        $('#div_outcome_comment_failure').hide();

                        // Re-enabling the button.
                        $('#reply_to_ticket').prop("disabled", false);

                        location.reload(true);
                    }, 1500);
                }
            },
            
            // If an error was encountered, the error will be logged to the console.
            error: function(error) {
                console.error(error);
            }
            
        });

    });

});