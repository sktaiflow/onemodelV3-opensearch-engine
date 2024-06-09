from typing import List, Any, Dict, Tuple, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator, ValidationInfo
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
    gender:GenderEnum = Field("unknown", description="Gender of the person")
    mno_profile_feature: Optional[str] = Field("", description="Gender of the person")
    adot_profile_feature: Optional[str] = Field("", description="Gender of the person")
    behavior_profile_feature: Optional[str] = Field("", description="Gender of the person")
    is_adot: Optional[bool] = False
    create_at: str
    user_vector:List[float]
    
    @field_validator('mno_profile_feature', 'adot_profile_feature', 'behavior_profile_feature', mode="before")
    @classmethod
    def set_empty_string_if_none(cls, v, info:ValidationInfo):
        if v is None or v in ['null']:
            return cls.model_fields[info.field_name].default
        else:
            return v
        
    @field_validator('gender', mode="before")
    @classmethod
    def set_empty_string_if_none(cls, v, info:ValidationInfo):
        if v is None or v in ['null']:
            return cls.model_fields[info.field_name].default
        else:
            return v
    model_config = {
        "extra": "forbid"
    }


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
