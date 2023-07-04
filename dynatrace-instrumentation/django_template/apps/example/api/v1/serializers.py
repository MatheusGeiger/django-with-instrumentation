from rest_framework import serializers

from django_template.apps.example.models import AuditAction


# ERROR HANDLER SERIALIZER
class ErrorDetailsSerializer(serializers.Serializer):
    field_related_errors = serializers.JSONField(required=False)
    msg = serializers.CharField(required=False)
    requestId = serializers.UUIDField()


class GlobalErrorSerializer(serializers.Serializer):
    error = ErrorDetailsSerializer()
    status_code = serializers.IntegerField()
    type = serializers.CharField()


# APPLICATION SERIALIZER
class UserMetadataSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=35, required=False)
    state = serializers.CharField(max_length=2, required=False)
    birthday = serializers.DateField(required=False)
    gender = serializers.CharField(max_length=35, required=False)


class UserAttributesSerializer(serializers.Serializer):
    user_metadata = UserMetadataSerializer(required=False)
    full_name = serializers.CharField(max_length=70, required=False)
    given_name = serializers.CharField(max_length=35, required=False)
    family_name = serializers.CharField(max_length=35, required=False)

    def validate(self, data: dict):
        is_any_property_available = any(value for key, value in data.items() if value)
        if not is_any_property_available:
            raise serializers.ValidationError("At least one property should be set!")
        return data


class AuditActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditAction
        fields = "__all__"
