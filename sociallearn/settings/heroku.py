from base import *
import os, os.path

############################################################
##### STATIC FILES #########################################
############################################################

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'libs.storages.S3Storage.S3Storage'
STATIC_URL = 'http://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

############################################################
##### DATABASE #############################################
############################################################

import dj_database_url
DATABASES['default'] =  dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

############################################################
##### OTHER ################################################
############################################################

DEBUG = False
TEMPLATE_DEBUG = False