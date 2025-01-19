from typing import Any, List, Optional
from pydantic import BaseModel

class UserEntity(BaseModel):
    id: Optional[str]

    email: Optional[str]
    password: Optional[str]
    name: Optional[str]
    phone_number: Optional[str]
    storage: Optional[str]
    province: Optional[str]
    district: Optional[str]
    address_detail: Optional[str]

    role: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]