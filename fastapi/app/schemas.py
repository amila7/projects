from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool]

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode = True