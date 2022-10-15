from uuid import UUID
from pydantic import BaseModel, Field

class Account(BaseModel):
    id: UUID
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)