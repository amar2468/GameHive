from django.urls import path
from . import views

app_name = 'rock_paper_scissors'

urlpatterns = [
    path('play/', views.play, name='play')
]