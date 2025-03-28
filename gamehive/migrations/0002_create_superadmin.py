# Generated by Django 4.2.9 on 2025-03-26 09:10

from django.db import migrations
from django.conf import settings

def create_superadmin(apps, schema_editor):
    CustomUserModel = apps.get_model("gamehive", "CustomUser")

    if not CustomUserModel.objects.exists():
        # Using the credentials from the .env file to create the super admin
        USERNAME_SUPER_ADMIN = settings.SUPER_ADMIN_USERNAME
        EMAIL_SUPER_ADMIN = settings.SUPER_ADMIN_EMAIL
        PASSWORD_SUPER_ADMIN = settings.SUPER_ADMIN_PASSWORD

        # Using the .env credentials to create an account for the super admin, who will be the owner of the web application
        CustomUserModel.objects.create_user(
            first_name="Amar",
            last_name="Plakalo",
            username=USERNAME_SUPER_ADMIN,
            email=EMAIL_SUPER_ADMIN,
            password=PASSWORD_SUPER_ADMIN,
            account_type="super_admin"
        )

class Migration(migrations.Migration):

    # The dependency reference ensures that the super admin will only be added when all migrations are applied.
    dependencies = [
        ('gamehive', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superadmin)
    ]