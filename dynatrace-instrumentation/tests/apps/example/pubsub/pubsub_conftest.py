from typing import Dict
from typing import Optional
from unittest.mock import MagicMock

from django_stomp.services.consumer import Payload


def create_fake_payload(body: Dict, headers: Optional[Dict] = None) -> Payload:
    if not headers:
        headers = {}

    ack = MagicMock()
    nack = MagicMock()

    return Payload(body=body, headers=headers, ack=ack, nack=nack)
