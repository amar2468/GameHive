$(document).ready(function() {
    $('[data-bs-toggle="tooltip"]').tooltip();

    $('#customer_support_form').on("submit", function(e) {
        e.preventDefault();
    });
});