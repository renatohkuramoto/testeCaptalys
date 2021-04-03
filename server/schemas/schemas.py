from pydantic import BaseModel, Field
from typing import Optional


class UserSchema(BaseModel):
    user_id: int = Field(...)
    username: str = Field(...)
    repositories: str = Field(...)
    
    class Config:
        orm_mode = True


class RepositoriesSchema(BaseModel):
    repo_id: int = Field(...)
    url: str = Field(...)
    name: str = Field(...)
    access_type: str = Field(...)
    created_at: str = Field(...)
    updated_at: str = Field(...)
    size: int = Field(...)
    stargazers_count: int = Field(...)
    watchers_count: int = Field(...)
    
    class Config:
        orm_mode = True

  
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }
