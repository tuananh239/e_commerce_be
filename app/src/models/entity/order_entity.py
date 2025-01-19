from typing import Any, List, Optional
from pydantic import BaseModel

class ProductEntity(BaseModel):
    link_product: Optional[str]
    link_product_image: Optional[str]
    color: Optional[str]
    size: Optional[str]
    number: Optional[int]
    price: Optional[float]
    note: Optional[str]


class OrderEntity(BaseModel):
    products: Optional[List[ProductEntity]]
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