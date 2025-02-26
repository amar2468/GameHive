$(document).ready(function () {
    $('#guessing_game_config_form').submit(function(event) {
        event.preventDefault();

        var selected_level = $('select[name="selected_level"]').val();

        var hints = $('select[name="hints"]').val();

        if(selected_level === 'easy')
        {
          if(hints === 'yes')
          {
            $('#selected-value').text(selected_level + " level. In this level, you have to guess a number between 1 and 10. You will have 2 guesses to do so. If you guess correctly, you will receive 5 points.");
          }

          else
          {
            $('#selected-value').text(selected_level + " level. In this level, you have to guess a number between 1 and 10. You will have 4 guesses to do so. If you guess correctly, you will receive 10 points.");
          }
          
        }

        else if(selected_level === 'medium')
        {
          if(hints === 'yes')
          {
            $('#selected-value').text(selected_level + " level. In this level, you have to guess a number between 1 and 50. You will have 5 guesses to do so. If you guess correctly, you will receive 25 points.");
          }

          else
          {
            $('#selected-value').text(selected_level + " level. In this level, you have to guess a number between 1 and 50. You will have 10 guesses to do so. If you guess correctly, you will receive 50 points.");
          }
        }

        else if(selected_level === 'hard')
        {
          if(hints === 'yes')
          {
            $('#selected-value').text(selected_level + " level. In this level, you have to guess a number between 1 and 100. You will have 10 guesses to do so. If you guess correctly, you will receive 50 points.");
          }

          else
          {
            $('#selected-value').text(selected_level + " level. In this level, you have to guess a number between 1 and 100. You will have 20 guesses to do so. If you guess correctly, you will receive 100 points.");
          }
        }

        $('#config_modal').modal('show');
    });

    $('#play_game').click(function() {
        let form_info = $('#guessing_game_config_form').serialize();

        let guess_the_digit_game_url = $('#play_game').data("url");

        var url = guess_the_digit_game_url + form_info;
        
        window.location.href = url;
    });
});