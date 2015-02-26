"""
Django settings for pdt project.

Generated by 'django-admin startproject' using Django 1.8a1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from YamJam import yamjam

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&4qvlp7z%qqka*-_3@zk733xenawadi@1+4%7=l%dg@0ma(sr8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_auth_fogbugz',
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'pdt.urls'

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

WSGI_APPLICATION = 'pdt.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTHENTICATION_BACKENDS = (
    'django_auth_fogbugz.backend.FogBugzBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_FOGBUGZ_SERVER = FOGBUGZ_URL = 'https://fogbugz.example.com'

AUTH_FOGBUGZ_AUTO_CREATE_USERS = True

AUTH_FOGBUGZ_ENABLE_PROFILE = True

AUTH_FOGBUGZ_ENABLE_PROFILE_TOKEN = True

SESSION_COOKIE_AGE = 1209600  # (2 weeks, in seconds)


try:
    from .settings_local import *
except ImportError:
    pass


cfg = yamjam('/etc/pdt/config.yaml;./config.yaml')

yam_config = cfg['pdt']

DJANGO_SECRET_KEY = yam_config['django_secret_key']

RAVEN_CONFIG = {
    'dsn': yam_config['raven']['dsn']
}

API_TOKEN = yam_config['api']['token']

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

dbcfg = yam_config['database']

DATABASES = {
    'default': {
        'ENGINE': dbcfg['engine'],
        'NAME': dbcfg['name'],
        'USER': dbcfg['user'],
        'PASSWORD': dbcfg['password'],
        'HOST': dbcfg['host'],
        'PORT': dbcfg['port'],
    }
}

# Token to use for fogbugz communication
FOGBUGZ_TOKEN = yam_config['fogbugz']['token']
