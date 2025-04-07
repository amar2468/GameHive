$(document).ready(function() {
    // When we are on the "Manage Users" page, we want the "Admin Dashboard" nav link to be highlighted.
    $('#admin_dashboard_link').addClass('highlight_sign_up_nav_link_in_login_page');

    // Disabling the button the delete the user, when the page is initially loaded.
    $('.admin_options_delete').prop("disabled", true);

    // Initialise the HTML table to be a datatable, with the "sort" option disabled for the first column.
    new DataTable('#manage_users_table', {
        columnDefs: [
            { orderable:false, targets:0 }
        ]
    });
    
    // When the admin clicks the button the refresh the page, we will perform a GET request and bring the changes
    // from the page without a page reload.
    $('#refresh_users_btn').click(function() {
        $.ajax({
            type: 'GET',
            url: $('.admin_options_delete').data("url"),

            // If the page refresh was successful, we will perform the below.
            success: function(response) {
                // We are clearing the information from the datatable, so that it can be updated with the latest info
                let manage_users_table = $('#manage_users_table').DataTable();
                manage_users_table.destroy();

                // Find the main section (whole page) and update the HTML with the new info
                let main_section_refresh = $(response).find("#main_section").html();
                $('#main_section').html(main_section_refresh);
                
                // Update the datatable with the new information.
                $('#manage_users_table').DataTable({
                    columnDefs: [
                        { orderable: false, targets: 0 }
                    ]
                });
            },
            
            // If an error was encountered, we will log it to the console.
            error: function(error) {
                console.log(error);
            }

        });
    });

    // If the admin clicks on the button to delete a user/users, a POST request will be performed, sending the relevant
    // info to the backend for processing.
    $(document).on("click", ".admin_options_delete", function() {
        // Creating an empty list that will store the users that need to be deleted (this would be all the users that the admin
        // selected using the checkbox)
        let users_to_delete_list = [];

        // Iterating through all the rows that were "checked", and then finding the username of the user to delete
        $('.select-row:checked').each(function() {
            // Find the row where this checkbox resides in
            let checked_row = $(this).closest("tr");

            // Within the row where the checkbox resides, find an element that stores the username of that user
            let username_to_delete = checked_row.find("#username_link_manage_users");

            // Add the username to delete into the array
            users_to_delete_list.push(username_to_delete[0].textContent);
        });

        // When the admin chooses the user(s) to delete and clicks the button to delete the users, a POST request will
        // be made and the list of user(s) to delete will be sent to the backend for processing.
        $.ajax({
            type: 'POST',
            url: $('.admin_options_delete').data("url"),
            data: JSON.stringify({
                users_to_delete_list : users_to_delete_list
            }),
            // As Django protects all POST requests with CSRF protection, we will need to use the csrf token when making the request
            headers: {
                "X-CSRFToken": $('#csrf_token').val()
            },

            // If the POST request was successful (no errors encountered from the backend), we will verify whether the user(s) record
            // has been removed.
            success: function(response) {
                // If the deletion of the user(s) was successful, we will just populate the paragraph element with the success
                // message and display the div that holds the paragraph element.
                if (response.success === true) {
                    $('#paragraph_outcome_delete_user_success').text(response.status);
                    $('#div_outcome_delete_user_success').show();
                }
                
                // If the deletion of the user(s) was unsuccessful, we will just populate the paragraph element with the failure
                // message and display the div that holds the paragraph element.
                else {
                    $('#paragraph_outcome_delete_user_failure').text(response.status);
                    $('#div_outcome_delete_testimonial_success').show();
                }

                // After 1 second, we want to refresh (not reload) the page, removing the success/failure messages and showing
                // the up-to-date user table.
                setTimeout(function() {
                    // We are clearing the success message and hiding the associated div, as we have already informed the admin
                    $('#paragraph_outcome_delete_user_success').text("");
                    $('#div_outcome_delete_user_success').hide();

                    // We are clearing the failure message and hiding the associated div, as we have already informed the admin
                    $('#paragraph_outcome_delete_user_failure').text("");
                    $('#div_outcome_delete_testimonial_success').hide();

                    // Refresh (not reload) the page by clicking on the refresh button.
                    $('#refresh_users_btn').click();
                }, 1000);
            },

            // If an error occurred, the error will be logged to the console.
            error: function(error) {
                console.log(error);
            }
        });

    });

    // If the user clicks on the "select all" button, it will either select all or unselect all options.
    $(document).on("click", "#select_all_users", function() {

        // If all the rows are already selected and the "select all" option is clicked again, it will deselect all the rows
        if (($('.select-row').length) === ($('.select-row:checked').length))
        {
            // Deselects all the rows and deselects the "select all" option
            $('.select-row').prop("checked", false);
            $('#select_all_users').prop("checked", false);

            // Disabling the "delete user" button, when no rows are selected.
            $('.admin_options_delete').prop("disabled", true);
        }

        // If all rows are NOT selected and the "select all" option is chosen, it will select all the rows.
        else {
            // Selects all the rows and selects the "select all" option
            $('.select-row').prop("checked", true);
            $('#select_all_users').prop("checked", true);

            // Enabling the "delete user" button, when all rows are selected.
            $('.admin_options_delete').prop("disabled", false);
        }

    });

    // When the row in the table is clicked, the checkbox will be checked. This means that we don't have to explicitly click
    // the checkbox. All that is needed is a click on that row for the checkbox to be checked.
    $(document).on("click", ".user-row", function() {
        // Get the current row
        let select_this_row = $(this).find(".select-row");

        // Check if it is checked/unchecked and do the inverse to the checkbox, which makes it a toggle.
        select_this_row.prop("checked", !select_this_row.prop("checked"));

        // If no rows are selected, we will disable the "delete user" button and uncheck the "select all" button.
        if (($('.select-row:checked').length) === 0) {
            $('.admin_options_delete').prop("disabled", true);
            $('#select_all_users').prop("checked", false);
        }

        // If all individual rows are selected (checked), we will select the "select all" option to be enabled.
        else if (($('.select-row:checked').length) === ($('.select-row').length)) {
            $('#select_all_users').prop("checked", true);
        }
        
        // If at least one row is selected, we will enable the "delete user" button.
        else {
            $('.admin_options_delete').prop("disabled", false);
        }
    });

    // To prevent the error of not being able to click on the checkbox directly, we need to include this part.
    $(document).on("click", ".select-row", function(e) {
        e.stopPropagation();

        // If no rows are selected, we will disable the "delete user" button and uncheck the "select all" button.
        if (($('.select-row:checked').length) === 0) {
            $('.admin_options_delete').prop("disabled", true);
            $('#select_all_users').prop("checked", false);
        }

        // If all individual rows are selected (checked), we will select the "select all" option to be enabled.
        else if (($('.select-row:checked').length) === ($('.select-row').length)) {
            $('#select_all_users').prop("checked", true);
        }
        
        // If at least one row is selected, we will enable the "delete user" button.
        else {
            $('.admin_options_delete').prop("disabled", false);
        }
    });

});