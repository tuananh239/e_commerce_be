from typing import List, Optional
from pydantic import BaseModel

from app.src.models.entity.order_entity import ProductEntity

class CartEntity(BaseModel):
    id: Optional[str]

    products: Optional[List[ProductEntity]]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]