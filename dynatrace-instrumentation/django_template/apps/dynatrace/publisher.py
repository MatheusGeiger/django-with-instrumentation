import logging

import oneagent
import wrapt

from autodynatrace.sdk import sdk
from stomp import StompConnection11
from stomp import StompConnection12

_logger = logging.getLogger(__name__)


def instrument_publisher():
    def on_send_message(wrapped, instance, args, kwargs):
        try:
            host, port = instance.transport.current_host_and_port
            destination = kwargs.get("destination")
            headers = kwargs.get("headers", {})

        except Exception as e:
            _logger.warn("autodynatrace - Could not trace Publisher.send: {}".format(e))
            return wrapped(*args, **kwargs)

        messaging_system = sdk.create_messaging_system_info(
            oneagent.common.MessagingVendor.RABBIT_MQ,
            destination,
            oneagent.common.MessagingDestinationType.QUEUE,
            oneagent.sdk.Channel(oneagent.sdk.ChannelType.TCP_IP, "{}:{}".format(host, port)),
        )

        with messaging_system:
            with sdk.trace_outgoing_message(messaging_system) as outgoing_message:
                outgoing_message.set_correlation_id(headers.get("correlation-id"))
                tag = outgoing_message.outgoing_dynatrace_string_tag.decode("utf-8")
                headers[oneagent.common.DYNATRACE_MESSAGE_PROPERTY_NAME] = tag
                _logger.info(
                    f"autodynatrace - Tracing Outgoing RabbitMQ host={host}, port={port}, routing_key={destination}, "
                    f"tag={tag}, headers={headers}"
                )
                return wrapped(*args, **kwargs)

    wrapt.wrap_function_wrapper(StompConnection11, "send", on_send_message)
    wrapt.wrap_function_wrapper(StompConnection12, "send", on_send_message)
