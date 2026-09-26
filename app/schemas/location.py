from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    """What the client must send to create a new location."""
    building: str = Field(..., min_length=1)
    floor: str = Field(..., min_length=1)
    room: str = Field(default="")


class LocationResponse(BaseModel):
    """What the server sends back."""
    id: str
    building: str
    floor: str
    room: str