import json
from typing import Any, List, Optional
from pydantic import BaseModel


class ConfigGetDTO(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 0
    sort_by: Optional[str] = "_id"
    sort: Optional[str] = "asc"
    search: Optional[str] = ""
    time_from: Optional[int] = None
    time_to: Optional[int] = None

class OptionDTO(BaseModel):
    min: Optional[int]
    max: Optional[int]
    value: Optional[float]


class ConfigCreateDTO(BaseModel):
    purchase_fee: Optional[List[OptionDTO]]
    exchange_rate: Optional[float]
    weight: Optional[List[OptionDTO]]


class ConfigUpdateDTO(BaseModel):
    purchase_fee: Optional[List[OptionDTO]]
    exchange_rate: Optional[float]
    weight: Optional[List[OptionDTO]]


class ConfigDTO(BaseModel):
    id: Optional[str]
    purchase_fee: Optional[List[OptionDTO]]
    exchange_rate: Optional[float]
    weight: Optional[List[OptionDTO]]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]