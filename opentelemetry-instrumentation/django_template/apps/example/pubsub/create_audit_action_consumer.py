"""
Module that contains the consumer responsible to show one example of utilization.
"""
import logging

from django_stomp.services.consumer import Payload

from django_template.apps.example.api.v1.serializers import AuditActionSerializer
from django_template.apps.example.pubsub.pubsub_logic.create_audit_action import process

_logger = logging.getLogger(__name__)


def consumer(payload: Payload) -> None:
    """
    This consumer will create AuditAction data in database.

    The validations consist of:
        - Payload validation (using AuditActionSerializer)
        - Check if user exists in database from payload id

    Expected payload:
        body: {
            "user_id": "f124779c-2852-458c-949f-4d9d1866d1de",
            "action": "Example of action",
            "success": True,
            "ip_address": "192.168.1.1",
        }
        headers: {
            correlation_id: "f124779c-2852-458c-949f-4d9d1866d1de"
        }

    Message to DLQ when:
        - Invalid payload
        - UserAttributes does not exist from payload.body.user_id data value
    """
    payload_body, payload_headers = payload.body, payload.headers
    _logger.debug(
        "Received payload with body: %s and headers: %s",
        payload_body,
        payload_headers,
    )

    user_attribute_data_serializer = AuditActionSerializer(data=payload_body)
    user_attribute_data_serializer.is_valid(raise_exception=True)

    process(validated_payload_serializer=user_attribute_data_serializer)

    payload.ack()
    return
