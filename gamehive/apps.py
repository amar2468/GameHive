from django.apps import AppConfig
from django.conf import settings

class GameHiveConfig(AppConfig):
    # Defining the name of the app
    name='gamehive'

    # When Django is ready, it will call the function to create the super admin.
    def ready(self):
        from gamehive.models import CustomUser
        self.create_super_admin(CustomUser)

    # Function that creates the super admin if there are 0 users created.
    def create_super_admin(self, CustomUser):
        if not CustomUser.objects.exists():
            # Using the credentials from the .env file to create the super admin
            USERNAME_SUPER_ADMIN = settings.SUPER_ADMIN_USERNAME
            EMAIL_SUPER_ADMIN = settings.SUPER_ADMIN_EMAIL
            PASSWORD_SUPER_ADMIN = settings.SUPER_ADMIN_PASSWORD

            # Using the .env credentials to create an account for the super admin, who will be the owner of the web application
            CustomUser.objects.create_user(
                username=USERNAME_SUPER_ADMIN,
                email=EMAIL_SUPER_ADMIN,
                password=PASSWORD_SUPER_ADMIN,
                account_type="super_admin"
            )