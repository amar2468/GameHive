$(document).ready(function() {

    // Highlighting the "Admin Dashboard" nav-link, to indicate that we are on that page.
    $('#admin_dashboard_link').addClass('highlight_specific_navlink');

    // Creating three datatables, one for storing unassigned requests, one for storing requests assigned to the specific admin
    // that is logged in, and the other table for storing closed requests
    new DataTable("#unassigned_user_requests_table");
    new DataTable("#assigned_to_me_user_requests_table");
    new DataTable("#closed_user_requests_table");

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

});