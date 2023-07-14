import logging

import oneagent

from autodynatrace.sdk import sdk
from django.utils.module_loading import import_string
from django_stomp import execution

from django_template.settings import STOMP_SERVER_HOST
from django_template.settings import STOMP_SERVER_PORT

_logger = logging.getLogger(__name__)


def instrument_consumer():
    def wrapped_import_string(dotted_path):
        callback_function = import_string(dotted_path)

        def instrumented_callable(payload):
            headers = payload.headers
            host, port = STOMP_SERVER_HOST, STOMP_SERVER_PORT
            destination = headers.get("tshoot-destination")

            tag = None
            if headers is not None:
                tag = headers.get(oneagent.common.DYNATRACE_MESSAGE_PROPERTY_NAME, None)

            messaging_system = sdk.create_messaging_system_info(
                oneagent.common.MessagingVendor.RABBIT_MQ,
                destination,
                oneagent.common.MessagingDestinationType.QUEUE,
                oneagent.sdk.Channel(oneagent.sdk.ChannelType.TCP_IP, "{}:{}".format(host, port)),
            )

            with messaging_system:
                with sdk.trace_incoming_message_receive(messaging_system):
                    with sdk.trace_incoming_message_process(messaging_system, str_tag=tag) as process_message:
                        process_message.set_correlation_id(headers.get("correlation-id"))
                        process_message.set_vendor_message_id(headers.get("message-id"))
                        _logger.info(
                            f"autodynatrace - Tracing Incoming RabbitMQ host={host}, port={port},"
                            f" routing_key={destination}, tag={tag}, headers={headers}"
                        )
                        return callback_function(payload)

        return instrumented_callable

    setattr(execution, "import_string", wrapped_import_string)
