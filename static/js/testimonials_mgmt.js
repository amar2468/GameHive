$(document).ready(function() {
    // When we are on the "Testimonials Management" page, we want the "Admin Dashboard" nav link to be highlighted.
    $('#admin_dashboard_link').addClass('highlight_sign_up_nav_link_in_login_page');

    // Initialise the HTML table to be a datatable, with the "sort" option disabled for the first column.
    new DataTable("#manage_testimonials_table", {
        columnDefs: [
            { orderable:false, targets:0 }
        ]
    });

    // When the admin clicks the button the refresh the page, we will perform a GET request and bring the changes
    // from the page without a page reload.
    $('#refresh_testimonials_btn').click(function() {
        $.ajax({
            type: 'GET',
            url: "{% url 'testimonials_mgmt' %}",

            // If the page refresh was successful, we will perform the below.
            success: function(response) {
                // We are clearing the information from the datatable, so that it can be updated with the latest info
                let manage_testimonials_table = $('#manage_testimonials_table').DataTable();
                manage_testimonials_table.destroy();
                
                // Find the main section (whole page) and update the HTML with the new info
                let main_section_refresh = $(response).find("#main_section").html();
                $('#main_section').html(main_section_refresh);

                // Update the datatable with the new information.
                $('#manage_testimonials_table').DataTable({
                    columnDefs: [
                        { orderable: false, targets: 0 }
                    ]
                });
                
            },

            // If an error was encountered, we will log it to the console.
            error: function(error) {
                console.log(error);
            }
        })
    });

    // If the user clicks on the "select all" button, it will either select all or unselect all options.
    $(document).on("click", "#select_all_testimonials", function() {
        // If all the rows are already selected and the "select all" option is clicked again, it will deselect all the rows
        if (($('.select-row').length) === ($('.select-row:checked').length))
        {
            $('.select-row').prop("checked", false);
            $('#select_all_testimonials').prop("checked", false);
        }

        // If all rows are NOT selected and the "select all" option is chosen, it will select all the rows.
        else {
            $('.select-row').prop("checked", true);
            $('#select_all_testimonials').prop("checked", true);
        }
    });

    // When the row in the table is clicked, the checkbox will be checked. This means that we don't have to explicitly click
    // the checkbox. All that is needed is a click on that row for the checkbox to be checked.
    $(document).on("click", ".testimonial-row", function() {
        // Get the current row
        let select_this_row = $(this).find(".select-row");

        // Check if it is checked/unchecked and do the inverse to the checkbox, which makes it a toggle.
        select_this_row.prop("checked", !select_this_row.prop("checked"));
    });

    // To prevent the error of not being able to click on the checkbox directly, we need to include this part.
    $(document).on("click", ".select-row", function(e) {
        e.stopPropagation();
    });

});