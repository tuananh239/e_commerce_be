import json
from typing import Any, List, Optional
from pydantic import BaseModel

class File(BaseModel):
    name: Optional[str]
    file_id: Optional[str]

class CommitmentGetDTO(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 0
    sort_by: Optional[str] = "_id"
    sort: Optional[str] = "asc"
    search: Optional[str] = ""
    time_from: Optional[int] = None
    time_to: Optional[int] = None


class CommitmentCreateDTO(BaseModel):
    decision_number: str
    decision_date: int
    unit: str
    signer: str
    name: Optional[str]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        
        return value
    

class CommitmentUpdateDTO(BaseModel):
    decision_number: str
    decision_date: int
    unit: str
    signer: str
    name: Optional[str]
    list_image_id: Optional[List[str]]
    list_file_id: Optional[List[File]]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        
        return value


class CommitmentDTO(BaseModel):
    id: Optional[str]
    decision_number: str
    decision_date: int
    unit: str
    signer: str
    name: Optional[str]
    list_image_id: Optional[List[str]]
    list_file_id: Optional[List[File]]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]