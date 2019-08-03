import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

NODE_MODULES = os.path.join(os.path.dirname(BASE_DIR), 'node_modules')

SECRET_KEY = 'yj@v(ey2p)i8k!fk-smheuen8p-any&o9hlv4_3u1s3tma3$a!'

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'nested_admin',
    'corsheaders',
    'rest_framework',
    'pipeline',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'api',
    'user_site'
]

MIDDLEWARE = [
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.FileSystemFinder'
)

DEFAULT_PER_PAGE = 20

CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r'^/api/.*$'

CORS_EXPOSE_HEADERS = []

CORS_ALLOW_CREDENTIALS = True

PIPELINE = {
    'JAVASCRIPT': {
        'vendor': {
            'source_filenames': (
                'user_site/vendor/jquery-3.4.1.min.js',
                'user_site/vendor/DataTables-1.10.18/js/jquery.dataTables.min.js',
                'user_site/vendor/Scroller-2.0.0/js/dataTables.scroller.min.js',
            ),
            'output_filename': 'user_site/js/vendor.min.js'
        },

        'application': {
            'source_filenames': (
                'user_site/js/common.es6',
                'user_site/js/person-rating.es6'
            ),
            'output_filename': 'user_site/application.min.js'
        }
    },

    'STYLESHEETS': {
        'application': {
            'source_filenames': (
                'user_site/scss/application.scss',
            ),
            'output_filename': 'user_site/application.min.css',
            'extra_context': {
                'media': 'all'
            },
        }
    },

    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.YuglifyCompressor',
    'YUGLIFY_BINARY': os.path.join(NODE_MODULES, '.bin', 'yuglify'),

    'COMPILERS': (
        'pipeline.compilers.sass.SASSCompiler',
        'pipeline.compilers.es6.ES6Compiler'
    ),

    'SASS_BINARY': os.path.join(NODE_MODULES, '.bin', 'node-sass'),
    'BABEL_BINARY': os.path.join(NODE_MODULES, '.bin', 'babel'),
    'BABEL_ARGUMENTS': '--presets @babel/preset-env'
}

HTML_MINIFY = True
