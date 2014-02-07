from base import *

############################################################
##### STATIC FILES #########################################
############################################################

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'libs.storages.S3Storage.S3Storage'
STATIC_URL = 'http://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

############################################################
##### DATABASE #############################################
############################################################

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

############################################################
##### OTHER ################################################
############################################################

DEBUG = False
TEMPLATE_DEBUG = False