from enum import Enum
from pydantic import BaseModel, Field

class MnoprofileKeys(Enum):
    INTERESTS= 'interests'
    GENDER = 'gender'
    AGE = 'age'
    SERVICE_DURATION = 'service_duration'
    DAYS_AFTER_CHANGE = 'days_after_change'
    PLAN_NAME = 'plan_name'
    PLAN_PRICE = 'plan_price'
    AVG_DATA_USAGE = 'avg_data_usage'
    DEVICE_PRICE = 'device_price'
    DEVICE_MANUFACTURER = 'device_manufacturer'
    MEMBERSHIP_LEVEL = 'membership_level'
    MEMBERSHIP_HISTORY = 'membership_history'
    FAMILY_BUNDLE_HISTORY = 'family_bundle_history'
    ROAMING_HISTORY = 'roaming_history'
    SECOND_DEVICE = 'second_device'
    MICROPAYMENT_HISTORY = 'micropayment_history'

default_null = ['없음', '', '모름']

DEFAULT_VALUES = {
    MnoprofileKeys.INTERESTS.value: default_null,
    MnoprofileKeys.GENDER.value: default_null,
    MnoprofileKeys.AGE.value: default_null,
    MnoprofileKeys.SERVICE_DURATION.value: default_null,
    MnoprofileKeys.DAYS_AFTER_CHANGE.value: default_null,
    MnoprofileKeys.PLAN_NAME.value: default_null,
    MnoprofileKeys.PLAN_PRICE.value: default_null,
    MnoprofileKeys.AVG_DATA_USAGE.value: default_null + ['0gb'],
    MnoprofileKeys.DEVICE_PRICE.value: default_null,
    MnoprofileKeys.DEVICE_MANUFACTURER.value: default_null,
    MnoprofileKeys.MEMBERSHIP_LEVEL.value: default_null,
    MnoprofileKeys.MEMBERSHIP_HISTORY.value: default_null,
    MnoprofileKeys.FAMILY_BUNDLE_HISTORY.value: default_null,
    MnoprofileKeys.ROAMING_HISTORY.value: default_null,
    MnoprofileKeys.SECOND_DEVICE.value: default_null,
    MnoprofileKeys.MICROPAYMENT_HISTORY.value: default_null + ['0원']
}

def select_default_value(field_name: MnoprofileKeys) -> str:
    # Logic to select the appropriate default value
    # For demonstration, we'll just return the first value in the list
    return DEFAULT_VALUES.get(field_name, default_null)

class MnoprofileKeysKeysModel(BaseModel):
    interests: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.INTER.valueESTS))
    gender: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.GENDER))
    age: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.AGE))
    service_duration: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.SERVICE_DURATION))
    days_after_change: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.DAYS_AFTER_CHANGE))
    plan_name: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.PLAN_NAME))
    plan_price: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.PLAN_PRICE))
    avg_data_usage: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.AVG_DATA_USAGE))
    device_price: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.DEVICE_PRICE))
    device_manufacturer: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.DEVICE_MANUFACTURER))
    membership_level: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.MEMBERSHIP_LEVEL))
    membership_history: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.MEMBERSHIP_HISTORY))
    family_bundle_history: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.FAMILY_BUNDLE_HISTORY))
    roaming_history: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.ROAMING_HISTORY))
    second_device: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.SECOND_DEVICE))
    micropayment_history: str = Field(default_factory=lambda: select_default_value(MnoprofileKeys.MICROPAYMENT_HISTORY))