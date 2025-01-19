import json
from typing import Any, List, Optional
from pydantic import BaseModel

class UserGetDTO(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 0
    sort_by: Optional[str] = "_id"
    sort: Optional[str] = "asc"
    search: Optional[str] = ""
    time_from: Optional[int] = None
    time_to: Optional[int] = None


class UserCreateDTO(BaseModel):
    username: str
    password: str


class UserUpdateDTO(BaseModel):
    password: str


class UserDTO(BaseModel):
    id: Optional[str]
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]