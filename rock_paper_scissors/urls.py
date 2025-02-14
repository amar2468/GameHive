from django.urls import path
from . import views

app_name = 'rock_paper_scissors'

urlpatterns = [
    path('single_player_rps/', views.single_player_rps, name='single_player_rps'),
    path('multiplayer_rps_start_game/', views.multiplayer_rps_start_game, name='multiplayer_rps_start_game'),
    path('rps_form_submitted/', views.rps_form_submitted, name='rps_form_submitted')
]