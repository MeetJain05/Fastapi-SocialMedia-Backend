from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # class Config:
    #     orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1, description="Direction can only be 0 or 1")
