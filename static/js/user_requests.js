$(document).ready(function() {

    // Highlighting the "Admin Dashboard" nav-link, to indicate that we are on that page.
    $('#admin_dashboard_link').addClass('highlight_specific_navlink');
    
    // Disabling the button the delete the user request, when the page is initially loaded.
    $('.admin_options_delete').prop("disabled", true);

    // Creating three datatables, one for storing unassigned requests, one for storing requests assigned to the specific admin
    // that is logged in, and the other table for storing closed requests. We are also disabling the "sort" option in the
    // first column for each table.
    new DataTable("#unassigned_user_requests_table", {
        columnDefs: [
            { orderable:false, target:0 }
        ]
    });

    new DataTable("#assigned_to_me_user_requests_table", {
        columnDefs: [
            { orderable:false, target:0 }
        ]
    });

    new DataTable("#closed_user_requests_table", {
        columnDefs: [
            { orderable:false, target:0 }
        ]
    });

    // If the user clicks on the "Closed Requests" tab, it will disable the "delete user record" button, show only the table
    // that presents the "closed" user requests, and uncheck any checkboxes in the "closed" table.
    $(document).on("click", "#closed_requests_tab", function() {
        $('.admin_options_delete').prop("disabled", true);

        $('#closed_user_requests_table').show();
        $('#assigned_to_me_user_requests_table').hide();
        $('#unassigned_user_requests_table').hide();

        $('.select_all_user_requests').prop("checked", false);
        $('.select-row').prop("checked", false);
    });

    // If the user clicks on the "Unassigned Requests" tab, it will disable the "delete user record" button, show only the table
    // that presents the "Unassigned" user requests, and uncheck any checkboxes in the "Unassigned Requests" table.
    $(document).on("click", "#unassigned_requests_tab", function() {
        $('.admin_options_delete').prop("disabled", true);

        $('#unassigned_user_requests_table').show();
        $('#assigned_to_me_user_requests_table').hide();
        $('#closed_user_requests_table').hide();
        
        $('.select_all_user_requests').prop("checked", false);
        $('.select-row').prop("checked", false);
    });

    // If the user clicks on the "Assigned To Me" requests tab, it will disable the "delete user record" button, show only the table
    // that presents the "Assigned To Me" user requests, and uncheck any checkboxes in the "Assigned To Me" table.
    $(document).on("click", "#assigned_to_me_tab", function() {
        $('.admin_options_delete').prop("disabled", true);

        $('#assigned_to_me_user_requests_table').show();
        $('#closed_user_requests_table').hide();
        $('#unassigned_user_requests_table').hide();

        $('.select_all_user_requests').prop("checked", false);
        $('.select-row').prop("checked", false);
    });

    // When the admin clicks the button the refresh the page, we will perform a GET request and bring the changes
    // from the page without a page reload.
    $(document).on("click", ".admin_options_refresh_page", function() {
        $.ajax({
            type: "GET",
            url: $('.admin_options_refresh_page').data("url"),
            
            // If the page refresh was successful, we will perform the below.
            success: function(response) {
                // We are clearing the information from the datatable, so that it can be updated with the latest info
                let manage_unassigned_requests_table = $('#unassigned_user_requests_table').DataTable();
                let manage_assigned_to_me_requests_table = $('#assigned_to_me_user_requests_table').DataTable();
                let manage_closed_requests_table = $('#closed_user_requests_table').DataTable();

                manage_unassigned_requests_table.destroy();
                manage_assigned_to_me_requests_table.destroy();
                manage_closed_requests_table.destroy();

                // Find the main section (whole page) and update the HTML with the new info
                let main_section_refresh = $(response).find("#main_section").html();
                $('#main_section').html(main_section_refresh);

                // Update the datatables with the new information.
                $('#unassigned_user_requests_table').DataTable();
                $('#assigned_to_me_user_requests_table').DataTable();
                $('#closed_user_requests_table').DataTable();

            },

            // If an error was encountered, we will log it to the console.
            error: function(error) {
                console.log(error);
            }
        })
    });

    // If the admin clicks on the button to delete the user request(s), a POST request will be performed, sending the 
    // relevant info to the backend for processing.
    $(document).on("click", ".admin_options_delete", function() {
        // Creating an empty list that will store the user request(s) that need to be deleted (this would be all the user requests that 
        // the admin selected using the checkbox)
        let user_requests_to_delete_list = [];

        // Iterating through all the rows that were "checked", and then finding the ticket ID of the user request(s) to delete
        $('.select-row:visible:checked').each(function() {
            // Find the row where this checkbox resides in
            let checked_row = $(this).closest("tr");

            // Within the row where the checkbox resides, find the element that stores the ticket ID of that user request
            let ticket_id_of_user_request_to_delete = checked_row.find(".ticket_id");

            // Add the ticket ID of the user request(s) to delete into the array
            user_requests_to_delete_list.push(ticket_id_of_user_request_to_delete[0].textContent);
        });

        $.ajax({
            type: "POST",
            url: $('.admin_options_delete').data("url"),
            data: JSON.stringify({
                user_requests_to_delete_list : user_requests_to_delete_list
            }),

            // As Django protects all POST requests with CSRF protection, we will need to use the csrf token when making the request
            headers: {
                "X-CSRFToken": $('#csrf_token').val()
            },

            // If the POST request was successful (no errors encountered from the backend), we will verify whether the user request records
            // have been deleted
            success: function(response) {
                // If the deletion of the user record(s) was successful, we will just populate the paragraph element with the success
                // message and display the div that holds the paragraph element.
                if (response.success === true) {
                    $('#paragraph_outcome_delete_user_request_success').text(response.status);
                    $('#div_outcome_delete_user_request_success').show();
                }

                // If the deletion of the user records(s) was unsuccessful, we will just populate the paragraph element with the failure
                // message and display the div that holds the paragraph element.
                else {
                    $('#paragraph_outcome_delete_user_request_failure').text(response.status);
                    $('#div_outcome_delete_user_request_failure').show();
                }

                // After 1 second, we want to refresh (not reload) the page, removing the success/failure messages and showing
                // the up-to-date user record tables.
                setTimeout(function() {
                    // We are clearing the success message and hiding the associated div, as we have already informed the admin
                    $('#paragraph_outcome_delete_user_request_success').text("");
                    $('#div_outcome_delete_user_request_success').hide();

                    // We are clearing the failure message and hiding the associated div, as we have already informed the admin
                    $('#paragraph_outcome_delete_user_request_failure').text("");
                    $('#div_outcome_delete_user_request_failure').hide();

                    // Refresh (not reload) the page by clicking on the refresh button.
                    $('.admin_options_refresh_page').click();
                }, 1000);
            },

            // If an error occurred, the error will be logged to the console.
            error: function(error) {
                console.log(error);
            }

        })
    });

    // If the admin clicks on the "select all" button, it will either select all or unselect all options.
    $(document).on("click", ".select_all_user_requests", function() {

        // If all the rows are already selected and the "select all" option is clicked again, it will deselect all the rows
        if (($('.select-row:visible').length) === ($('.select-row:visible:checked').length)) {
            // Deselects all the rows and deselects the "select all" option
            $('.select-row:visible').prop("checked", false);
            $('.select_all_user_requests:visible').prop("checked", false);

            // Disabling the "delete user request" button, when no rows are selected.
            $('.admin_options_delete').prop("disabled", true);
        }

        // If all rows are NOT selected and the "select all" option is chosen, it will select all the rows.
        else {
            // Selects all the rows and selects the "select all" option
            $('.select-row:visible').prop("checked", true);
            $('.select_all_user_requests:visible').prop("checked", true);

            // Enabling the "delete user request" button, when all rows are selected.
            $('.admin_options_delete').prop("disabled", false);
        }
    });

    // When the row in the table is clicked, the checkbox will be checked. This means that we don't have to explicitly click
    // the checkbox. All that is needed is a click on that row for the checkbox to be checked.
    $(document).on("click", ".user-record-row", function() {
        // Get the current row
        let select_this_row = $(this).find('.select-row:visible');

        // Check if it is checked/unchecked and do the inverse to the checkbox, which makes it a toggle.
        select_this_row.prop("checked", !select_this_row.prop("checked"));

        // If no rows are selected, we will disable the "delete user request" button and uncheck the "select all" button.
        if (($('.select-row:visible:checked').length) === 0) {
            $('.admin_options_delete').prop("disabled", true);
            $('.select_all_user_requests:visible').prop("checked", false);
        }

        // If all individual rows are selected (checked), we will select the "select all" option to be enabled.
        else if (($('.select-row:visible:checked').length) === ($('.select-row:visible').length)) {
            $('.select_all_user_requests:visible').prop("checked", true);
            $('.admin_options_delete').prop("disabled", false);
        }

        // If at least one row is selected (but not all rows), we will enable the "delete user request" button and uncheck the
        // select all button, if checked.
        else {
            $('.admin_options_delete').prop("disabled", false);
            $('.select_all_user_requests:visible').prop("checked", false);
        }
    });

    // To prevent the error of not being able to click on the checkbox directly, we need to include this part.
    $(document).on("click", ".select-row", function(e) {
        e.stopPropagation();

        // If no rows are selected, we will disable the "delete user request" button and uncheck the "select all" button.
        if (($('.select-row:visible:checked').length) === 0) {
            $('.admin_options_delete').prop("disabled", true);
            $('.select_all_user_requests:visible').prop("checked", false);
        }

        // If all individual rows are selected (checked), we will select the "select all" option to be enabled.
        else if (($('.select-row:visible:checked').length) === ($('.select-row:visible').length)) {
            $('.select_all_user_requests:visible').prop("checked", true);
            $('.admin_options_delete').prop("disabled", false);
        }

        // If at least one row is selected (but not all rows), we will enable the "delete user request" button and uncheck the
        // select all button, if checked.
        else {
            $('.admin_options_delete').prop("disabled", false);
            $('.select_all_user_requests:visible').prop("checked", false);
        }
    });

});