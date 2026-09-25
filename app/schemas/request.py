from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class RequestStatus(str, Enum):
    new = "new"
    assigned = "assigned"
    in_progress = "in_progress"
    on_hold = "on_hold"
    resolved = "resolved"
    closed = "closed"


class RequestPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class RequestCreate(BaseModel):
    """What the client must send to create a new facility request."""
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    category_id: str
    location: str = Field(..., min_length=1)
    priority: RequestPriority = RequestPriority.medium
    created_by: str  # user id of the employee reporting the issue


class RequestUpdate(BaseModel):
    """What the client can send to update an existing request's details."""
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    location: Optional[str] = None
    priority: Optional[RequestPriority] = None


class RequestStatusUpdate(BaseModel):
    """Dedicated model for changing just the status (separate from general edits)."""
    status: RequestStatus


class RequestAssign(BaseModel):
    """Dedicated model for assigning a technician to a request."""
    assigned_to: str  # user id of the facility technician


class RequestResponse(BaseModel):
    """What the server sends back."""
    id: str
    title: str
    description: str
    category_id: str
    location: str
    priority: RequestPriority
    status: RequestStatus
    created_by: str
    assigned_to: Optional[str] = None