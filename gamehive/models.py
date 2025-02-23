from django.db import models
from django.contrib.auth.models import User

class GameUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_score = models.IntegerField(default=0)

class PersonalDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)

class TestimonialsModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_testimonial = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    star_rating = models.IntegerField()