import uuid

import pytest

from django_template.apps.example.models import UserAttributes
from django_template.apps.example.pubsub.pubsub_logic.create_audit_action import get_user_attributes_by_id
from tests.utils import create_user_attributes


class TestCreateAuditActionPubsubLogic:
    def test_get_user_attributes_by_id_should_raise_user_attributes_does_not_exists(self, db):
        # arrange
        user_id_non_existent_in_database = str(uuid.uuid4())

        # assert
        with pytest.raises(UserAttributes.DoesNotExist):
            # act
            get_user_attributes_by_id(user_id_non_existent_in_database)

    def test_should_return_user_by_id_in_get_user_attributes_by_id(self, db):
        # arrange
        user_attributes = create_user_attributes()
        user_id_existent_in_database = str(user_attributes.id)

        # act
        user_attributes_from_database = get_user_attributes_by_id(user_id_existent_in_database)

        # assert
        assert user_attributes_from_database.id == user_attributes.id
