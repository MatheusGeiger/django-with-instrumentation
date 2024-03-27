import logging
import uuid

from uuid import uuid4

import requests
from django.conf import settings
from django.utils import timezone
from django_outbox_pattern.factories import factory_producer
from django_stomp.builder import build_publisher
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_template.apps.example.api.openapi import standard_responses
from django_template.apps.example.api.v1.serializers import UserAttributesSerializer
from django_template.apps.example.models import AuditAction
from django_template.apps.pika.publisher import publish_to_pika
from django_template.settings import CREATE_AUDIT_ACTION_DESTINATION

_logger = logging.getLogger(__name__)


@extend_schema_view(get=extend_schema(tags=["tag1", "tag2"]), post=extend_schema(tags=["tag1"]))
class UserManagementAttributesAPIView(APIView):
    """
    View with responsibility to manipulate UserAttributes data.
    """

    @extend_schema(
        responses={200: UserAttributesSerializer} | standard_responses,
    )
    def post(self, request):
        user_id = uuid4()
        _logger.debug("The following user is trying to refresh his attributes: %s", user_id)
        serializer = UserAttributesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # testing logging trace
        _logger.info("What I received: %s", serializer.validated_data)

        # testing db trace
        AuditAction(user_id=user_id, action=UserManagementAttributesAPIView.post.__name__, success=True).save()

        # testing publish message to broker
        publisher = build_publisher(f"django-template-standard-view-{uuid4()}")
        publisher.send(
            queue=CREATE_AUDIT_ACTION_DESTINATION,
            body={
                "user_id": user_id,
                "action": UserManagementAttributesAPIView.post.__name__,
                "success": True,
                "ip_address": "192.168.1.1",
            },
        )

        with factory_producer() as producer:
            _id = str(uuid.uuid4())
            name = CREATE_AUDIT_ACTION_DESTINATION.split("/")[-1]
            headers = {
                "correlation-id": _id,
                "cap-msg-id": _id,
                "cap-msg-name": name,
                "cap-senttime": timezone.now(),
                "cap-corr-id": _id,
                "cap-corr-seq": 0,
            }
            producer.send_event(
                destination=CREATE_AUDIT_ACTION_DESTINATION,
                body={
                    "user_id": user_id,
                    "action": UserManagementAttributesAPIView.post.__name__,
                    "success": True,
                    "ip_address": "192.168.1.1",
                },
                headers=headers,
            )

        publish_to_pika(
            headers,
            {
                "user_id": user_id,
                "action": UserManagementAttributesAPIView.post.__name__,
                "success": True,
                "ip_address": "192.168.1.1",
            },
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: UserAttributesSerializer} | standard_responses,
    )
    def get(self, request):
        user_id = "Salted User has been logged"
        _logger.debug("The following user is trying to retrieve his attributes: %s", user_id)
        serializer = UserAttributesSerializer(
            {
                "full_name": "Carl Edward Sagan",
                "given_name": "Carl",
                "family_name": "Sagan",
                "user_metadata": {
                    "city": "santo andré",
                    "state": "alagoas",
                    "birthday": "23-06-1989",
                    "gender": "male",
                },
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class InterServicesTestingView(APIView):
    @extend_schema(
        responses={200: UserAttributesSerializer} | standard_responses,
    )
    def get(self, request):
        user_id = uuid4()
        _logger.info("Received request to ping an user id: %s", user_id)


        requests.post(url=settings.ENDPOINT_TO_PING_USER_ID, json={"user_id": str(user_id)})

        # testing db trace
        AuditAction(user_id=user_id, action=InterServicesTestingView.get.__name__, success=True).save()

        # testing publish message to broker
        publisher = build_publisher(f"django-template-standard-view-{uuid4()}")
        publisher.send(
            queue=CREATE_AUDIT_ACTION_DESTINATION,
            body={
                "user_id": user_id,
                "action": InterServicesTestingView.get.__name__,
                "success": True,
                "ip_address": "192.168.1.1",
            },
        )

        with factory_producer() as producer:
            _id = str(uuid.uuid4())
            name = CREATE_AUDIT_ACTION_DESTINATION.split("/")[-1]
            headers = {
                "correlation-id": _id,
                "cap-msg-id": _id,
                "cap-msg-name": name,
                "cap-senttime": timezone.now(),
                "cap-corr-id": _id,
                "cap-corr-seq": 0,
            }
            producer.send_event(
                destination=CREATE_AUDIT_ACTION_DESTINATION,
                body={
                    "user_id": user_id,
                    "action": InterServicesTestingView.get.__name__,
                    "success": True,
                    "ip_address": "192.168.1.1",
                },
                headers=headers,
            )

        return Response({"response": "OK"}, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: UserAttributesSerializer} | standard_responses,
    )
    def post(self, request):
        request_data = request.data
        _logger.info("Received request_data: %s", request_data)
        user_id = request_data

        # testing db trace
        AuditAction(user_id=user_id, action=InterServicesTestingView.post.__name__, success=True).save()

        # testing publish message to broker
        publisher = build_publisher(f"django-template-standard-view-{uuid4()}")
        publisher.send(
            queue=CREATE_AUDIT_ACTION_DESTINATION,
            body={
                "user_id": user_id,
                "action": InterServicesTestingView.post.__name__,
                "success": True,
                "ip_address": "192.168.1.1",
            },
        )

        with factory_producer() as producer:
            _id = str(uuid.uuid4())
            name = CREATE_AUDIT_ACTION_DESTINATION.split("/")[-1]
            headers = {
                "correlation-id": _id,
                "cap-msg-id": _id,
                "cap-msg-name": name,
                "cap-senttime": timezone.now(),
                "cap-corr-id": _id,
                "cap-corr-seq": 0,
            }
            producer.send_event(
                destination=CREATE_AUDIT_ACTION_DESTINATION,
                body={
                    "user_id": user_id,
                    "action": InterServicesTestingView.post.__name__,
                    "success": True,
                    "ip_address": "192.168.1.1",
                },
                headers=headers,
            )

        return Response({}, status=status.HTTP_200_OK)
