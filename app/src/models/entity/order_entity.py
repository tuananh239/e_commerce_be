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
    code: Optional[str]
    status: Optional[str]
    image_order: Optional[str]
    type_delivery: Optional[str]
    products: Optional[List[ProductEntity]]
    note_owner: Optional[str]
    note_staff: Optional[str]
    order_fee_percent: Optional[float]
    exchange_rate: Optional[float]
    stock_storage: Optional[str]
    user_storage: Optional[str]
    extra_fee: Optional[float]
    ship_cn_fee: Optional[float]
    tally_fee: Optional[float]
    item_total_cost: Optional[float]
    total_fee: Optional[float]
    total_paid: Optional[float]
    deposit_at: Optional[int]
    purchase_at: Optional[int]
    transit_at_vn: Optional[str]
    stock_at_vn: Optional[str]
    return_at: Optional[int]
    ship_at: Optional[int]
    weight_fee: Optional[float]
    volumn_fee: Optional[float]
    total_weight_fee: Optional[float]
    wood_package_fee: Optional[float]
    is_wood_package: Optional[bool]
    extra_ship_fee: Optional[float]
    weight: Optional[float]
    weight_base_volumn: Optional[float]
    weight_rate: Optional[float]

    id: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]