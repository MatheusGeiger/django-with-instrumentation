import logging

from typing import TypedDict

from request_id_django_log.request_id import current_request_id
from rest_framework import exceptions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import exception_handler as default_global_exception_handler

from django_template.apps.example.api.v1.serializers import GlobalErrorSerializer
from django_template.support.inter_utils import retrieve_first_item_otherwise_itself

_logger = logging.getLogger(__name__)


class Context(TypedDict):
    view: APIView
    args: tuple
    kwargs: dict
    request: Request


def exception_handler(thrown_exception: Exception, context: Context):
    _logger.exception("Exception has been caught inside global handler")

    response = default_global_exception_handler(thrown_exception, context)
    request_id = current_request_id()

    if response is not None:
        headers = response.headers
        error_type, status_code, error = None, response.status_code, None

        if isinstance(thrown_exception, exceptions.APIException):
            status_code = thrown_exception.status_code
        if isinstance(thrown_exception, exceptions.ValidationError):
            error_type = "VALIDATION_ERRORS"
            error = {"field_related_errors": thrown_exception.detail}
        else:
            error_detail: exceptions.ErrorDetail = response.data["detail"]
            error_type = retrieve_first_item_otherwise_itself(error_detail.code).replace(" ", "_").upper()
            error = {"msg": str(error_detail)}

        error["requestId"] = request_id
        serializer = GlobalErrorSerializer(
            {
                "error": error,
                "status_code": status_code,
                "type": error_type,
            }
        )

        return Response(serializer.data, status=response.status_code, headers=headers)

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    serializer = GlobalErrorSerializer(
        instance={
            "error": {
                "requestId": request_id,
                "msg": (
                    f'Oh, sorry! We didn\'t expect that 😬 Please inform the ID "{request_id}" so we can help you properly.'  # noqa: E501
                ),
            },
            "status_code": status_code,
            "type": "UNEXPECTED_ERROR",
        }
    )

    return Response(serializer.data, status=status_code)
