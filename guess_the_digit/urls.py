from django.urls import path
from . import views

app_name = 'guess_the_digit'

urlpatterns = [
    path('play/', views.guess_the_digit_game, name='play'),
    path('config/', views.guess_the_digit_config, name='config')
]