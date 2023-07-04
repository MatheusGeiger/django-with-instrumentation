"""
Auxiliary module to generate the documentation of standard responses of the application.

Status Code: Response model

    400: {
        "error": {
            "field_related_errors": {
                "user_metadata": {
                    "state": [
                        "Ensure this field has no more than 2 characters."
                    ],
                    "birthday": [
                        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                    ]
                }
            },
            "requestId": "a6965089-217f-4bce-ba20-0c337450ab1c"
        },
        "status_code": 400,
        "type": "VALIDATION_ERRORS"
    }

    401: {
        "error": {
            "requestId": "b9ce34b8-f3c6-4806-94fc-c5957e1949eb",
            "msg": "Authentication credentials were not provided."
        },
        "status_code": 401,
        "type": "NOT_AUTHENTICATED"
    }

    403: {
        "error": {
            "msg": "You do not have permission to perform this action.",
            "requestId": "2c65a36a-9875-4d60-91e7-a2c9f1c22496"
        },
        "status_code": 403,
        "type": "PERMISSION_DENIED"
    }

    500: {
        "error": {
            "requestId": request_id,
            "msg": (
                f'Oh, sorry! We didn\'t expect that 😬 Please inform the ID "{request_id}" so we can help you properly.'
            ),
        },
        "status_code": status_code,
        "type": "UNEXPECTED_ERROR",
    }

TODO:
    * MOVE THIS MODULE TO LIBRARY
"""
import uuid

from typing import Dict

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status


def create_inline_serializer_with_custom_config(
    default_value_for_status_code: int, default_value_for_type: str, include_field_related_errors: bool = False
) -> Dict:
    """Auxiliary function to create drf_spectacular schemas/serializer based in parameters.

    The drf spectacular use the serializers to include our structure in schema openapi definition and
    this behavior disturb the response in swagger-ui when use "common" serializer.
    This function will create multiples schemas/serializer with particularity and optimize the swagger-ui view.

    The function returns one object with base structure changing the status_code, type and error_field_related_errors
    fields.

    Args:
      default_value_for_status_code(int): status_code to use in response from request.
      default_value_for_type(str): error type to use in response from request.
      include_field_related_errors(bool): boolean to included include_field_related_errors additional parameter
      (used in error 400 - Validation errors)

    Returns:
      dict: Dict with standard response

    Example of return:
        {
            "error": {
                "field_related_errors": { <-- Optional parameter included from include_field_related_errors parameter
                    "user_metadata": {
                        "state": [
                            "Ensure this field has no more than 2 characters."
                        ],
                        "birthday": [
                            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                        ]
                    }
                },
                "requestId": "a6965089-217f-4bce-ba20-0c337450ab1c"
            },
            "status_code": 400, <-- Value of default_value_for_status_code parameter
            "type": "VALIDATION_ERRORS"  <-- Value of default_value_for_type parameter
        }
    """
    common_error_detail_fields = {"requestId": uuid.uuid4(), "msg": "string"}

    if include_field_related_errors:
        common_error_detail_fields.update(
            {
                "field_related_errors": {
                    "field_name_1": ["errors"],
                    "field_name_2": ["errors"],
                }
            }
        )

    return {
        "error": serializers.JSONField(default=common_error_detail_fields),
        "status_code": serializers.IntegerField(default=default_value_for_status_code),
        "type": serializers.CharField(default=default_value_for_type),
    }


standard_responses = {
    status.HTTP_400_BAD_REQUEST: inline_serializer(
        name="ValidationErrorSerializer",
        fields=create_inline_serializer_with_custom_config(
            default_value_for_status_code=status.HTTP_400_BAD_REQUEST,
            default_value_for_type="VALIDATION_ERRORS",
            include_field_related_errors=True,
        ),
    ),
    status.HTTP_401_UNAUTHORIZED: inline_serializer(
        name="NotAuthenticatedErrorSerializer",
        fields=create_inline_serializer_with_custom_config(
            default_value_for_status_code=status.HTTP_401_UNAUTHORIZED,
            default_value_for_type="NOT_AUTHENTICATED",
        ),
    ),
    status.HTTP_403_FORBIDDEN: inline_serializer(
        name="PermissionDeniedErrorSerializer",
        fields=create_inline_serializer_with_custom_config(
            default_value_for_status_code=status.HTTP_403_FORBIDDEN,
            default_value_for_type="PERMISSION_DENIED",
        ),
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR: inline_serializer(
        name="UnexpectedErrorSerializer",
        fields=create_inline_serializer_with_custom_config(
            default_value_for_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            default_value_for_type="UNEXPECTED_ERROR",
        ),
    ),
}
