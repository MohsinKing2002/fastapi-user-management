from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# user creation schema
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    phone_number: str = Field(min_length=10)


# user response schema
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone_number: str | None
    created_at: datetime
