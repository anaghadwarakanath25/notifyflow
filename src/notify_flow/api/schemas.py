from pydantic import BaseModel, Field

from notify_flow.domain.notification import Channel


class SendNotificationRequest(BaseModel):
    channel: Channel
    recipient: str = Field(min_length=3)
    template_id: int