from .base import *


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(', ')

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

REST_FRAMEWORK.update(
    {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 20,
    }
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR'
        }
    }
}
