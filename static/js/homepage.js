$(document).ready(function() {
    $('#form_rps_single_player_multiplayer').submit(function(e) {
        e.preventDefault();

        $('#rps_single_player_or_multiplayer_toggle').modal('show');
    });
});