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
            url: "{% url 'manage_users' %}",

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