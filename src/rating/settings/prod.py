from decouple import config
from dj_database_url import parse as parse_db_connection_string

from .base import *  # NOQA

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda val: [x.strip() for x in val.split(',')], default='*')

DATABASES = {
    'default': parse_db_connection_string(config('DATABASE_URI'))
}
