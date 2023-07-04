import os

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

from django_template.opentelemetry.tracing import instrument_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_template.settings")

instrument_app()

if settings.USE_STATIC_FILE_HANDLER_FROM_WSGI:
    application = StaticFilesHandler(OpenTelemetryMiddleware(get_wsgi_application()))
else:
    application = OpenTelemetryMiddleware(get_wsgi_application())
