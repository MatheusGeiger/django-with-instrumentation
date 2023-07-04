import json
import uuid

import pytest

from rest_framework.exceptions import ValidationError

from django_template.apps.example.models import AuditAction
from django_template.apps.example.models import UserAttributes
from django_template.apps.example.pubsub.create_audit_action_consumer import consumer
from tests.apps.example.pubsub.pubsub_conftest import create_fake_payload
from tests.utils import create_user_attributes


class TestCreateAuditActionConsumer:
    def test_should_raise_validation_error_when_payload_is_invalid(self):
        # arrange
        fake_payload_with_invalid_body = create_fake_payload({"test": "invalid"})

        # act
        with pytest.raises(ValidationError) as e:
            consumer(fake_payload_with_invalid_body)

        # assert
        expected_validation_error = {
            "user_id": ["This field is required."],
            "action": ["This field is required."],
            "success": ["This field is required."],
        }
        assert json.loads(json.dumps(e.value.detail)) == expected_validation_error

    def test_should_raise_user_attributes_does_not_exists(self, db):
        # arrange
        fake_payload_with_invalid_user_id = create_fake_payload(
            body={
                "user_id": str(uuid.uuid4()),
                "action": "Example of action",
                "success": True,
                "ip_address": "192.168.1.1",
            }
        )
        # act
        with pytest.raises(UserAttributes.DoesNotExist):
            consumer(fake_payload_with_invalid_user_id)

        # assert
        assert len(AuditAction.objects.all()) == 0

    def test_should_ack_and_save_audit_log_when_payload_is_valid(self, db):
        # arrange
        user_attributes = create_user_attributes()
        fake_payload = create_fake_payload(
            body={
                "user_id": str(user_attributes.id),
                "action": "Example of action",
                "success": True,
                "ip_address": "192.168.1.1",
            }
        )

        # act
        consumer(fake_payload)

        # assert
        audict_action_created = AuditAction.objects.first()
        assert fake_payload.ack.call_count == 1
        assert audict_action_created.user_id == fake_payload.body["user_id"]
        assert audict_action_created.action == fake_payload.body["action"]
        assert audict_action_created.success == fake_payload.body["success"]
        assert audict_action_created.ip_address == fake_payload.body["ip_address"]
