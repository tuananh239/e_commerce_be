from typing import Any, List, Optional
from pydantic import BaseModel


class OptionEntity(BaseModel):
    min: Optional[int]
    max: Optional[int]
    value: Optional[float]


class ConfigEntity(BaseModel):
    purchase_fee: Optional[List[OptionEntity]]
    exchange_rate: Optional[float]
    weight: Optional[List[OptionEntity]]

    id: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]