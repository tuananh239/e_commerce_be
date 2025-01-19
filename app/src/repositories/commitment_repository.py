# =================================================================================================================
# Feature: commitment_repository
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
from app.src.models.entity.commitment_entity import CommitmentEntity

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

class CommitmentRepository(BaseRepository, metaclass=Singleton):
    """
        Class này triển khai các phương thức phục vụ cho việc truy vấn dữ liệu trong bảng commitment
    """
    def __init__(self) -> None:
        self.__client = self._get_client(MONGODB_CONST.CONNECTION.SERVER)
        self.__connection = self.__client.get_database("decision_manager")
        self.__collection = self.__connection.commitment


    def create(self, commitment_data: CommitmentEntity):
        _response = self.__collection.insert_one(jsonable_encoder(commitment_data))

        if not _response.inserted_id:
            raise RepositoryException(message="Repository error - Insert document to DB fail!")
        
        _response = self.__collection.find_one({"_id": _response.inserted_id})

        _response = CommitmentEntity(**{**_response, "id": str(_response["_id"])})

        return _response
    

    def get(self, sort=Sorting(), filter=Filtering(), pagination=Pagination(), search: str=""):
        _condition = {
            "is_active": True,
            **(filter.data),
            "$or": [
                {"decision_number": self._approximate_search(search)}
            ]
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
            _response = [CommitmentEntity(**{**commitment, "id": str(commitment["_id"])}) for commitment in _response]

        return _response
    

    def count_document(self, filter=Filtering(), search: str=""):
        _condition = {
            "is_active": True,
            **(filter.data),
            "$or": [
                {"decision_number": self._approximate_search(search)}
            ]
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


    def get_detail(self, commitment_id: str):
        _response = self.__collection.find_one({'_id': ObjectId(commitment_id), "is_active": True})

        if _response:
            return CommitmentEntity(**{**_response, "id": str(_response["_id"])})
        else:
            return None
        
    
    def update(self, commitment_id: str, commitment_data: CommitmentEntity):
        self.__collection.update_one(
            {
                "_id": ObjectId(commitment_id)
            },
            {
                Syntax.SET: jsonable_encoder(commitment_data, exclude_none=True)
            }
        )

        return commitment_data
    

    def remove(self, commitment_id: str):
        self.__collection.update_one(
            {
                "_id": ObjectId(commitment_id)
            },
            {
                Syntax.SET: {
                    "is_active": False
                }
            }
        )

        return True