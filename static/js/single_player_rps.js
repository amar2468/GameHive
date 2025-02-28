$(document).ready(function(){
    $('#carousel_rps_player').carousel();

    $('#carousel_control_prev_player').click(function(){
        $('#carousel_rps_player').carousel('prev');
    });

    $('#carousel_control_next_player').click(function(){
        $('#carousel_rps_player').carousel('next');
    });

    // If the user wants to replay the rps game, this button will make a get request and load the new game
    $('#rps_replay_game').on("click", function() {
        window.location.href = $('#rps_replay_game').data("url");
    });

    // If the user wants to go back to the homepage after playing the rps game, this function will redirect them to the homepage.
    $('#back_to_homepage_button').on("click", function() {
        window.location.href = $('#back_to_homepage_button').data("url");
    });

    $('.selected_rps').click(function(e){
        e.preventDefault();

        $('.selected_rps').css({
            'pointer-events' : 'none',
            'cursor' : 'default'
        });

        // Hide the carousel next and previous buttons, as we don't want the user to change their choice mid game.
        $('#carousel_control_prev_player').hide();
        $('#carousel_control_next_player').hide();

        $('#waiting_for_computer_choice').show();

        setTimeout(function() {

            rps_form_submission();

        }, 2000);
    });

    function rps_form_submission() 
    {
        var selected_rps_player = $('#carousel_rps_player .carousel-item.active').data('value');

        var form_data = $('#rps_form').serialize();

        $('#carousel').val(selected_rps_player);

        form_data += '&carousel_value=' + selected_rps_player;
        
        $.ajax({
            type: 'POST',
            url: $('#rps_form').data("url"),
            data: form_data,

            success: function(response) {

                let computer_rps_choice = response.computer_rps_choice;

                if (computer_rps_choice === "rock")
                {
                    $('#paper_computer').hide();
                    $('#scissors_computer').hide();
                    $('#rock_computer').show();
                    // Hide the loading spinner
                    $('#waiting_for_computer_choice').hide();
                }

                else if (computer_rps_choice === "paper")
                {
                    $('#rock_computer').hide();
                    $('#scissors_computer').hide();
                    $('#paper_computer').show();
                    // Hide the loading spinner
                    $('#waiting_for_computer_choice').hide();
                }

                else if (computer_rps_choice === "scissors")
                {
                    $('#rock_computer').hide();
                    $('#paper_computer').hide();
                    $('#scissors_computer').show();
                    // Hide the loading spinner
                    $('#waiting_for_computer_choice').hide();
                }

                $('#carousel_rps_computer').show();

                if (response.rps_end_of_game == "Game Over! You failed to win this game! Good luck next time!" || response.rps_end_of_game == "Game Over! You won this game! You have received 10 points!")
                {
                    $('.selected_rps').css({
                        'pointer-events' : 'none',
                        'cursor' : 'default'
                    });

                    // Update the total wins counter for the user
                    $('#user_wins').text("");
                    $('#user_wins').text(response.user_total_wins);

                    // Update the total wins counter for the computer
                    $('#computer_wins').text("");
                    $('#computer_wins').text(response.computer_wins);

                    let round_number = response.round_number;
                    $('#rps_game_heading').text("Round " + round_number);

                    $('.rps_round_outcome').text("You " + response.rps_round_outcome);
                    
                    $('.rps_end_of_game_info').text(response.rps_end_of_game);

                    setTimeout(function() {
                        $('#rps_end_of_game_info_modal').modal('show');
                    }, 1000);

                    $('#rps_round_outcome_div').show();
                }
                
                else
                {
                    $('#carousel_control_prev_player').hide();
                    $('#carousel_control_next_player').hide();

                    $('#prompt_user_to_make_choice').text("You chose " + response.user_rps_choice);

                    let round_number = response.round_number;
                    $('#rps_game_heading').text("Round " + round_number);

                    $('.rps_round_outcome').text("You " + response.rps_round_outcome);

                    $('#rps_round_outcome_div').show();

                    setTimeout(function () {
                        // After waiting for 2 seconds, we will reset the opponent options and bring back the loading spinner
                        // which indicates that we are waiting for the opponent to make their choice.
                        $('#rock_computer').hide();
                        $('#paper_computer').hide();
                        $('#scissors_computer').hide();
                        // Show the loading spinner again, as the new round will be played.
                        $('#waiting_for_computer_choice').show();
                        
                        // Re-enable the option to click on the rock,paper,scissor options (it was disabled when the user
                        // already made their choice, so that multiple options weren't selected at once.)
                        $('.selected_rps').css({
                            'pointer-events' : '',
                            'cursor' : ''
                        });

                        // Hiding the outcome of the current round, as we load the new round.
                        $('#rps_round_outcome_div').hide();

                        // After removing the next/previous option from the carousel, we are bringing it back so the user
                        // can pick their next option.
                        $('#carousel_control_prev_player').show();
                        $('#carousel_control_next_player').show();

                        // Update the total wins counter for the user
                        $('#user_wins').text("");
                        $('#user_wins').text(response.user_total_wins);

                        // Update the total wins counter for the computer
                        $('#computer_wins').text("");
                        $('#computer_wins').text(response.computer_wins);

                        // Set the prompt text to the default
                        $('#prompt_user_to_make_choice').text("Make your choice!");

                    }, 2000);
                }

            },

            error: function(error) {
                console.error(error);
            }
        });
    }
});