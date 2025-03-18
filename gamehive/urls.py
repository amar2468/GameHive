"""gamehive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('guess_the_digit/', include('guess_the_digit.urls')),
    path('rock_paper_scissors/', include('rock_paper_scissors.urls')),
    path('', views.homepage, name='homepage'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('testimonials_page/', views.testimonials_page, name='testimonials_page'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('update_personal_details/', views.update_personal_details, name='update_personal_details'),
    path('change_password/', views.change_password, name='change_password'),
    path('redeeming_points/', views.redeeming_points, name='redeeming_points'),
    path('remove_testimonial/', views.remove_testimonial, name='remove_testimonial'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.log_out, name='logout')
]

handler404 = views.page_does_not_exist
