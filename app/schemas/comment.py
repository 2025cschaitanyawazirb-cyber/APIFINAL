from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    """What the client must send to add a comment to a request."""
    request_id: str
    author_id: str
    message: str = Field(..., min_length=1)


class CommentResponse(BaseModel):
    """What the server sends back."""
    id: str
    request_id: str
    author_id: str
    message: str