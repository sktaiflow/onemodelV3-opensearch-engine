from typing import List, Any, Dict, Tuple, Optional
from pydantic import BaseModel, Field, ValidationError
from enum import Enum

class ClientSetting(BaseModel):
    host:str
    port:int
    http_auth:Tuple[str, str]
    timeout:Optional[int]=2
    pool_maxsize: Optional[int]=40
    http_compress:Optional[bool]=True,
    use_ssl:Optional[bool]=True,
    verify_certs:Optional[bool]=True


class GenderEnum(str, Enum):
    male = "male"
    female = "female" 
    unknown = "unknown"


class RawInputSchema(BaseModel):
    svc_mgmt_num: str = Field(..., min_length=1)
    luna_id: str
    age: Optional[int] = Field(None, gt=0)
    gender:GenderEnum = Field(..., description="Gender of the person")
    mno_profile_feature: Optional[str]
    adot_profile: Optional[str]
    behavior_profile: Optional[str]
    is_adot: Optional[bool]
    created_at: str
    user_vector:List[float]
    class Config:
        extra = 'forbid'


class IndexingSchema(BaseModel):
    _id:str
    svc_mgmt_num: str = Field(..., min_length=1)
    luna_id: str
    age: Optional[int] = Field(None, gt=0)
    gender:GenderEnum = Field(..., description="Gender of the person")
    mno_profile: str
    adot_profile: str
    behavior_profile: str
    is_active: bool
    is_adot: bool
    model_version:str
    created_at: str
    user_embedding:List[float]
    class Config:
        extra = 'forbid'
