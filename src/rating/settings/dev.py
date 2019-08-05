from dj_database_url import parse as parse_db_connection_string
from decouple import config

from .base import *  # NOQA

DEBUG = True

DATABASES = {
    'default': parse_db_connection_string(
        config('DATABASE_URI', default='postgres://rating:rating@localhost:5432/rating_dev')
    )
}

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    },
}
