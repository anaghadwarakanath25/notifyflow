from dataclasses import dataclass, field
from enum import StrEnum


class Channel(StrEnum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    IN_APP = "in_app"


@dataclass(frozen=True)
class Notification:
    id: int
    tenant_id: int
    channel: Channel
    recipient: str
    tags: list[str] = field(default_factory=list)

