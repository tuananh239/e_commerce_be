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
    note_staff: Optional[str]


class PackageDTO(BaseModel):
    id: Optional[Any]
    weight: Optional[float]
    weight_rate: Optional[float]
    total_weight_price: Optional[float]
    ship_at: Optional[Any]
    transit_at_vn: Optional[Any]
    stock_at_vn: Optional[Any]
    return_at: Optional[Any]
    weight_base_volumn: Optional[float]
    weight_base_volumn_rate: Optional[float]
    total_weight_volumn_price: Optional[float]
    status: Optional[Any]


class OrderGetDTO(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 0
    sort_by: Optional[str] = "_id"
    sort: Optional[str] = "asc"
    search: Optional[str] = ""
    status: Optional[str] = ""
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
    status: Optional[str]
    type_delivery: Optional[str]
    products: Optional[List[ProductDTO]]
    packages: Optional[List[PackageDTO]]
    note_owner: Optional[str]
    note_staff: Optional[str]
    order_fee_percent: Optional[float]
    exchange_rate: Optional[float]
    stock_storage: Optional[str]
    user_storage: Optional[str]
    extra_fee: Optional[float]
    ship_cn_fee: Optional[float]
    tally_fee: Optional[float]
    order_fee: Optional[float]
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

    custom_percent_paid: Optional[float]
    is_custom_percent_paid: Optional[bool]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        
        return value


class OrderDTO(BaseModel):
    code: Optional[str]
    status: Optional[str]
    image_order: Optional[str]
    type_delivery: Optional[str]
    products: Optional[List[ProductDTO]]
    packages: Optional[List[PackageDTO]]
    note_owner: Optional[str]
    note_staff: Optional[str]
    order_fee_percent: Optional[float]
    exchange_rate: Optional[float]
    stock_storage: Optional[str]
    user_storage: Optional[str]
    extra_fee: Optional[float]
    ship_cn_fee: Optional[float]
    tally_fee: Optional[float]
    order_fee: Optional[float]
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

    email: Optional[str]
    phone_number: Optional[str]

    custom_percent_paid: Optional[float]
    is_custom_percent_paid: Optional[bool]

    id: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]
    is_active: Optional[bool]