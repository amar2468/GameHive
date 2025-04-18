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

class CustomerSupportModel(models.Model):
    requester_username = models.CharField(max_length=150)
    requester_email = models.EmailField(blank=True)
    ticket_id = models.BigAutoField(primary_key=True)
    ticket_request_type = models.CharField(max_length=150)
    ticket_title = models.CharField(max_length=150)
    ticket_description = models.TextField()
    ticket_attachments = models.FileField(upload_to="ticket_attachments/", blank=True, null=True)
    ticket_status = models.CharField(max_length=150)
    ticket_assigned_to = models.CharField(max_length=150)
    ticket_created_at = models.DateTimeField(auto_now_add=True)
    ticket_updated_at = models.DateTimeField(auto_now=True)
    ticket_comments = models.TextField(default='[]', blank=True)