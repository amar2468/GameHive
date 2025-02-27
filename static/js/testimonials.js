$(document).ready(function () {

    $('.testimonial_star_rating_link').click(function() {
        // Retrieving the index of the star that was clicked, which will decide how many stars should be coloured in.
        let star_rating_index = $(this).data("index");

        $('#star_rating').val(star_rating_index);

        // Clearing the stars that were filled in before
        $(".bi-star-fill").removeClass("bi-star-fill").addClass("bi-star");
        
        for (let i = 1; i <= star_rating_index; i++)
        {
            $(".bi-star[data-index='" + i + "']").removeClass("bi-star").addClass("bi-star-fill");
        }
    });

    // If the form is submitted, this will perform an AJAX call and send the testimonial info to the backend.
    // Then, it will be sent back to the client-side, so that it can be displayed.
    $('#testimonials_form').submit(function (e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#testimonials_form').serialize();

        // AJAX POST request, which will attempt to add a testimonial and
        // deliver the outcome (success or failure) to the user
        $.ajax({
            type : "POST",
            url : $('#testimonials_form').data("url"),
            data : form_data,

            success: function(response) {

                // Making sure the div that shows the error messages is hidden.
                $('#div_testimonial_errors').hide();
                $('#testimonial_form_success').hide();

                // Clearing any previous errors, so only new errors are displayed.
                $('#testimonial_errors_list').text("");
                $('#testimonial_form_success').text("");

                // If there was an issue with creating the testimonial, error messages will be displayed on the screen
                if (response.success === "")
                {
                    // If the error messages are stored in an object data type, we will iterate through each and 
                    // append them to the list of error messages. All error messages will then be displayed in a list.
                    if ($.type(response.error_messages) === "object")
                    {
                        // Iterating through each error message and putting it in the error list.
                        for (let element in response.error_messages)
                        {
                            response.error_messages[element].forEach(error => {
                                $('#testimonial_errors_list').append(`<li>${element} is required.</li>`);
                            });
                        }
                    }

                    // If the error message is a simple string, we will just display it in the list as it is.
                    else
                    {
                        $('#testimonial_errors_list').text(`${response.error_messages}`);
                    }

                    // Regardless of whether the errors are in an object or string data type, we want to display the div
                    // the shows the errors. It will be visible on the screen.
                    $('#div_testimonial_errors').show();
                }

                // If the testimonial was created successfully, a success message will be displayed on the screen
                // and the page will reload, so that the new testimonial is present on the screen.
                else
                {
                    // Disabling the submit button in the testimonial form, so that a user cannot click it while the request
                    // is being processed
                    $('#submitButton').prop("disabled", true);

                    // Success message displayed on the screen
                    $('#testimonial_form_success').text(response.success);
                    $('#testimonial_form_success').show();

                    // Reloading the page so that the new testimonial is shown in the list of testimonials.
                    setTimeout(function() {
                        location.reload(true);
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
    
    $('#form_for_deleting_testimonial').submit(function(e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // We are serialising the form data, so that it can be sent to the backend for review.
        form_data = $('#form_for_deleting_testimonial').serialize();

        // AJAX POST request, which will attempt to remove a testimonial and deliver the outcome (success or failure)
        // to the user
        $.ajax({
            type : "POST",
            url : $('#form_for_deleting_testimonial').data("url"),
            data : form_data,

            success: function(response) {

                // Making sure that fields that indicate whether the user deleted the testimonial or not are clear.
                $('#delete_testimonial_success').text("");
                $('#delete_testimonial_error_message').text("");

                // If the testimonial was deleted, we will display the success message on the screen and reload the page
                // so that the user can see that this was deleted.
                if (response.success === "yes")
                {
                    // Add the message that the testimonial has been deleted
                    $('#delete_testimonial_success').text(response.testimonial_status);

                    // Display the div that stores the message above
                    $('#delete_testimonial_success').show();

                    // We are disabling the button to delete the testimonial, as we don't want the user to touch this button
                    // while the request is being processed.
                    $('#delete_testimonial_button').prop("disabled", true);

                    // After 1.5 seconds, the page will be reloaded
                    setTimeout(function() {
                        location.reload();
                    }, 1500);
                }

                // If there was an issue with deleting the testimonial, we will display the error message on the screen
                else
                {  
                    // Display the error message on the screen
                    $('#delete_testimonial_error_message').text(response.testimonial_status);

                    // Display the div that holds the error message above
                    $('#div_delete_testimonial').show();
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