import uuid

from typing import Optional

from django.db import models
from django.db.models import JSONField


class StandardModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class AuditAction(StandardModelMixin):
    user_id = models.CharField(max_length=128, null=False, blank=False)
    action = models.CharField(max_length=128, null=False, blank=False)
    success = models.BooleanField(null=False, blank=False)
    # Later we can identify where the anonymous user is using the following:
    # https://docs.djangoproject.com/en/3.2/ref/contrib/gis/geoip2/
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f"{self.user_id} / {self.action} / {self.ip_address} / {self.created_at.date()}"


class UserAttributes(StandardModelMixin):
    """
    A class to represent a UserAttributes entity
    """

    full_name = models.CharField(max_length=70, null=True, blank=True, verbose_name="User Full Name")
    given_name = models.CharField(max_length=35, null=True, blank=True, verbose_name="Given Name")
    family_name = models.CharField(max_length=35, null=True, blank=True, verbose_name="Family Name")
    user_metadata = JSONField(null=True, default=dict, verbose_name="User data")

    def _get_user_metadata_by_key(self, key) -> Optional[str]:
        return self.user_metadata.get(key)

    @property
    def birthday(self) -> Optional[str]:
        return self._get_user_metadata_by_key("birthday")

    @property
    def city(self) -> Optional[str]:
        return self._get_user_metadata_by_key("city")

    @property
    def state(self) -> Optional[str]:
        return self._get_user_metadata_by_key("state")

    @property
    def gender(self) -> Optional[str]:
        return self._get_user_metadata_by_key("gender")
