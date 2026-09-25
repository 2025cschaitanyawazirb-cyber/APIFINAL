from datetime import datetime
from pymongo.collection import Collection


def create_audit_log_entry(
    audit_logs_collection: Collection,
    request_id: str,
    performed_by: str,
    action: str,
    details: str = "",
) -> None:
    """
    Shared helper that writes one audit log entry. Called from inside
    request-related actions (create, assign, status change) as a side
    effect — never called directly by a user-facing endpoint.
    """
    audit_logs_collection.insert_one({
        "request_id": request_id,
        "performed_by": performed_by,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow(),
    })