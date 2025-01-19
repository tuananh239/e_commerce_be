import json
from typing import Any, List, Optional
from pydantic import BaseModel

class File(BaseModel):
    name: Optional[str]
    file_id: Optional[str]

class DecisionGetDTO(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 0
    sort_by: Optional[str] = "_id"
    sort: Optional[str] = "asc"
    search: Optional[str] = ""
    decision_number: Optional[str] = ""
    decision_date: Optional[int] = None
    unit: Optional[str] = ""
    time_from: Optional[int] = None
    time_to: Optional[int] = None


class DecisionCreateDTO(BaseModel):
    decision_number: str
    decision_date: int
    unit: str
    address: Optional[str]
    number_computer: Optional[int]
    connection_type: Optional[str]
    internet_carrier: str
    intended_use: Optional[str]
    signer: str
    name: Optional[str]
    status: Optional[str]
    note: Optional[str]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        
        return value
    

class DecisionUpdateDTO(BaseModel):
    decision_number: str
    decision_date: int
    unit: str
    address: Optional[str]
    number_computer: Optional[int]
    connection_type: Optional[str]
    internet_carrier: str
    intended_use: Optional[str]
    signer: str
    name: Optional[str]
    list_image_id: Optional[List[str]]
    list_file_id: Optional[List[File]]
    list_commitment_id: Optional[List[File]]
    list_petition_id: Optional[List[File]]
    status: Optional[str]
    note: Optional[str]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        
        return value


class DecisionDTO(BaseModel):
    id: Optional[str]
    decision_number: str
    decision_date: int
    unit: str
    address: Optional[str]
    number_computer: Optional[int]
    connection_type: Optional[str]
    internet_carrier: str
    intended_use: Optional[str]
    signer: str
    name: Optional[str]
    list_image_id: Optional[List[str]]
    list_file_id: Optional[List[File]]
    list_commitment_id: Optional[List[File]]
    list_petition_id: Optional[List[File]]
    status: Optional[str]
    note: Optional[str]
    modified_by: Optional[str]
    modified_time: Optional[int]
    created_by: Optional[str]
    created_time: Optional[int]