from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    employee = "employee"
    facility_technician = "facility_technician"
    facility_manager = "facility_manager"
    admin = "admin"


class UserCreate(BaseModel):
    """What the client must send to create a new user."""
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole


class UserResponse(BaseModel):
    """What the server sends back — note: no password."""
    id: str
    name: str
    email: EmailStr
    role: UserRole