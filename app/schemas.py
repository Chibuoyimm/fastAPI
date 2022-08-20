from pydantic import BaseModel
from datetime import datetime



class PostBase(BaseModel):  # defining a schema of what to expect from the frontend and this automitcally does the validation
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
