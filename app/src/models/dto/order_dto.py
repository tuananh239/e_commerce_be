import json
from typing import Any, List, Optional
from pydantic import BaseModel

class ProductDTO(BaseModel):
    link_product: Optional[str]
    link_product_image: Optional[str]
    color: Optional[str]
    size: Optional[str]
    number: Optional[int]
    price: Optional[float]
    note: Optional[str]


class OrderGetDTO(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 0
    sort_by: Optional[str] = "_id"
    sort: Optional[str] = "asc"
    search: Optional[str] = ""
    time_from: Optional[int] = None
    time_to: Optional[int] = None


class OrderCreateDTO(BaseModel):
    products: Optional[List[ProductDTO]]
    type_delivery: Optional[str]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        
        return value
    

class OrderUpdateDTO(BaseModel):
    products: Optional[List[ProductDTO]]
    type_delivery: Optional[str]
    status: Optional[str]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        
        return value


class OrderDTO(BaseModel):
    products: Optional[List[ProductDTO]]
    type_delivery: Optional[str]
    image_order: Optional[str]
    status: Optional[str]
    code: Optional[str]

    id: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]