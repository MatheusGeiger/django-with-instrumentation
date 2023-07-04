import requests

from django.urls import reverse

from django_template.urls import urlpatterns


class TestRoutes:
    def test_named_urls(self):
        # Arrange
        number_of_urls = len(urlpatterns)
        validated_urls = 0
        # Act
        for url in urlpatterns:
            if hasattr(url, "url_patterns"):
                patterns = url.url_patterns
                first_pattern_available = patterns[0]
                if hasattr(first_pattern_available, "name"):
                    full_name = f"{url.namespace}:{first_pattern_available.name}"
                    urlpath = reverse(full_name)
                    assert urlpath
                    validated_urls += 1
        # Assert
        has_two_urls_configured = number_of_urls == 6
        assert has_two_urls_configured
        assert validated_urls == 2

    def test_django_live_server(self, live_server):
        # Arrange
        address = f"{live_server.url}/admin/"
        # Act
        response = requests.get(address)
        # Assert
        assert response.status_code == 200
