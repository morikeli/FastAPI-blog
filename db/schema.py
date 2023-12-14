from typing import List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str
    

class Blog(BlogBase):
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class UserDetails(BaseModel):
    name: str
    email: str
    blog: List[Blog] = []

    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    author: UserDetails

    class Config:
        orm_mode = True