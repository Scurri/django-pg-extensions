# -*- coding: utf-8 -*-

# Discover tests in all cases
import os.path
TEST_DISCOVER_TOP_LEVEL = os.path.dirname(os.path.dirname(__file__))
TEST_DISCOVER_ROOT = os.path.join(TEST_DISCOVER_TOP_LEVEL, 'tests')

DATABASES = {
    'default': {
        'ENGINE': 'djangopg.postgresql_psycopg2',
        'NAME': 'test_db',
        'USER': 'dbuser',
        'PASSWORD': 'dbpass',
        'HOST': 'djangopg_db',
        'PORT': 5432
    }
}
SECRET_KEY = 'very_secret_key_nobody_know_about_it'

INSTALLED_APPS = (
    'tests.resource_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

DEBUG = True
