$(document).ready(function() {
    $('#homepage_link').css("color", "#FFFFFF");
    $('#testimonials_link').css("color", "#FFFFFF");
    $('#customer_support_link').css("color", "#FFFFFF");
    $('#profile_link').css("color", "#FFFFFF");
    $('#admin_dashboard_link').css("color", "#FFFFFF")
    $('#logout_link').css("color", "#FFFFFF");
    $('#sign_up_link').css("color", "#FFFFFF");

    let currentPath = window.location.pathname;
    
    let homepage_url = $('#homepage_link').data("url");
    let testimonials_url = $('#testimonials_link').data("url");
    let customer_support_url = $('#customer_support_link').data("url");
    let profile_url = $('#profile_link').data("url");
    let admin_dashboard_url = $('#admin_dashboard_link').data("url");
    let logout_url = $('#logout_link').data("url");
    let sign_up_url = $('#sign_up_link').data("url");

    if (currentPath == homepage_url)
    {
        $('#homepage_link').css("color", "yellow");

        $('#testimonials_link').css("color", "#FFFFFF");
        $('#customer_support_link').css("color", "#FFFFFF");
        $('#profile_link').css("color", "#FFFFFF");
        $('#admin_dashboard_link').css("color", "#FFFFFF");
        $('#logout_link').css("color", "#FFFFFF");
        $('#sign_up_link').css("color", "#FFFFFF");
    }

    else if (currentPath == testimonials_url)
    {
        $('#testimonials_link').css("color", "yellow");

        $('#homepage_link').css("color", "#FFFFFF");
        $('#profile_link').css("color", "#FFFFFF");
        $('#customer_support_link').css("color", "#FFFFFF");
        $('#admin_dashboard_link').css("color", "#FFFFFF");
        $('#logout_link').css("color", "#FFFFFF");
        $('#sign_up_link').css("color", "#FFFFFF");
    }

    else if (currentPath == customer_support_url) {
        $('#customer_support_link').css("color", "yellow");

        $('#homepage_link').css("color", "#FFFFFF");
        $('#profile_link').css("color", "#FFFFFF");
        $('#admin_dashboard_link').css("color", "#FFFFFF");
        $('#logout_link').css("color", "#FFFFFF");
        $('#sign_up_link').css("color", "#FFFFFF");
    }

    else if (currentPath == profile_url)
    {
        $('#profile_link').css("color", "yellow");

        $('#homepage_link').css("color", "#FFFFFF");
        $('#testimonials_link').css("color", "#FFFFFF");
        $('#customer_support_link').css("color", "#FFFFFF");
        $('#admin_dashboard_link').css("color", "#FFFFFF");
        $('#logout_link').css("color", "#FFFFFF");
        $('#sign_up_link').css("color", "#FFFFFF");
    }

    else if (currentPath == admin_dashboard_url)
    {
        $('#admin_dashboard_link').css("color", "yellow");

        $('#homepage_link').css("color", "#FFFFFF");
        $('#testimonials_link').css("color", "#FFFFFF");
        $('#customer_support_link').css("color", "#FFFFFF");
        $('#profile_link').css("color", "#FFFFFF");
        $('#logout_link').css("color", "#FFFFFF");
        $('#sign_up_link').css("color", "#FFFFFF");
    }

    else if (currentPath == logout_url)
    {
        $('#logout_link').css("color", "yellow");

        $('#homepage_link').css("color", "#FFFFFF");
        $('#testimonials_link').css("color", "#FFFFFF");
        $('#customer_support_link').css("color", "#FFFFFF");
        $('#profile_link').css("color", "#FFFFFF");
        $('#admin_dashboard_link').css("color", "#FFFFFF");
        $('#sign_up_link').css("color", "#FFFFFF");
    }

    else if(currentPath == sign_up_url)
    {
        $('#sign_up_link').css("color", "yellow");

        $('#homepage_link').css("color", "#FFFFFF");
        $('#testimonials_link').css("color", "#FFFFFF");
        $('#customer_support_link').css("color", "#FFFFFF");
        $('#profile_link').css("color", "#FFFFFF");
        $('#admin_dashboard_link').css("color", "#FFFFFF");
        $('#logout_link').css("color", "#FFFFFF");
    }

    $('#homepage_link').click(function () {
        window.location.href = homepage_url;
    });

    $('#testimonials_link').click(function() {
        window.location.href = testimonials_url;
    });

    $('#customer_support_link').click(function() {
        window.location.href = customer_support_url;
    })

    $('#profile_link').click(function() {
        window.location.href = profile_url;
    })

    $('#admin_dashboard_link').click(function() {
        window.location.href = admin_dashboard_url
    })

    $('#logout_link').click(function() {
        window.location.href = logout_url;
    });

    $('#sign_up_link').click(function() {
        window.location.href = sign_up_url;
    });
});