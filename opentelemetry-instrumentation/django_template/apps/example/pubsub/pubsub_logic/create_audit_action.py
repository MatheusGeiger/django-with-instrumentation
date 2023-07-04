"""
Module that contains the logic about user attributes update.
"""
import logging
import uuid

from typing import Union

from django_stomp.builder import build_publisher

from django_template.apps.example.api.v1.serializers import AuditActionSerializer
from django_template.apps.example.models import UserAttributes

_logger = logging.getLogger(__name__)


def get_user_attributes_by_id(user_id: Union[str, uuid.UUID]) -> UserAttributes:
    try:
        return UserAttributes.objects.get(id=user_id)
    except UserAttributes.DoesNotExist as e:
        _logger.warning("User with id %s does not exists", user_id)
        raise e


def process(validated_payload_serializer: AuditActionSerializer):
    """
    This function process the AuditAction data save on database.

    Raises:
        UserAttributes.DoesNotExist: if validated_payload_serializer.validated_data["user_id"] not found
        in UserAttributes
    """
    user_id = validated_payload_serializer.validated_data["user_id"]

    publisher = build_publisher(f"django-template-standard-view-{uuid.uuid4()}")
    publisher.send(queue="/queue/test-do-test", body={"any": "value"})

    _logger.debug("Finding user with id %s", user_id)
    get_user_attributes_by_id(user_id)

    _logger.debug("Saving AuditAction %s", validated_payload_serializer.validated_data)
    validated_payload_serializer.save()
