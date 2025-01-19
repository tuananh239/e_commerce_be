from typing import Any, List, Optional
from pydantic import BaseModel

class UserEntity(BaseModel):
    id: Optional[str]
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]