"""
Django settings for isalive project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import sys


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / 'apps'

PUBLIC_ROOT = BASE_DIR / 'media'
FETCHER_DIR = BASE_DIR / 'background_service/fetcher'
NOTIFIER_DIR = BASE_DIR / 'background_service/notifier'

sys.path.insert(0, str(APPS_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '40#ap-=*!mdg74pog+zv%@w2hyuuotz#4%==i!m24e&h^$9(^2')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

API_HOST = 'localhost:8000'
SITE_HOST = 'localhost:8000'
LOGIN_PAGE = SITE_HOST + '/login/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "push_notifications",
    'account.apps.AccountConfig',
    'authorization.apps.AuthorizationConfig',
    'utils.apps.UtilsConfig',
    'monitor.apps.MonitorConfig',
    'device.apps.DeviceConfig',
    'configs.apps.ConfigsConfig',
    'notification.apps.NotificationConfig',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'channels',
    'solo',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'project.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOSTNAME'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = PUBLIC_ROOT / 'static'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

AUTH_USER_MODEL = 'account.User'

CONFIRMATION_EMAIL_EXPIRATION = 24

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
REST_DATE_FORMAT = '%m-%d-%Y'
REST_DATETIME_FORMAT = '%m-%d-%Y %H:%M:%S'

CORS_ALLOW_ALL_ORIGINS = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


PUSH_NOTIFICATIONS_SETTINGS = {
        "FCM_API_KEY": 'AAAAU26WSJw:APA91bE5VYuX4_3Psa3xhOo8lrYgTVTYci77ozKs_7ajNExfViUbPHRWsVCd8tq4s8xd73odb3TYC4ph4bpCYRykN3D1ffAh1syRHZV2_LMK_wKip4007kWMf8AUe7cUoknFK95d2Yt0',
        "UPDATE_ON_DUPLICATE_REG_ID": True
}

# Telegram
CONFIRMATION_TELEGRAM_EXPIRATION = 12 # hours
TELEGRAM_BOT_NAME = 'IsaliveProjectNotificationsBot'
TELEGRAM_BOT_TOKEN = '1799516847:AAF2zRucTQOUiBg_aNu5ZqxdxfovBIBlZEY'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
            '%(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },

        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'backupCount': 12,
            'maxBytes': 16 * 1000000,
            'filename': os.path.join(BASE_DIR / 'logs/app.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    'django.request': {
        'handlers': ['log_file'],
        'level': 'INFO',
        'propagate': False,
    },
    },
}

