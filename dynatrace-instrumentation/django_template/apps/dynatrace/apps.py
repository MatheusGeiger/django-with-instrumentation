from django.apps import AppConfig

from django_template.apps.dynatrace.consumer import instrument_consumer
from django_template.apps.dynatrace.log import instrument_log
from django_template.apps.dynatrace.publisher import instrument_publisher


class DjangoStompAutoDynatrace(AppConfig):
    name = "django_template.apps.dynatrace"

    def ready(self):
        instrument_consumer()
        instrument_publisher()
        instrument_log()
