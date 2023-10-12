from django.db import models
from django.contrib.auth.models import User

class GameUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_score = models.IntegerField(default=0)