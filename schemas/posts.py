from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None

class PostResponse(PostBase):
    id: int
    user_id: int
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)

class PostList(BaseModel):
    posts: List[PostResponse]
    total: int
    page: int
    pages: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None