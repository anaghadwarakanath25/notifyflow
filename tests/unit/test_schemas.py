import pytest
from pydantic import ValidationError

from notify_flow.api.schemas import SendNotificationRequest


def test_valid_request() -> None:
    req = SendNotificationRequest.model_validate(
        {"channel": "email", "recipient": "a@x.com", "template_id": 1}
    )
    assert req.template_id == 1


def test_string_id_is_converted() -> None:
    req = SendNotificationRequest.model_validate(
        {"channel": "email", "recipient": "a@x.com", "template_id": "7"}
    )
    assert req.template_id == 7


def test_bad_channel_rejected() -> None:
    with pytest.raises(ValidationError):
        SendNotificationRequest.model_validate(
            {"channel": "pigeon", "recipient": "a@x.com", "template_id": 1}
        )
