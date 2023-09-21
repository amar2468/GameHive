from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.guess_the_digit_game, name='play')
]