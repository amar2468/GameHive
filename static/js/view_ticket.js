$(document).ready(function() {

    // Highlighting the "Admin Dashboard" nav-link, to indicate that we are on that page
    $('#admin_dashboard_link').addClass('highlight_specific_navlink');

    // If the button to toggle the sidebar is clicked, we want to show/hide ticket info
    $(document).on("click", "#toggle_sidebar", function() {
        // If the ticket info is not being displayed, clicking the toggle button will display it.
        if ($('.ticket_info').css("display") === 'none') {
            $('.ticket_info').removeClass("d-none");
        }

        // If the ticket info is being displayed, clicking the toggle button will hide it.
        else {
            $('.ticket_info').addClass("d-none");
        }
    });

});