from django.urls import path
from . import views

app_name = 'rock_paper_scissors'

urlpatterns = [
    path('play/', views.play, name='play'),
    path('rps_form_submitted/', views.rps_form_submitted, name='rps_form_submitted'),
    path('update_personal_details/', views.update_personal_details, name='update_personal_details'),
    path('change_password/', views.change_password, name='change_password')
]