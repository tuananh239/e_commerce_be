# =================================================================================================================
# Feature: cart_repository
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo.collation import Collation

from app.libs.exception.exceptions import RepositoryException

from app.libs.fastapi.request import Filtering, Pagination, Sorting
from app.libs.pattern.creational.singleton import Singleton
from app.libs.pymongo.base_repository import BaseRepository
from app.src.commons.constants.constants import MONGODB_CONST
from app.src.models.entity.cart_entity import CartEntity

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

class Syntax():
    OR = "$or"
    AND = "$and"
    SET = "$set"
    COND = "$cond"
    IF = "if"
    GT = "$gt"
    SIZE = "$size"
    THEN = "then"
    IN = "$in"
    ELSE = "else"
    MATCH = "$match"
    LOOKUP = "$lookup"
    ADD_FIELDS = "$addFields"
    SORT = "$sort"
    LIMIT = "$limit"
    SKIP = "$skip"
    FROM = "from"
    LOCAL_FIELD = "localField"
    FOREIGN_FIELD = "foreignField"
    AS = "as"
    NOT_EQUAL = "$ne"
    NOT_IN = "$nin"
    PIPELINE = "pipeline"

# Main class ======================================================================================================

class CartRepository(BaseRepository, metaclass=Singleton):
    """
        Class này triển khai các phương thức phục vụ cho việc truy vấn dữ liệu trong bảng cart
    """
    def __init__(self) -> None:
        self.__client = self._get_client(MONGODB_CONST.CONNECTION.SERVER)
        self.__connection = self.__client.get_database("e_commerce")
        self.__collection = self.__connection.cart


    def create(self, cart_data: CartEntity):
        _response = self.__collection.insert_one(jsonable_encoder(cart_data))

        if not _response.inserted_id:
            raise RepositoryException(message="Repository error - Insert document to DB fail!")
        
        _response = self.__collection.find_one({"_id": _response.inserted_id})

        _response = CartEntity(**{**_response, "id": str(_response["_id"])})

        return _response
    

    def get(self, user):
        _response = self.__collection.find_one({'created_by': user, "is_active": True})

        if _response:
            return CartEntity(**{**_response, "id": str(_response["_id"])})
        else:
            return None


    def get_detail(self, cart_id: str):
        _response = self.__collection.find_one({'_id': ObjectId(cart_id), "is_active": True})

        if _response:
            return CartEntity(**{**_response, "id": str(_response["_id"])})
        else:
            return None
        
    
    def update(self, cart_id: str, cart_data: CartEntity):
        self.__collection.update_one(
            {
                "_id": ObjectId(cart_id)
            },
            {
                Syntax.SET: jsonable_encoder(cart_data, exclude_none=True)
            }
        )

        return cart_data
    

    def remove(self, cart_id: str):
        self.__collection.update_one(
            {
                "_id": ObjectId(cart_id)
            },
            {
                Syntax.SET: {
                    "is_active": False
                }
            }
        )

        return True