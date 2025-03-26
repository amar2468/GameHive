from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    account_type = models.CharField(max_length=25)

class GameUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_score = models.IntegerField(default=0)

class TestimonialsModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_testimonial = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    star_rating = models.IntegerField()