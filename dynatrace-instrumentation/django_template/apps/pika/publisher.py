import json

import pika

from django.core.serializers.json import DjangoJSONEncoder

from django_template.apps.pika import connection
from django_template.settings import CREATE_AUDIT_ACTION_DESTINATION_2

channel = connection.channel()


def publish_to_pika(headers, body):
    properties = pika.BasicProperties(headers=headers, correlation_id=headers.get("correlation_id"))
    channel.basic_publish(
        exchange="",
        routing_key=CREATE_AUDIT_ACTION_DESTINATION_2,
        body=json.dumps(body, cls=DjangoJSONEncoder),
        properties=properties,
    )
