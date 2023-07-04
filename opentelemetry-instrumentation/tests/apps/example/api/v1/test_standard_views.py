import pytest

from django_template.apps.example.models import AuditAction
from tests.utils import is_valid_uuid


class TestUserView:
    def test_should_return_400_as_no_property_has_been_sent(self, client):
        # Arrange
        fake_data = {}
        # Act
        response = client.post("/api/v1/users/attributes", content_type="application/json", data=fake_data)
        # Assert
        result = response.json()
        assert response.status_code == 400
        request_id = result["error"]["requestId"]
        assert result == {
            "error": {
                "field_related_errors": {"non_field_errors": ["At least one property should be set!"]},
                "requestId": request_id,
            },
            "status_code": 400,
            "type": "VALIDATION_ERRORS",
        }

    @pytest.mark.django_db
    def test_should_return_200_with_new_full_name(self, client):
        # Arrange
        fake_data = {
            "full_name": "Jafar Iago",
            "user_metadata": {"birthday": "1985-06-23"},
        }
        # Act
        response = client.post("/api/v1/users/attributes", content_type="application/json", data=fake_data)
        # Assert
        assert response.status_code == 200
        assert AuditAction.objects.count() == 1
        created_audit_action: AuditAction = AuditAction.objects.first()
        assert is_valid_uuid(created_audit_action.id)
        assert created_audit_action.ip_address is None
        assert created_audit_action.action == "post"
        assert created_audit_action.success

    def test_should_return_200_with_user_attributes(self, client):
        # Act
        response = client.get("/api/v1/users/attributes", content_type="application/json")
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result == {
            "user_metadata": {"city": "santo andré", "state": "alagoas", "birthday": "23-06-1989", "gender": "male"},
            "full_name": "Carl Edward Sagan",
            "given_name": "Carl",
            "family_name": "Sagan",
        }
