import os

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

from django_template.apps.dynatrace import instrument_consumer
from django_template.apps.dynatrace import instrument_log
from django_template.apps.dynatrace import instrument_publisher

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_template.settings")

instrument_publisher()
instrument_consumer()
instrument_log()

if settings.USE_STATIC_FILE_HANDLER_FROM_WSGI:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
