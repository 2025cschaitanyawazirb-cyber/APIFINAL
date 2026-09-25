from pydantic import BaseModel, Field


class AttachmentCreate(BaseModel):
    """What the client must send to attach a file reference to a request."""
    request_id: str
    file_name: str = Field(..., min_length=1)
    file_url: str = Field(..., min_length=1)
    file_size: int = Field(..., ge=0)


class AttachmentResponse(BaseModel):
    """What the server sends back."""
    id: str
    request_id: str
    file_name: str
    file_url: str
    file_size: int