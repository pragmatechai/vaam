"""
Django settings for vaam_project project.
"""

import os
import logging
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-yweov*ywo#qv89u*%0$&fe-0o811h_li3%y06w@majyb90peo-'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

# Ensure a proper SECRET_KEY is set in production
if not DEBUG and SECRET_KEY.startswith('django-insecure'):
    raise ValueError("DJANGO_SECRET_KEY must be set to a secure value in production!")

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    '46.101.102.220,vaamglobal.com,www.vaamglobal.com'
).split(',')

CSRF_TRUSTED_ORIGINS = [
    'https://vaamglobal.com',
    'https://www.vaamglobal.com',
    'http://vaamglobal.com',
    'http://www.vaamglobal.com',
]

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'anymail',
    'core',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vaam_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'vaam_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '60')),
        'OPTIONS': {
            'connect_timeout': 10,
        } if os.environ.get('DB_ENGINE', '') == 'django.db.backends.postgresql' else {},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============ LANGUAGE / I18N ============
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Русский')),
    ('tr', _('Türkçe')),
    ('ar', _('العربية')),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru', 'tr', 'ar')

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Baku'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ============ STATIC / MEDIA ============
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============ CACHE ============
# Uses database cache in production so it works across multiple Gunicorn workers.
# Run: python manage.py createcachetable  (once on the server)
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': os.environ.get(
                'CACHE_BACKEND',
                'django.core.cache.backends.db.DatabaseCache'
            ),
            'LOCATION': os.environ.get('CACHE_LOCATION', 'django_cache'),
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
            },
        }
    }

# ============ EMAIL ============
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'anymail.backends.resend.EmailBackend'

ANYMAIL = {
    'RESEND_API_KEY': os.environ.get('RESEND_API_KEY', ''),
}

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'VAAM Global <info@vaamglobal.com>')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'info@vaamglobal.com')
EMAIL_SUBJECT_PREFIX = ''
CONTACT_NOTIFICATION_EMAIL = os.environ.get('CONTACT_NOTIFICATION_EMAIL', 'info@vaamglobal.com')

# MANAGERS receives mail_managers() notifications (contact form, inquiries)
_notify_email = os.environ.get('CONTACT_NOTIFICATION_EMAIL', 'info@vaamglobal.com')
MANAGERS = [('VAAM', _notify_email)]
ADMINS = MANAGERS

# ============ LOGGING ============
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# ============ LOGIN ============
LOGIN_URL = '/dashboard/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/dashboard/login/'

# ============ SECURITY ============
# Always set safe defaults
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

if not DEBUG:
    _ssl_enabled = os.environ.get('DJANGO_SSL_REDIRECT', 'False').lower() in ('true', '1', 'yes')
    # These MUST only be True when HTTPS is actually configured
    SESSION_COOKIE_SECURE = _ssl_enabled
    CSRF_COOKIE_SECURE = _ssl_enabled
    SECURE_HSTS_SECONDS = 31536000 if _ssl_enabled else 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = _ssl_enabled
    SECURE_HSTS_PRELOAD = _ssl_enabled
    SECURE_SSL_REDIRECT = _ssl_enabled
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
