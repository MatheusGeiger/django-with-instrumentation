import os
from distutils.util import strtobool
from logging import Formatter
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

from django_template.support.django_helpers import eval_env_as_boolean
from pythonjsonlogger.jsonlogger import JsonFormatter

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DJANGO_DEBUG", "False"))

DJANGO_ALLOWED_HOSTS: Optional[str] = os.getenv("ALLOWED_HOSTS")
if DJANGO_ALLOWED_HOSTS:
    EXTRA_ALLOWED_HOST: Optional[str] = os.getenv("EXTRA_ALLOWED_HOST")
    FINAL_ALLOWED_HOSTS = f"{DJANGO_ALLOWED_HOSTS},{EXTRA_ALLOWED_HOST}" if EXTRA_ALLOWED_HOST else DJANGO_ALLOWED_HOSTS
    ALLOWED_HOSTS = FINAL_ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS: Union[List[str], str]
if CSRF_TRUSTED_ORIGINS := os.getenv("CSRF_TRUSTED_ORIGINS", ""):
    CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS.split(",")

CSRF_COOKIE_SECURE = strtobool(os.getenv("CSRF_COOKIE_SECURE", "True"))
SESSION_COOKIE_SECURE = strtobool(os.getenv("SESSION_COOKIE_SECURE", "True"))

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "request_id_django_log",
    "health_check",
    "health_check.db",
    "drf_spectacular",
    "django_stomp",
    "django_outbox_pattern",
    "autodynatrace.wrappers.django",
]

LOCAL_APPS: List[str] = [
    "django_template.apps.example",
    "django_template.apps.pika",
    "django_template.apps.dynatrace"
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django_template.support.middlewares.LivenessHealthCheckMiddleware",
    "request_id_django_log.middleware.RequestIdDjangoLog",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_template.urls"

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

WSGI_APPLICATION = "django_template.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "drf_link_navigation_pagination.LinkNavigationPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 20)),
    "EXCEPTION_HANDLER": "django_template.apps.example.api.global_exception_handler.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (),
}

# https://drf-spectacular.readthedocs.io/en/latest/settings.html

SPECTACULAR_SETTINGS = {
    "TITLE": "Django Template API - Description",
    "DESCRIPTION": "Description for project here.",
    "VERSION": "1.0.0",
    "TAGS": [
        {
            "name": "tag1",
            "description": "Application requests",
        },
        {
            "name": "tag2",
            "description": "Operations available to regular users through browser",
        },
    ],
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASE_SSL_MODE = os.getenv("DB_SSL_MODE")

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

DATABASES["default"]["CONN_MAX_AGE"] = int(os.getenv("DB_CONN_MAX_AGE", 0))  # type: ignore

if DATABASE_SSL_MODE:
    DATABASES["default"]["OPTIONS"].update({"sslmode": DATABASE_SSL_MODE})  # type: ignore

if strtobool(os.getenv("USE_REPLICA", "False")):
    DATABASES["replica"] = {
        "ENGINE": os.getenv("DB_ENGINE_REPLICA"),
        "NAME": os.getenv("DB_DATABASE_REPLICA"),
        "USER": os.getenv("DB_USER_REPLICA"),
        "HOST": os.getenv("DB_HOST_REPLICA"),
        "PORT": os.getenv("DB_PORT_REPLICA"),
        "PASSWORD": os.getenv("DB_PASSWORD_REPLICA"),
    }

    DATABASES["replica"]["CONN_MAX_AGE"] = int(os.getenv("DB_CONN_MAX_AGE", 0))  # type: ignore

    DATABASE_ROUTERS: List[str] = []  # Place your database router path here

    if DATABASE_SSL_MODE:
        DATABASES["replica"]["OPTIONS"].update({"sslmode": DATABASE_SSL_MODE})  # type: ignore

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Logging
# https://docs.djangoproject.com/en/4.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "request_id_django_log.filters.RequestIDFilter"},
        "redact_filter": {
            "()": "django_template.support.logger.RedactingFilter",
            "patterns": ["cpf", "email", "birthday", "gender", "number", "emails", "username", "name", "phone"],
        },
    },
    "formatters": {
        "standard": {
            "()": JsonFormatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s",
        },
        "development": {
            "()": Formatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_id", "redact_filter"],
            "formatter": os.getenv("DEFAULT_LOG_FORMATTER", "standard"),
        }
    },
    "loggers": {
        "": {"level": os.getenv("ROOT_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django_template": {
            "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {"level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django.db.backends": {"level": os.getenv("DJANGO_DB_BACKENDS_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django.request": {"level": os.getenv("DJANGO_REQUEST_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "stomp.py": {"level": os.getenv("STOMP_LOG_LEVEL", "WARNING"), "handlers": ["console"], "propagate": False},
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
USE_STATIC_FILE_HANDLER_FROM_WSGI = strtobool(os.getenv("USE_STATIC_FILE_HANDLER_FROM_WSGI", "true"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://github.com/juntossomosmais/request-id-django-log

REQUEST_ID_CONFIG = {
    "REQUEST_ID_HEADER": "HTTP_X_REQUEST_ID",
    "GENERATE_REQUEST_ID_IF_NOT_FOUND": True,
    "RESPONSE_HEADER_REQUEST_ID": "HTTP_X_REQUEST_ID",
}

###############################
# Custom settings

# Liveness URL
LIVENESS_URL = os.getenv("LIVENESS_URL", "/healthcheck/liveness")

# DEBUG CONFIGURATION
USE_DEBUG_APPS = eval_env_as_boolean("USE_DEBUG_APPS", False)
if DEBUG and USE_DEBUG_APPS:
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": (lambda request: True)}
    INTERNAL_IPS = ["0.0.0.0"]

    DEBUG_APPS = os.getenv("DEBUG_APPS")
    if DEBUG_APPS:
        INSTALLED_APPS += DEBUG_APPS.split(",")

    DEBUG_MIDDLEWARE = os.getenv("DEBUG_MIDDLEWARE")
    if DEBUG_MIDDLEWARE:
        MIDDLEWARE += DEBUG_MIDDLEWARE.split(",")

# STOMP
STOMP_LISTENER_CLIENT_ID = os.getenv("STOMP_LISTENER_CLIENT_ID")
STOMP_SERVER_HOST = os.getenv("STOMP_SERVER_HOST")
STOMP_SERVER_PORT = os.getenv("STOMP_SERVER_PORT")
STOMP_SERVER_PORT_PIKA = os.getenv("STOMP_SERVER_PORT_PIKA")
STOMP_SERVER_STANDBY_HOST = os.getenv("STOMP_SERVER_STANDBY_HOST")
STOMP_SERVER_STANDBY_PORT = os.getenv("STOMP_SERVER_STANDBY_PORT")
STOMP_SERVER_USER = os.getenv("STOMP_SERVER_USER")
STOMP_SERVER_PASSWORD = os.getenv("STOMP_SERVER_PASSWORD")
STOMP_USE_SSL = eval_env_as_boolean("STOMP_USE_SSL", True)
STOMP_SERVER_VHOST = os.getenv("STOMP_SERVER_VHOST")
STOMP_OUTGOING_HEARTBEAT = os.getenv("STOMP_OUTGOING_HEARTBEAT", 15000)
STOMP_INCOMING_HEARTBEAT = os.getenv("STOMP_INCOMING_HEARTBEAT", 15000)
STOMP_PROCESS_MSG_ON_BACKGROUND = os.getenv("STOMP_PROCESS_MSG_ON_BACKGROUND", True)

# OUTBOX
DJANGO_OUTBOX_PATTERN = {
    "DEFAULT_STOMP_HOST_AND_PORTS": [(STOMP_SERVER_HOST, STOMP_SERVER_PORT)],
    "DEFAULT_STOMP_USERNAME": STOMP_SERVER_USER,
    "DEFAULT_STOMP_PASSCODE": STOMP_SERVER_PASSWORD,
    "DEFAULT_STOMP_USE_SSL": STOMP_USE_SSL,
    "DEFAULT_STOMP_VHOST": STOMP_SERVER_VHOST,
}

# Broker
CREATE_AUDIT_ACTION_DESTINATION = os.getenv("CREATE_AUDIT_ACTION_DESTINATION", "/queue/create-audit-action")
CREATE_AUDIT_ACTION_DESTINATION_2 = os.getenv("CREATE_AUDIT_ACTION_DESTINATION_2", "create-audit-action-2")

ENDPOINT_TO_PING_USER_ID = os.getenv("ENDPOINT_TO_PING_USER_ID", "http://localhost:8000/api/v1/ping/")
