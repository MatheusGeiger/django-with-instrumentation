import logging

import oneagent
import wrapt

from autodynatrace.sdk import sdk
from stomp import StompConnection11
from stomp import StompConnection12

_logger = logging.getLogger(__name__)


def turn_on_callback():
    def _diag_callback(unicode_message):
        print("CALLBACK DIAG", unicode_message)

    sdk.set_diagnostic_callback(_diag_callback)
    sdk.set_verbose_callback(_diag_callback)


def get_destination_type_by_name(destination: str) -> int:
    return (
        oneagent.common.MessagingDestinationType.TOPIC
        if "/topic/" in destination
        else oneagent.common.MessagingDestinationType.QUEUE
    )


def instrument_publisher():
    def on_send_message(wrapped, instance, args, kwargs):
        turn_on_callback()
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
            get_destination_type_by_name(destination),
            oneagent.sdk.Channel(oneagent.sdk.ChannelType.TCP_IP, "{}:{}".format(host, port)),
        )

        with messaging_system:
            with sdk.trace_outgoing_message(messaging_system) as outgoing_message:
                print("Agent state (parent process):", sdk.agent_state)
                print("Agent fork state (parent process):", sdk.agent_fork_state)
                print("Agent found:", sdk.agent_found)
                print("Agent is compatible:", sdk.agent_is_compatible)
                print("Agent version:", sdk.agent_version_string)
                trace_info = sdk.tracecontext_get_current()
                span_id, trace_id = trace_info.span_id, trace_info.trace_id
                _logger.info(f"autodynatrace - TRACE OUTGOING INFO span_id={span_id}, trace_id={trace_id}")

                outgoing_message.set_correlation_id(headers.get("correlation-id"))
                # outgoing_message.set_vendor_message_id(headers.get("message-id"))
                tag = outgoing_message.outgoing_dynatrace_string_tag.decode("utf-8")
                headers[oneagent.common.DYNATRACE_MESSAGE_PROPERTY_NAME] = tag
                headers["trace-id"] = trace_id
                headers["trace_id"] = trace_id
                headers["span-id"] = span_id
                headers["span_id"] = span_id
                _logger.info(
                    f"autodynatrace - Tracing Outgoing RabbitMQ host={host}, port={port}, routing_key={destination}, "
                    f"tag={tag}, headers={headers}"
                )
                return wrapped(*args, **kwargs)

    wrapt.wrap_function_wrapper(StompConnection11, "send", on_send_message)
    wrapt.wrap_function_wrapper(StompConnection12, "send", on_send_message)


def instrument_consumer():
    def wrapper_on_message(wrapped, instance, args, kwargs):
        turn_on_callback()
        host, port = instance.transport.current_host_and_port
        frame = args[0]
        headers, body = frame.headers, frame.body
        destination = headers.get("tshoot-destination")

        tag = None
        if headers is not None:
            tag = headers.get(oneagent.common.DYNATRACE_MESSAGE_PROPERTY_NAME, None)

        messaging_system = sdk.create_messaging_system_info(
            oneagent.common.MessagingVendor.RABBIT_MQ,
            destination,
            get_destination_type_by_name(destination),
            oneagent.sdk.Channel(oneagent.sdk.ChannelType.TCP_IP, "{}:{}".format(host, port)),
        )

        with messaging_system:
            with sdk.trace_incoming_message_receive(messaging_system):
                with sdk.trace_incoming_message_process(messaging_system, str_tag=tag) as process_message:
                    print("Agent state (parent process):", sdk.agent_state)
                    print("Agent fork state (parent process):", sdk.agent_fork_state)
                    print("Agent found:", sdk.agent_found)
                    print("Agent is compatible:", sdk.agent_is_compatible)
                    print("Agent version:", sdk.agent_version_string)
                    trace_info = sdk.tracecontext_get_current()
                    span_id, trace_id = trace_info.span_id, trace_info.trace_id
                    _logger.info(f"autodynatrace - TRACE INCOMING INFO span_id={span_id}, trace_id={trace_id}")

                    process_message.set_correlation_id(headers.get("correlation-id"))
                    process_message.set_vendor_message_id(headers.get("message-id"))

                    _logger.info(
                        f"autodynatrace - Tracing Incoming RabbitMQ host={host}, port={port},"
                        f" routing_key={destination}, tag={tag}, headers={headers}"
                    )
                    return wrapped(*args, **kwargs)

    wrapt.wrap_function_wrapper(StompConnection11, "on_message", wrapper_on_message)
    wrapt.wrap_function_wrapper(StompConnection12, "on_message", wrapper_on_message)


def instrument_log():
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        trace_info = sdk.tracecontext_get_current()
        span_id, trace_id = trace_info.span_id, trace_info.trace_id
        record.span_id = span_id
        record.trace_id = trace_id

        return record

    logging.setLogRecordFactory(record_factory)
