# =================================================================================================================
# Feature: decision_repository
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
from app.src.models.entity.decision_entity import DecisionEntity

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

class DecisionRepository(BaseRepository, metaclass=Singleton):
    """
        Class này triển khai các phương thức phục vụ cho việc truy vấn dữ liệu trong bảng decision
    """
    def __init__(self) -> None:
        self.__client = self._get_client(MONGODB_CONST.CONNECTION.SERVER)
        self.__connection = self.__client.get_database("decision_manager")
        self.__collection = self.__connection.decision


    def create(self, decision_data: DecisionEntity):
        _response = self.__collection.insert_one(jsonable_encoder(decision_data))

        if not _response.inserted_id:
            raise RepositoryException(message="Repository error - Insert document to DB fail!")
        
        _response = self.__collection.find_one({"_id": _response.inserted_id})

        _response = DecisionEntity(**{**_response, "id": str(_response["_id"])})

        return _response
    

    def get(self, sort=Sorting(), filter=Filtering(), pagination=Pagination(), search: str=""):
        _condition = {
            "is_active": True,
            **(filter.approximate_search())
        }

        if filter.time_from:
            if filter.time_to:
                _condition.update({
                    "created_time": {
                        "$gt": filter.time_from,
                        "$lt": filter.time_to
                    }
                })
            else:
                _condition.update({
                    "created_time": {
                        "$gt": filter.time_from
                    }
                })
        else:
            if filter.time_to:
                _condition.update({
                    "created_time": {
                        "$lt": filter.time_to
                    }
                })

        _response = list(self.__collection.find(_condition).sort(
            [(sort.sort_by, sort.sort)]
        ).collation(
            Collation(locale="vi", caseLevel=True)
        ).skip(pagination.skip).limit(pagination.size))

        if _response:
            _response = [DecisionEntity(**{**decision, "id": str(decision["_id"])}) for decision in _response]

        return _response
    

    def count_document(self, filter=Filtering(), search: str=""):
        _condition = {
            "is_active": True,
            **(filter.approximate_search())
        }

        if filter.time_from:
            if filter.time_to:
                _condition.update({
                    "created_time": {
                        "$gt": filter.time_from,
                        "$lt": filter.time_to
                    }
                })
            else:
                _condition.update({
                    "created_time": {
                        "$gt": filter.time_from
                    }
                })
        else:
            if filter.time_to:
                _condition.update({
                    "created_time": {
                        "$lt": filter.time_to
                    }
                })

        _response = self.__collection.count_documents(_condition)

        return _response


    def get_detail(self, decision_id: str):
        _response = self.__collection.find_one({'_id': ObjectId(decision_id), "is_active": True})

        if _response:
            return DecisionEntity(**{**_response, "id": str(_response["_id"])})
        else:
            return None
        

    def get_detail_by_decision_number(self, decision_number: str):
        _response = self.__collection.find_one({'decision_number': decision_number, "is_active": True})

        if _response:
            return DecisionEntity(**{**_response, "id": str(_response["_id"])})
        else:
            return None
        
    
    def update(self, decision_id: str, decision_data: DecisionEntity):
        self.__collection.update_one(
            {
                "_id": ObjectId(decision_id)
            },
            {
                Syntax.SET: jsonable_encoder(decision_data, exclude_none=True)
            }
        )

        return decision_data
    

    def remove(self, decision_id: str):
        self.__collection.update_one(
            {
                "_id": ObjectId(decision_id)
            },
            {
                Syntax.SET: {
                    "is_active": False
                }
            }
        )

        return True

    # def _get_detail(self, client_message_id: str = None, transaction_code: str = None):
    #     """
    #         Lấy ra thông tin chi tiết của attachment
    #     """
    #     # Tìm kiếm message trong bảng message_receive với id truyền vào
    #     if client_message_id != None:
    #         _response = self.__collection.find_one({
    #             MessageReceiveCollectionField.CLIENT_MESSAGE_ID: client_message_id
    #         })
    #     else:
    #         _response = self.__collection.find_one({
    #             MessageReceiveCollectionField.TRANSACTION_CODE: transaction_code
    #         })

    #     # Nếu tìm thấy trả về thông tin chi tiết message, nếu không tìm thấy trả về None
    #     if _response:
    #         return MessageReceiveEntity(**_response)
    #     else:
    #         return None

    
    # def _count_documents(self, *args, **kwargs):
    #     """"""


    # def _get(self, *args, **kwargs):
    #     """"""
    

    # def _update(
    #         self,
    #         client_message_id: str = None,
    #         transaction_code: str = None,
    #         message_receive_data: MessageReceiveEntity = None,
    #         session = None
    #         ):
    #     """
    #         Cập nhật dữ liệu batch dataset vào trong bảng batch dataset:\n
    #         Đầu vào: BatchDatasetEntity\n
    #         Đầu ra: BatchDatasetDTO\n
    #     """
    #     if client_message_id != None:
    #         _response = self.__collection.update_one(
    #             {
    #                 MessageReceiveCollectionField.CLIENT_MESSAGE_ID: client_message_id
    #             },
    #             {
    #                 Syntax.SET: {
    #                     **message_receive_data.dict(exclude_none=True)
    #                 }
    #             },
    #             session=session
    #         )
    #     else:
    #         _response = self.__collection.update_one(
    #             {
    #                 MessageReceiveCollectionField.TRANSACTION_CODE: transaction_code
    #             },
    #             {
    #                 Syntax.SET: {
    #                     **message_receive_data.dict(exclude_none=True)
    #                 }
    #             },
    #             session=session
    #         )
        
    #     # Nếu cập nhật được thì trả về dữ liệu cập nhật
    #     return message_receive_data
    

    # def _remove(self, *args, **kwargs):
    #     """"""