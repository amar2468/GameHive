from django.db import models
from django.contrib.auth.models import User

class GameUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_score = models.IntegerField(default=0)

class TestimonialsModel(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_testimonial = models.DateTimeField(auto_now_add=True)
    message = models.TextField()