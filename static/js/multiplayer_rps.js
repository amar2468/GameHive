let round_number = 1;

let username = document.getElementById("username").value;

$('.multiplayer_rps_play_again').click(function () {
    window.location.href = $('.multiplayer_rps_play_again').data("url");
});

$('.multiplayer_back_to_homepage_button').click(function() {
    window.location.href = $('.multiplayer_back_to_homepage_button').data("url");
});

// If the web app is using HTTP as the protocol, we want to use "ws" websocket
if (window.location.protocol === "http:") {
    gameSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/multiplayer_rps/'
    );
}

// If the web app is using HTTPS as the protocol, we want to use "wss" websocket.
else {
    gameSocket = new WebSocket(
        'wss://' + window.location.host +
        '/ws/multiplayer_rps/'
    );
}

const message = {
    user_option : "",
    message: "Rock, Paper, Scissors multiplayer game connection succeeded!",
    username : username
};

gameSocket.addEventListener("open", (event) => {
    console.log('WebSocket connection opened:', event);
    gameSocket.send(JSON.stringify(message));
});

gameSocket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    console.log('Received message from server:', message);

    $('#multiplayer_rps_game_heading').text("Room Number: " + message.rps_room_name);

    if (message.type === 'start_rps_game') {
        $('#start_multiplayer_game').show();
        $('#loading_screen_waiting_for_opponent_div').removeClass('d-flex').hide();
        $('#loading_screen_waiting_for_opponent_div').hide();
    }

    else if(message.type === 'end_game') {
        if ($('#multiplayer_rps_end_of_game_info_modal').is(':hidden')) {
            $('#waiting_for_opponent_choice').hide();
            $('#session_disconnected_modal').modal('show');
        }
    }

    // If the opponent makes their move first, we want to inform the user that the opponent made their choice.
    else if (message.type === 'opponent_move') {
        // We only want to change the text and loading spinner (to signify that an opponent has made their choice) if
        // the user is the opponent.
        if (username != message.opponent_username) {
            // Clearing the text that says that we are waiting for the opponent to make a choice
            $('#waiting_for_opponent_status').text("");

            // Saying that the opponent has made their choice
            $('#waiting_for_opponent_status').text("Opponent has made their choice");

            // Hide the spinner as the opponent has made their choice
            $('#multiplayer_loading_rps').hide();
        }
    }

    if (message.hasOwnProperty('rps_options')) {
        let rps_options = message.rps_options;
        let user_list = message.user_list;

        for(let i = 0; i < user_list.length; i++)
        {
            if(user_list[i] !== username)
            {
                opponent_username = user_list[i];
                break;
            }
        }

        if (rps_options[opponent_username]["outcome_of_round"] != "")
        {                    
            if (rps_options[opponent_username]["user_option"] === "rock")
            {
                $('#paper_opponent').hide();
                $('#scissors_opponent').hide();
                $('#rock_opponent').show();
                $('#waiting_for_opponent_choice').hide();
            }

            else if (rps_options[opponent_username]["user_option"] === "paper")
            {
                $('#rock_opponent').hide();
                $('#scissors_opponent').hide();
                $('#paper_opponent').show();
                $('#waiting_for_opponent_choice').hide();
            }

            else if (rps_options[opponent_username]["user_option"] === "scissors")
            {
                $('#rock_opponent').hide();
                $('#paper_opponent').hide();
                $('#scissors_opponent').show();
                $('#waiting_for_opponent_choice').hide();
            }

            if (rps_options[username]["outcome_of_game"] == "Game Over! You failed to win this game! Good luck next time!" || rps_options[username]["outcome_of_game"] == "Game Over! You won this game! You have received 10 points!")
            {
                // Disabling the option to pick an option (rock,paper,scissors) as the game has ended and we don't want the 
                // user to choose any options anymore.
                $('.user_selected_rps_choice').css({
                    'pointer-events' : 'none',
                    'cursor' : 'default'
                });

                $('#user_wins').text("");
                $('#opponent_wins').text("");
                
                $('#user_wins').text(rps_options[username]["total_wins"]);
                $('#opponent_wins').text(rps_options[opponent_username]["total_wins"]);

                $('#multiplayer_rps_outcome').text(rps_options[username]["outcome_of_game"]);

                $('#rock_opponent').hide();
                $('#paper_opponent').hide();
                $('#scissors_opponent').hide();
                $('#waiting_for_opponent_choice').hide();

                $('#multiplayer_attempts_div').hide();

                $('#multiplayer_rps_outcome_div').show();

                $('#multiplayer_loading_rps').hide();

                $('.multiplayer_rps_end_of_game_info').text(rps_options[username]["outcome_of_game"]);

                setTimeout(function() {
                    $('#multiplayer_rps_end_of_game_info_modal').modal('show');
                }, 1000);
            }
            
            else
            {
                $('#carousel_rps_opponent').show();

                // Removing next/previous buttons from carousel as we don't want user to change this when they already
                // made their choice
                $('#carousel_control_prev_for_user').hide();
                $('#carousel_control_next_for_user').hide();

                $('#user_selection_prompt').text("You chose " + rps_options[username]["user_option"] + "!");

                $('#multiplayer_rps_outcome').text("You " + rps_options[username]["outcome_of_round"]);
                $('#multiplayer_rps_outcome_div').show();

                setTimeout(function() {
                    // After waiting for 2 seconds, we will reset the opponent options and bring back the loading spinner
                    // which indicates that we are waiting for the opponent to make their choice.
                    $('#paper_opponent').hide();
                    $('#scissors_opponent').hide();
                    $('#rock_opponent').hide();
                    $('#waiting_for_opponent_choice').show();

                    // Re-enable the option to click on the rock,paper,scissor options (it was disabled when the user
                    // already made their choice, so that multiple options weren't selected at once.
                    $('.user_selected_rps_choice').css({
                        'pointer-events' : '',
                        'cursor' : ''
                    });

                    // We are hiding the div that displays whether the user won/lost/drew in the current round. This is because
                    // we want to start the new round, so this is being reset for that purpose.
                    $('#multiplayer_rps_outcome_div').hide();

                    // Reset the text that informs what choice the user picked.
                    $('#user_selection_prompt').text("Make your choice!");
                    
                    // After removing the next/previous option from the carousel, we are bringing it back so the user
                    // can pick their next option.
                    $('#carousel_control_prev_for_user').show();
                    $('#carousel_control_next_for_user').show();

                    // As we are moving to the next round, we are increasing the round number by 1 and updating the text to
                    // display the correct round number.
                    round_number += 1;
                    $('#current_round_number').text("Round " + round_number);
                    
                    $('#user_wins').text("");
                    $('#opponent_wins').text("");

                    $('#user_wins').text(rps_options[username]["total_wins"]);
                    $('#opponent_wins').text(rps_options[opponent_username]["total_wins"]);

                    // We are the clearing the text that displays whether opponent made their choice or not
                    $('#waiting_for_opponent_status').text("");

                    // We are bringing the text that displays whether opponent made their choice or not back to default,
                    // which is that we are waiting for opponent to make their choice
                    $('#waiting_for_opponent_status').text("Waiting for opponent to choose their option");

                    // Return the spinner, as we are moving on to the next round
                    $('#multiplayer_loading_rps').show();

                }, 2000);
            }
        }

        console.log('Received rps_options:', rps_options);
    }
});

gameSocket.addEventListener("error", (event) => {
    console.error('WebSocket error:', event);
});

gameSocket.addEventListener("close", (event) => {
    console.log('WebSocket connection closed:', event);
});

// When the user chooses an option (rock,paper,scissors), it will jump to this block and perform numerous steps
// such as displaying the user choice, hiding the arrows, and sending the response back to the server.
$('.user_selected_rps_choice').click(function (e) {

    $('.user_selected_rps_choice').css({
        'pointer-events' : 'none',
        'cursor' : 'default'
    });

    var selected_rps_user = $('#carousel_rps_user .carousel-item.active').data('value');
    $('#user_selection_prompt').text("You chose " + selected_rps_user + "!");

    // Removing next/previous buttons from carousel as we don't want user to change this when they already
    // made their choice.
    $('#carousel_control_prev_for_user').hide();
    $('#carousel_control_next_for_user').hide();


    gameSocket.send(JSON.stringify({
        'type' : "rps_move",
        'user_option': selected_rps_user,
        'username': username
    }));
});