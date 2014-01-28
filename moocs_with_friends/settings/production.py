from base import *

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'moocs_with_friends',
        'USER': 'moocs_with_friends',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False
TIME_ZONE = 'America/New_York'