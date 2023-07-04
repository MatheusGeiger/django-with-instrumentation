from django.contrib import admin

from django_template.apps.example.models import AuditAction
from django_template.support.django_helpers import CustomModelAdminMixin


@admin.register(AuditAction)
class AuditActionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    search_fields = ["user_id"]
