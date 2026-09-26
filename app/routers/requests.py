from fastapi import APIRouter, Depends, HTTPException, status, Query
from bson import ObjectId
from typing import Optional

from app.dependencies import get_requests_collection, get_audit_logs_collection
from app.schemas.request import (
    RequestCreate,
    RequestUpdate,
    RequestStatusUpdate,
    RequestAssign,
    RequestResponse,
    RequestStatus,
)
from app.models.request import is_transition_allowed
from app.models.audit_log import create_audit_log_entry

router = APIRouter(prefix="/requests", tags=["Requests"])


def request_doc_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc["description"],
        "category_id": doc["category_id"],
        "location_id": doc["location_id"],
        "priority": doc["priority"],
        "status": doc["status"],}