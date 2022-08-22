from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class PostBase(BaseModel):  # defining a schema of what to expect from the frontend and this automitcally does the validation
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass


class Post(PostBase): # response schema for posts
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel): # response schema for the user
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None