from pydantic import BaseModel


class DirectusPayload(BaseModel):
    collection: str = ""
    event: str = ""
    payload: dict = {}


class WebhookResponse(BaseModel):
    status: str
    collection: str
    keys_cleared: int
