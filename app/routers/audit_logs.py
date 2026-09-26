from fastapi import APIRouter, Depends

from app.dependencies import get_audit_logs_collection
from app.schemas.audit_log import AuditLogResponse

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


def audit_log_doc_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "request_id": doc["request_id"],
        "performed_by": doc["performed_by"],
        "action": doc["action"],
        "details": doc["details"],
        "timestamp": doc["timestamp"],
    }


@router.get("", response_model=list[AuditLogResponse])
def list_audit_logs_for_request(request_id: str, audit_logs_collection=Depends(get_audit_logs_collection)):
    logs = list(audit_logs_collection.find({"request_id": request_id}))
    return [audit_log_doc_to_response(l) for l in logs]