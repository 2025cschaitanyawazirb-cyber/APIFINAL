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
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    category_id: str
    location_id: str
    priority: RequestPriority = RequestPriority.medium
    created_by: str


class RequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    location_id: Optional[str] = None
    priority: Optional[RequestPriority] = None


class RequestStatusUpdate(BaseModel):
    status: RequestStatus


class RequestAssign(BaseModel):
    assigned_to: str


class RequestResponse(BaseModel):
    id: str
    title: str
    description: str
    category_id: str
    location_id: str
    priority: RequestPriority
    status: RequestStatus
    created_by: str
    assigned_to: Optional[str] = None