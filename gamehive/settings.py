"""
Django settings for gamehive project.
"""

from pathlib import Path
import os
import environ
from dotenv import load_dotenv
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# If this will run locally, we want to load the .env file. This check is here because we don't have the .env file in the repo,
# so Jenkins wouldn't be able to get the credentials from it. Instead, Jenkins will use environment variables for this in the pipeline.
if os.getenv("JENKINS_ENV") is None:
    load_dotenv()

# Retrieving the credentials for the super admin, depending on if the application is run locally (will use .env) 
# or in Jenkins (will use environment variables)
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

redis_url = os.getenv("REDIS_URL")

# Getting the env variable "DJANGO_DEBUG" from .env file. The default value is set as "False", which will only be applied if
# the env variable cannot be found. The "== True" part is there because the os.getenv part will only return "True" or "False" as 
# a string but we want the value to be Boolean. So comparing it to "True" will either retrieve a True/False boolean value.
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Retrieves the env variable "DJANGO_ALLOWED_HOSTS". If nothing is specified, the default will be localhost. We are splitting it
# for every comma that appears, as we want a comma separated list.
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# We are specifying that we want Django to use CustomUser model as the user model, instead of the default (User model)
AUTH_USER_MODEL='gamehive.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'gamehive',
    'guess_the_digit',
    'rock_paper_scissors'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gamehive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [redis_url],
        },
    },
}

ASGI_APPLICATION = 'gamehive.asgi.application'

# Emails that are sent will be displayed in the console, for testing purposes.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Checking to see if the user ran "python manage.py runserver"
using_runserver = "runserver" in sys.argv

# If the Debug mode is turned on and the user is using "python manage.py runserver" to run the server, we don't want to use 
# whitenoise, as runserver automatically handles static files in Debug mode. We only need to set the STATIC_ROOT to point to
# the "staticfiles" folder, where collected static files will be stored
if DEBUG == True and using_runserver:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

# If Debug mode is turned on and the user is not using runserver (perhaps they are using something like uvicorn) to run the app,
# then we will set the STATIC_ROOT to point to the "staticfiles" folder, where collected static files will be stored. We are also
# configuring the server to use whitenoise for static file handling.
if DEBUG == True and not using_runserver:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# If Debug mode is turned off (which would be the case if this app is deployed), we will set the STATIC_ROOT to point to 
# the "staticfiles" folder in the specific location in Render, where collected static files will be stored.
    STATIC_ROOT = "/opt/render/project/src/staticfiles"

    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'