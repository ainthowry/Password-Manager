from uuid import UUID
from pydantic import BaseModel, Field


class Account(BaseModel):
    id: int
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)

    class Config:
        orm_mode = True


class RegisterInput(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
