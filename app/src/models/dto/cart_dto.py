import json
from typing import List, Optional
from pydantic import BaseModel

from app.src.models.dto.order_dto import ProductDTO


class CartUpdateDTO(BaseModel):
    products: Optional[List[ProductDTO]]


class CartDTO(BaseModel):
    products: Optional[List[ProductDTO]]

    id: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]