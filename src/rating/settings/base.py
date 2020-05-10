import os
from decouple import config

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

MEDIA_DIR = os.path.join(BASE_DIR, 'img')
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/img/'

NODE_MODULES = os.path.join(os.path.dirname(BASE_DIR), 'node_modules')

SECRET_KEY = 'yj@v(ey2p)i8k!fk-smheuen8p-any&o9hlv4_3u1s3tma3$a!'

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'admin_site',

    'nested_admin',
    'admin_actions',
    'django_admin_listfilter_dropdown',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'compressor',
    'debug_toolbar',

    'core',
    'api',
    'user_site'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware'
]

ROOT_URLCONF = 'rating.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        },
    },
]

WSGI_APPLICATION = 'rating.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

USE_I18N = False

USE_L10N = True

USE_TZ = True

TIME_ZONE = config('TIME_ZONE', default='UTC')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

DEFAULT_PER_PAGE = 20

CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r'^/api/.*$'

CORS_EXPOSE_HEADERS = []

CORS_ALLOW_CREDENTIALS = True

COMPRESS_OFFLINE = True

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', f'{os.path.join(NODE_MODULES, ".bin", "node-sass")} {{infile}} > {{outfile}}'),
    ('text/es6', f'{os.path.join(NODE_MODULES, ".bin", "babel")} --presets @babel/preset-env {{infile}} > {{outfile}}')
)

COMPRESS_CSS_HASHING_METHOD = 'content'

COMPRESS_FILTERS = {
    'css': (
        'django_compressor_autoprefixer.AutoprefixerFilter',
        'compressor.filters.css_default.CssRelativeFilter',
        'compressor.filters.yuglify.YUglifyCSSFilter'
    ),
    'js': (
        'compressor.filters.yuglify.YUglifyJSFilter',
    )
}

COMPRESS_YUGLIFY_BINARY = os.path.join(NODE_MODULES, '.bin', 'yuglify')

COMPRESS_AUTOPREFIXER_BINARY = os.path.join(NODE_MODULES, '.bin', 'postcss')

INTERNAL_IPS = [
    '127.0.0.1'
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 100
}

ADMIN_APP_LIST = (
    'auth',
    {
        'app': 'core',
        'models': (
            'University',
            'Faculty',
            'Department',
            'Person',
            'PersonType',
            'Article',
            'Revision',
            'ScopusSnapshot',
            'GoogleScholarSnapshot',
            'SemanticScholarSnapshot',
            'WosSnapshot'
        )
    },
    'user_site'
)
