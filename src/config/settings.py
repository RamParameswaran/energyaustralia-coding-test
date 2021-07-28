"""
Django settings for energyaustralia-coding-test project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging
from logging.handlers import SysLogHandler

SYSLOG_ADDRESS = (
    os.environ.get("SYSLOG_HOST", "localhost"),
    int(os.environ.get("SYSLOG_PORT", 514)),
)


# Add a special logger to log related occurrences in settings
formatter = logging.Formatter("SETTINGS %(levelname)-8s %(message)s")
settings_logger = logging.getLogger("settings")

if not os.environ.get("CONSOLE_LOGS"):
    handler = SysLogHandler(address=SYSLOG_ADDRESS)
    handler.setFormatter(formatter)
    settings_logger.addHandler(handler)

# Log settings also in stdout
handler = logging.StreamHandler()
handler.setFormatter(formatter)
settings_logger.addHandler(handler)

settings_logger.setLevel(logging.INFO)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG_MODE", False))
if DEBUG:
    settings_logger.critical("STARTING SERVER IN DEBUG MODE")

ALLOWED_HOSTS = []
allowed_hosts = os.environ.get("ALLOWED_HOSTS", [])
if allowed_hosts:
    ALLOWED_HOSTS = allowed_hosts.split(",")
settings_logger.info("ALLOWED_HOSTS: {}".format(ALLOWED_HOSTS))


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "tweet",
]

MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/opt/static/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id": {"()": "log_request_id.filters.RequestIDFilter"}},
    "formatters": {
        "standard": {
            "format": "energyaustralia-coding-test: %(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        # Only send to syslog info or higher
        "syslog": {
            "level": "INFO",
            "class": "logging.handlers.SysLogHandler",
            "address": SYSLOG_ADDRESS,
            "filters": ["request_id"],
            "formatter": "standard",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["request_id"],
            "formatter": "standard",
        },
    },
    "loggers": {
        # Top level for the application. Remember to set on
        # all loggers
        "": {
            "handlers": ["syslog"],
            "level": "DEBUG",
            "propagate": False,
        },
        # For usage on runserver (dev-server)
        "django.server": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

if os.environ.get("CONSOLE_LOGS"):
    # Log all to the console as well. This is used while running unit tests
    del LOGGING["handlers"]["syslog"]
    LOGGING["loggers"][""]["handlers"] = ["console"]


LOG_REQUESTS = True
# Origin request will be X-REQUEST-ID
LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = "X-REQUEST-ID"
