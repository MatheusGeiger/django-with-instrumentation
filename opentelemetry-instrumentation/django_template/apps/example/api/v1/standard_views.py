import logging

from uuid import uuid4

from django_stomp.builder import build_publisher
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from request_id_django_log.request_id import current_request_id
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_template.apps.example.api.openapi import standard_responses
from django_template.apps.example.api.v1.serializers import UserAttributesSerializer
from django_template.apps.example.models import AuditAction
from django_template.settings import CREATE_AUDIT_ACTION_DESTINATION
from django_template.apps.pika.publisher import publish_to_pika

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
        
        headers = {
            "correlation-id": current_request_id()
        }
        # testing publish message to broker using pika
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
