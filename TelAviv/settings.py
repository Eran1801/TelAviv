"""
Django settings for TelAviv project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# --------- .env Variables ---------

# SECRET_KEY_DJANGO = os.environ['SECRET_KEY']
# DB_NAME = os.environ['DB_NAME']
# DB_PASSWORD = os.environ['DB_PAS_SQL']
# ROOT = os.environ['ROOT']
# HOST_DB_SQL = os.environ['HOST_DB_SQL']
# PORT = os.environ['PORT']


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f--g3ey-1mxjm&)po*vlg0%h+%u=zg4-$6r^4z&pca5pxn@cj%' # todo: put var to env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My apps
    'corsheaders',
    'Users.apps.UsersConfig',
    'rest_framework',
    'Posts.apps.PostsConfig',
    'PersonalInfo.apps.PersonalInfoConfig',
    'storages',
]


CORS_ORIGIN_ALLOW_ALL = True  # can reach from any host

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TelAviv.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'TelAviv.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# todo: put vars to env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway', 
        'USER': 'root', 
        'PASSWORD': 'e2qx7q9qBVnEWKDjPsAC',
        'HOST': 'containers-us-west-36.railway.app',
        'PORT': 7970,
        'OPTIONS': {
            'charset': 'utf8',  # Example character encoding setting
        },
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'rent-buzz-db', 
#         'USER': 'admin', 
#         'PASSWORD': 'Eran1302',
#         'HOST': 'runt-buzz-db.cwbbnuwtlmzz.us-east-1.rds.amazonaws.com',
#         'PORT': 3306,
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGER CONFIG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Set the desired log level
            'class': 'logging.FileHandler',
            'filename': 'debug.log',  # Set the log file name
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',  # Set the desired log level
            'propagate': True,
        },
    },
}

# S3 BUCKETS CONFIG

# credentials used to authenticate and authorize your application to interact with the AWS services.
AWS_ACCESS_KEY_ID = 'AKIATGTS4CJ6H77C7XO2'
AWS_SECRET_ACCESS_KEY = 'LhN05bF5khOATlmzAJSPxmKmc/drY4VggvEIBDB+'

# the name of the S3 bucket where you want to store your static and media files.
AWS_STORAGE_BUCKET_NAME = 'rent-buzz'

# specifies the version of the signature to use for requests to S3.
# 's3v4' indicates the AWS Signature Version 4.
AWS_S3_SIGNATURE_VERSION = 's3v4'

# sets the default access control for new objects in the S3 bucket.
# Setting it to None allows you to control the access through bucket policies or IAM roles.
AWS_DEFAULT_ACL = None

AWS_S3_REGION_NAME = 'eu-west-3'

# the custom domain to use for serving static and media files.
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# the base URL for static files served from S3.
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# defines the storage backend to use for static files.
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DEFAULT_FILE_STORAGE defines the storage backend to use for media files.
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# controls whether query parameters are included in URLs for S3 objects.
# Setting it to False removes query parameters from URLs, enhancing security.
AWS_QUERYSTRING_AUTH = False

# MEDIA_URL is the base URL for media files served from S3.
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
