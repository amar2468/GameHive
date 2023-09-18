from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.check_if_works, name='play')
]