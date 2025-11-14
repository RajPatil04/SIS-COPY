import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-a-secure-secret'
DEBUG = True
ALLOWED_HOSTS = ['*']  # Allow all hosts in development

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'students',
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
]

ROOT_URLCONF = 'sis_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Project templates first
            os.path.join(BASE_DIR, '..', 'sis_frontend_detailed - Copy')  # Frontend templates second
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sis_backend.wsgi.application'

# Database configuration - use environment variables so the project can be
# re-linked to any database by setting environment values.
#
# To link to a new DB, set these environment variables before running Django:
#   DB_ENGINE (e.g. 'django.db.backends.mysql' or 'django.db.backends.postgresql' or 'django.db.backends.sqlite3')
#   DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

_DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
if 'sqlite' in _DB_ENGINE:
    default_name = os.getenv('DB_NAME', str(BASE_DIR / 'db.sqlite3'))
else:
    default_name = os.getenv('DB_NAME', 'sis_db')

DATABASES = {
    'default': {
        'ENGINE': _DB_ENGINE,
        'NAME': default_name,
        'USER': os.getenv('DB_USER', 'sis_user') if 'sqlite' not in _DB_ENGINE else os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', 'sis_password') if 'sqlite' not in _DB_ENGINE else os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1') if 'sqlite' not in _DB_ENGINE else os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', '3306') if 'sqlite' not in _DB_ENGINE else os.getenv('DB_PORT', ''),
    }
}

if 'mysql' in _DB_ENGINE:
    DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}

# CORS configuration for frontend-backend communication
CORS_ALLOW_ALL_ORIGINS = True  # For development only; restrict in production
CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Point static files to the existing frontend assets folder
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'sis_frontend_detailed - Copy', 'assets'),
]

# Media files (for uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Redirect after login
LOGIN_REDIRECT_URL = '/students/profile/'
LOGIN_URL = '/students/login/'
