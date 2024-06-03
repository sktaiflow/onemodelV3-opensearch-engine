from enum import Enum
from pydantic import BaseModel, Field

class AdotprofileKeys(Enum):
    PREFERRED_DOMAIN= 'preferred_domain'
    GENDER = 'gender'
    AGE = 'age'
    ACTIVE_STATUS = 'service_duration'
    PREFERRED_CATEGORY = 'days_after_change'
    PREFERRED_ITEM = 'preferred_item'
    MULTI_DOMAIN_TENDENCY = 'multi_domain_tendency'
    POPULAR_CONTENT_PREFERENCE = 'popular_content_preference'
    USABILITY_CRITERIA = 'usability_criteria'
    HEAVY_USE_DOMAINS = 'heavy_use_domains'




default_null = ['없음', '', '모름']

ADOT_DEFAULT_VALUES = {
    AdotprofileKeys.PREFERRED_DOMAIN.value: default_null,
    AdotprofileKeys.GENDER.value: default_null,
    AdotprofileKeys.ACTIVE_STATUS.value: default_null,
    AdotprofileKeys.PREFERRED_CATEGORY.value: default_null,
    AdotprofileKeys.PREFERRED_ITEM.value: default_null,
    AdotprofileKeys.MULTI_DOMAIN_TENDENCY.value: default_null,
    AdotprofileKeys.POPULAR_CONTENT_PREFERENCE.value: default_null,
    AdotprofileKeys.USABILITY_CRITERIA.value: default_null,
    AdotprofileKeys.HEAVY_USE_DOMAINS.value: default_null
}

def adot_select_default_value(field_name: AdotprofileKeys) -> str:
    # Logic to select the appropriate default value
    # For demonstration, we'll just return the first value in the list
    return ADOT_DEFAULT_VALUES.get(field_name, default_null)

"""
class AdotprofileKeysKeysModel(BaseModel):
    preferred_domain: str = Field(default_factory=lambda: adot_select_default_value(AdotprofileKeys.INTER.valueESTS))
    gender: str = Field(default_factory=lambda: adot_select_default_value(AdotprofileKeys.GENDER))
    age: str = Field(default_factory=lambda: adot_select_default_value(AdotprofileKeys.AGE))
    service_duration: str = Field(default_factory=lambda: adot_select_default_value(AdotprofileKeys.SERVICE_DURATION))
"""