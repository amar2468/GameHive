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

    // If the button to edit the ticket title is clicked, we will show the input field (where the user can edit the title) and the
    // save and cancel buttons.
    $(document).on("click", ".edit_ticket_title", function() {
        // Getting the current text in the ticket title
        const ticketTitle = $('#ticket_title').text();

        // Adding the ticket title into the input field and displaying it, so that the user can edit it.
        $('#ticket_title_input').val(ticketTitle).removeClass("d-none");

        // Hide the ticket title, as the user can now edit the ticket title using the input field instead
        $('#ticket_title').addClass("d-none");

        // Show the save button
        $('#save_edited_title').removeClass("d-none");

        // Show the cancel button
        $('#cancel_edited_title').removeClass("d-none");

        // Hide the pencil icon, which allows the user to edit the ticket title.
        $(this).addClass("d-none");
    });

    // If the button to cancel the ticket editing is clicked, it will hide the buttons and the input field, and just
    // show the ticket title along with the pencil icon for editing the ticket title.
    $(document).on("click", "#cancel_edited_title", function() {
        // Hide the cancel button
        $('#cancel_edited_title').addClass("d-none");

        // Hide the save button
        $('#save_edited_title').addClass("d-none");

        // Hide the ticket title input field, as the user has finished editing the ticket title
        $('#ticket_title_input').addClass("d-none");

        // Display the ticket title again
        $('#ticket_title').removeClass("d-none");

        // Display the button to edit the ticket title again.
        $('.edit_ticket_title').removeClass("d-none");
    });

    // When the user clicks on the save button, an attempt will be made to update the ticket title by passing the
    // new ticket title to the Django view, where it will try to update the record in the model.
    $(document).on("click", "#save_edited_title", function() {
        // Retrieving the new ticket title
        const newTicketTitle = $("#ticket_title_input").val();

        // Retrieving the csrf token from the page, to allow the sending of data through AJAX
        const csrf_token = $('#csrf_token').val();

        // AJAX POST request that sends the new ticket title and ticket ID to the backend, in order to update the ticket title
        $.ajax({
            type: "POST",
            url: $('#ticket_title_input').data("url"),
            headers: {
                'X-CSRFToken': csrf_token
            },
            data: {
                'newTicketTitle': newTicketTitle,
                'ticketID': $("#ticket_id").val()
            },

            // If the ticket title updated successfully, we won't do anything. We'll just print the success message
            // to the console.
            success: function(response) {
                console.log(response.message);
            },

            // If an error occurred, we will display it in the console.
            error: function(err) {
                console.error(err);
            }
        });

        // Update the ticket title to use the new one.
        $('#ticket_title').text(newTicketTitle).removeClass("d-none");

        // Hide the save button
        $('#save_edited_title').addClass("d-none");

        // Hide the cancel button
        $('#cancel_edited_title').addClass("d-none");

        // Hide the input field that allows you to put the new ticket title
        $('#ticket_title_input').addClass("d-none");

        // Show the button that allows the editing of the ticket title.
        $('.edit_ticket_title').removeClass("d-none");
    });

    // If the form to update the ticket information is submitted, it will try to make a POST request and update the ticket information
    // that was changed. It will display a success or failure alert, depending on the outcome.
    $(document).on("submit", "#update_ticket_info_form", function(e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#update_ticket_info_form').serialize();

        // AJAX POST request, that sends the updated ticket fields to the backend, so that they can be updated in the model.
        $.ajax({
            type: "POST",
            url: $("#update_ticket_info_form").data("url"),
            data: form_data,

            // If no error was encountered when trying to update the ticket information, we will check to see if the
            // ticket information updated successfully.
            success: function(response) {
                // Clearing any old alerts
                $('#paragraph_ticket_updated_success').text("");
                $('#paragraph_ticket_updated_failure').text("");

                // Populating the paragraph with the success message and displaying it on the page.
                $('#paragraph_ticket_updated_success').text(response.message);
                $('#div_ticket_updated_success').show();
            },

            // If an error was encountered, the error will be logged to the console.
            error: function(error) {
                console.error(error.statusText);
                
                // Clearing any old alerts
                $('#paragraph_ticket_updated_success').text("");

                // Populating the paragraph with the failure message and displaying it on the page.
                $('#paragraph_ticket_updated_failure').text(error.responseJSON.message);
                $('#div_ticket_updated_failure').show();
            }
        })
    });

});