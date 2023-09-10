from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.check_if_works)
]