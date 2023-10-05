from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CORS and access to the API
ALLOWED_HOSTS = ['localhost','127.0.0.1']

# Conection to the database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '5194',
        'NAME':'gymForceData',
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'