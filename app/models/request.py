from app.schemas.request import RequestStatus

# ---------------------------------------------------------------------------
# The complete map of which status can move to which other status.
# Every attempt to change a request's status is checked against this map
# before anything is saved. An illegal jump (e.g. New -> Resolved) is
# rejected with a clear error explaining why.
# ---------------------------------------------------------------------------

ALLOWED_STATUS_TRANSITIONS = {
    RequestStatus.new: [RequestStatus.assigned],
    RequestStatus.assigned: [RequestStatus.in_progress],
    RequestStatus.in_progress: [RequestStatus.on_hold, RequestStatus.resolved],
    RequestStatus.on_hold: [RequestStatus.in_progress],
    RequestStatus.resolved: [RequestStatus.closed],
    RequestStatus.closed: [],  # terminal state — no further transitions allowed
}


def is_transition_allowed(current_status: RequestStatus, new_status: RequestStatus) -> bool:
    """
    Checks whether moving from current_status to new_status is a legal move.
    """
    return new_status in ALLOWED_STATUS_TRANSITIONS.get(current_status, [])