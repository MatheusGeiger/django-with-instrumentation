from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django_template.apps.example.api.v1 import standard_views as standard_views_v1
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("healthcheck/readiness", include("health_check.urls"), name="health-check"),
    path("api/v1/users/attributes", standard_views_v1.UserManagementAttributesAPIView.as_view()),
    path("api/v1/ping/", standard_views_v1.InterServicesTestingView.as_view()),
    path("iapi/doc/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("iapi/doc/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("iapi/doc/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG and settings.USE_DEBUG_APPS:
    urlpatterns += [
        path("debug-callback/", include("django_stomp_debug_callback.urls")),  # django stomp callback urls
        path("debug-toolbar/", include("debug_toolbar.urls")),  # django debug toolbar
    ]
