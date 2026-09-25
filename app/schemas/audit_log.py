from pydantic import BaseModel
from datetime import datetime


class AuditLogResponse(BaseModel):
    """What the server sends back. Note: no 'Create' model — these are
    only ever generated automatically as a side effect of other actions,
    never created directly by a user."""
    id: str
    request_id: str
    performed_by: str
    action: str
    details: str
    timestamp: datetime