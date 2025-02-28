let correct_guess_div_guess_the_digit = document.getElementById("correct_guess_div_guess_the_digit");
let game_over_div_guess_the_digit = document.getElementById("game_over_div_guess_the_digit");

// Extracting the text from the objects above. We are checking whether the objects are null and if they are, they will be an empty string.

let correct_guess_div_guess_the_digit_text = "";
let game_over_div_guess_the_digit_text = "";

if (correct_guess_div_guess_the_digit != null)
{
    correct_guess_div_guess_the_digit_text = correct_guess_div_guess_the_digit.textContent;
}

if (game_over_div_guess_the_digit != null)
{
    game_over_div_guess_the_digit_text = game_over_div_guess_the_digit.textContent;
}

// Checking if the game is over. If it is, we want to hide some elements from the game, which are no longer relevant.
if (correct_guess_div_guess_the_digit_text === 'Correct guess! Well done!' || game_over_div_guess_the_digit_text.includes('Game over! The correct number was'))
{
    let easy_level_div = document.getElementById("easy_level_div");
    let medium_level_div = document.getElementById("medium_level_div");
    let hard_level_div = document.getElementById("hard_level_div");
    let div_for_replay_game_button = document.getElementById("div_for_replay_game_button");
    
    // Identifies the level of the game, which will be used as a parameter in the URL, if the user "replays" the game
    let level_identifier = ""

    // Hiding the divs that shows what range of numbers the user can guess, if the game is over
    if (easy_level_div != null)
    {
        easy_level_div.style.display = "none";
        level_identifier = "easy"
    }

    else if (medium_level_div != null) 
    {
        medium_level_div.style.display = "none";
        level_identifier = "medium"
    }

    else if (hard_level_div != null)
    {
        hard_level_div.style.display = "none";
        level_identifier = "hard"
    }

    // Hiding the hint for the user, if the game is over
    let hint_div = document.getElementById("hint_div");
    let hint_enabled = "no"

    if (hint_div != null)
    {
        hint_div.style.display = "none";
        // Tracking whether the hint was enabled, which will be used as a parameter in the URL, if the user "replays" the game
        hint_enabled = "yes"
    }

    div_for_replay_game_button.style.display = "block"
    div_for_going_back_to_homepage_button.style.display = "block"

    // Hiding the guessing form (where user can choose the number that they want to guess), if the game is over
    let guessing_game_form = document.getElementById("guessing_game_form");
    guessing_game_form.style.display = "none";

    
    let replay_game_button = document.getElementById("replay_game_button")

    let back_to_homepage_btn = document.getElementById("back_to_homepage_btn");

    replay_game_button.addEventListener("click", function() {
            let replay_game_url_without_params = $('#replay_game_button').data("url")
            let replay_game_url_with_params = replay_game_url_without_params + "?selected_level=" + level_identifier + "&hints=" + hint_enabled;
            
            window.location.href = replay_game_url_with_params;
    });

    back_to_homepage_btn.addEventListener("click", function() {
        let url = $('#back_to_homepage_btn').data("url");
        window.location.href = url;
    });
}