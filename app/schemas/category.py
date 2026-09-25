from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """What the client must send to create a new category."""
    name: str = Field(..., min_length=1)
    description: str = Field(default="")


class CategoryResponse(BaseModel):
    """What the server sends back."""
    id: str
    name: str
    description: str