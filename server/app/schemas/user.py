from pydantic import BaseModel
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: str

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass