from typing import Optional
from uuid import UUID

from django_template.apps.example.models import UserAttributes


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    if isinstance(uuid_to_test, UUID):
        return True
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def create_user_attributes(
    full_name: Optional[str] = "Fake Given Family Name",
    given_name: Optional[str] = "Given Name",
    family_name: Optional[str] = "Family Name",
    user_metadata: Optional[dict] = None,
) -> UserAttributes:
    user_metadata = user_metadata if user_metadata else {"fake": "data"}
    user_attribute_data = {
        "full_name": full_name,
        "given_name": given_name,
        "family_name": family_name,
        "user_metadata": user_metadata,
    }
    return UserAttributes.objects.create(**user_attribute_data)
