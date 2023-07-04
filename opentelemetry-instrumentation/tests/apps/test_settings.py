import logging
import uuid

import requests

from django_template import settings


class TestMiddlewares:
    def test_liveness_is_properly_configured(self, live_server, django_assert_num_queries):
        # Arrange
        liveness_url_value = settings.LIVENESS_URL
        address = f"{live_server.url}{liveness_url_value}"
        # Act
        with django_assert_num_queries(0):
            response = requests.get(address)
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert body == {"message": "Ok"}
        middlewares = settings.MIDDLEWARE
        assert middlewares[0] == "django_template.support.middlewares.LivenessHealthCheckMiddleware"

    def test_request_id_is_properly_configured(self, live_server, django_assert_num_queries, mocker, caplog):
        # Arrange
        caplog.set_level(logging.DEBUG)
        request_id = uuid.uuid4()
        mock_request_id = mocker.patch("request_id_django_log.middleware.RequestIdDjangoLog._generate_id")
        mock_request_id.return_value = request_id
        # Act
        with django_assert_num_queries(0):
            requests.get(live_server.url)
        # Assert
        mock_request_id.assert_called_once()
        middlewares = settings.MIDDLEWARE
        assert middlewares[1] == "request_id_django_log.middleware.RequestIdDjangoLog"
        records = caplog.records
        number_of_records = len(records)
        assert number_of_records > 2
        found_none, found_request_id = False, False
        for index, record in enumerate(records):
            if index == 0 or record == records[-1]:
                found_none = record.request_id == "none"
            else:
                found_request_id = record.request_id == request_id
        assert found_none
        assert found_request_id
