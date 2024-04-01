import os
from distutils.util import strtobool

from django.apps import AppConfig

from django_template.apps.dynatrace.consumer import instrument_consumer
from django_template.apps.dynatrace.log import instrument_log
from django_template.apps.dynatrace.publisher import instrument_publisher


class DjangoStompAutoDynatrace(AppConfig):
    name = "django_template.apps.dynatrace"

    def ready(self):
        import oneagent
        sdk_options = oneagent.sdkopts_from_commandline(remove=True)
        is_forkable_enabled = bool(strtobool(os.getenv("AUTODYNATRACE_FORKABLE", "True")))
        oneagent.initialize(sdk_options, forkable=is_forkable_enabled)
        instrument_consumer()
        instrument_publisher()
        instrument_log()
