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

    // If the user clicks on the "Closed Requests" tab, it will hide the button to delete the record
    $(document).on("click", "#closed_requests_tab", function() {
        $('.admin_options_delete').hide();
    });

    // If the user clicks on the "Unassigned Requests" tab, it will re-display the button to delete the record
    $(document).on("click", "#unassigned_requests_tab", function() {
        $('.admin_options_delete').show();
    });

    // If the user clicks on the "Assigned To Me" tab, it will re-display the button to delete the record
    $(document).on("click", "#assigned_to_me_tab", function() {
        $('.admin_options_delete').show();
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

    // If the admin clicks on the "select all" button, it will either select all or unselect all options.
    $(document).on("click", ".select_all_user_requests", function() {
        // If all the rows are already selected and the "select all" option is clicked again, it will deselect all the rows
        if (($('.select-row').length) == ($('.select-row:checked').length)) {
            // Deselects all the rows and deselects the "select all" option
            $('.select-row').prop("checked", false);
            $('.select_all_user_requests').prop("checked", false);

            // Disabling the "delete user request" button, when no rows are selected.
            $('.admin_options_delete').prop("disabled", true);
        }

        // If all rows are NOT selected and the "select all" option is chosen, it will select all the rows.
        else {
            // Selects all the rows and selects the "select all" option
            $('.select-row').prop("checked", true);
            $('.select_all_user_requests').prop("checked", true);

            // Enabling the "delete user request" button, when all rows are selected.
            $('.admin_options_delete').prop("disabled", false);
        }
    });

    // When the row in the table is clicked, the checkbox will be checked. This means that we don't have to explicitly click
    // the checkbox. All that is needed is a click on that row for the checkbox to be checked.
    $(document).on("click", ".user-row", function() {
        // Get the current row
        let select_this_row = $(this).find('.select-row');

        // Check if it is checked/unchecked and do the inverse to the checkbox, which makes it a toggle.
        select_this_row.prop("checked", !select_this_row.prop("checked"));

        // If no rows are selected, we will disable the "delete user request" button and uncheck the "select all" button.
        if (($('.select-row:checked').length) === 0) {
            $('.admin_options_delete').prop("disabled", true);
            $('.select_all_user_requests').prop("checked", false);
        }

        // If all individual rows are selected (checked), we will select the "select all" option to be enabled.
        else if (($('.select-row:checked').length) === ($('.select-row').length)) {
            $('.select_all_user_requests').prop("checked", true);
        }

        // If at least one row is selected (but not all rows), we will enable the "delete user request" button and uncheck the
        // select all button, if checked.
        else {
            $('.admin_options_delete').prop("disabled", false);
            $('.select_all_user_requests').prop("checked", false);
        }
    });

    // To prevent the error of not being able to click on the checkbox directly, we need to include this part.
    $(document).on("click", ".select-row", function(e) {
        e.stopPropagation();

        // If no rows are selected, we will disable the "delete user request" button and uncheck the "select all" button.
        if (($('.select-row:checked').length) === 0) {
            $('.admin_options_delete').prop("disabled", true);
            $('.select_all_user_requests').prop("checked", false);
        }

        // If all individual rows are selected (checked), we will select the "select all" option to be enabled.
        else if (($('.select-row:checked').length) === ($('.select-row').length)) {
            $('.select_all_user_requests').prop("checked", true);
        }

        // If at least one row is selected (but not all rows), we will enable the "delete user request" button and uncheck the
        // select all button, if checked.
        else {
            $('.admin_options_delete').prop("disabled", false);
            $('.select_all_user_requests').prop("checked", false);
        }
    });

});