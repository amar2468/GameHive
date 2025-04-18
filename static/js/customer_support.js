$(document).ready(function() {
    $('[data-bs-toggle="tooltip"]').tooltip();

    // When the user submits the customer support form, this will get executed.
    $('#customer_support_form').on("submit", function(e) {
        // We are preventing the submission of the form, as this will be done through AJAX
        e.preventDefault();

        // Create a FormData object from the submitted form, including all input fields and uploaded files.
        // This allows us to send the form data (including file uploads) using AJAX.
        const form_data = new FormData(this);

        // AJAX POST request, which will attempt send the form data from the customer support form to the backend, 
        // and retrieve the information back from the backend, which will be presented on the page.
        $.ajax({
            type: 'POST',
            url: $('#customer_support_form').data("url"),
            data: form_data,
            processData: false, // Prevents jQuery from attempting to process the data
            contentType: false, // Allows the browser to set the correct Content-Type for multipart data (especially the case for files)

            // If the form submission was successful, we will then try to determine if the form is valid or not, based on the
            // django form in forms.py.
            success: function(response) {
                // If the customer support form that was submitted is deemed a valid form (based on the form specified in forms.py)
                // then we will display the message on the page, informing the user of the successful submission of the form.
                if (response.valid_form === true) {
                    // Hide any error messages from previous attempts (if applicable)
                    $('#div_outcome_customer_support_submit_failure').hide();
                    $('#paragraph_outcome_customer_support_submit_failure').text("");

                    $('#div_customer_support_errors').hide();
                    $('#customer_support_errors_list').text("");

                    // Show the success message on the screen. The message is populated from the backend.
                    $('#div_outcome_customer_support_submit_success').show();
                    $('#paragraph_outcome_customer_support_submit_success').text(response.submit_form_outcome);
                    
                    // Temporarily hide the submit button, while the success message is on the screen, to avoid the user submitting
                    // another attempt.
                    $('#submit_customer_support_form').hide();

                    // After 1.5 seconds, hide all the success messages and re-display the button for submitting the customer support
                    // form on the screen.
                    setTimeout(function() {
                        $('#div_outcome_customer_support_submit_success').hide();
                        $('#paragraph_outcome_customer_support_submit_success').text("");

                        $('#submit_customer_support_form').show();
                    }, 1500);
                }
                
                // If the customer support form that was submitted is deemed an invalid form (based on the form specified in forms.py)
                // then we will display the message on the page, informing the user of the errors encountered during the submission
                // of the form.
                else {
                    // Clearing any previous specific errors from the customer support form, so new specific errors can be displayed.
                    $('#customer_support_errors_list').text("");

                    // Informing the user that an error was encountered when submitting the form.
                    $('#div_outcome_customer_support_submit_failure').show();
                    $('#paragraph_outcome_customer_support_submit_failure').text(response.submit_form_outcome);
                    
                    // Iterating through the specific errors and displaying each on a separate line, without any bulletpoints.
                    for(let element in response.error_messages) {
                        response.error_messages[element].forEach(error => {
                            $('#customer_support_errors_list').append(`<li>${element} is required </li>`);
                            $('#customer_support_errors_list').css("list-style-type", "none");
                        });
                    }

                    // Show the list of specific errors that were encountered in the form.
                    $('#div_customer_support_errors').show();
                }
            },

            // If there was an error encountered when the POST request was made, we will log the error to the console.
            error: function(error) {
                console.log(error);
            }
        });
    });
});