from typing import Any, List, Optional
from pydantic import BaseModel

class File(BaseModel):
    name: Optional[str]
    file_id: Optional[str]

class CommitmentEntity(BaseModel):
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
    is_active: Optional[bool]