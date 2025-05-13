$(document).ready(function() {
    // If the button to toggle the sidebar is clicked, we want to show/hide ticket info
    $(document).on("click", "#toggle_sidebar", function() {
        // If the ticket info is not being displayed, clicking the toggle button will display it.
        if ($('.ticket_info').css("display") === 'none') {
            $('.custom_backdrop_for_sidebar').removeClass("d-none");
            $('.ticket_info').removeClass("d-none");
        }

        // If the ticket info is being displayed, clicking the toggle button will hide it.
        else {
            $('.custom_backdrop_for_sidebar').addClass("d-none");
            $('.ticket_info').addClass("d-none");
        }
    });

});