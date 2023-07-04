from datetime import date

from django_template.apps.example.api.v1.serializers import UserAttributesSerializer


class TestUserAttributesSerializer:
    def test_should_return_error_given_no_field_has_been_configured(self):
        # Arrange
        fake_data = {}
        # Act
        serializer = UserAttributesSerializer(data=fake_data)
        # Assert
        assert not serializer.is_valid()
        assert len(serializer.errors) == 1
        assert serializer.errors["non_field_errors"][0] == "At least one property should be set!"

    def test_should_return_error_as_date_is_not_iso_8601(self):
        # Arrange
        fake_data = {
            "user_metadata": {"birthday": "23-06-1989"},
        }
        # Act
        serializer = UserAttributesSerializer(data=fake_data)
        # Assert
        assert not serializer.is_valid()
        assert len(serializer.errors) == 1
        assert (
            str(serializer.errors["user_metadata"]["birthday"][0])
            == "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
        )

    def test_should_convert_birthday_to_date_object(self):
        # Arrange
        fake_data = {
            "full_name": "Jafar",
            "user_metadata": {"birthday": "1989-06-23"},
        }
        # Act
        serializer = UserAttributesSerializer(data=fake_data)
        # Assert
        assert serializer.is_valid()
        assert serializer.validated_data["full_name"] == fake_data["full_name"]
        assert serializer.validated_data["user_metadata"]["birthday"] == date(1989, 6, 23)
