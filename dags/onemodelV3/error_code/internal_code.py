from enum import Enum, auto
"""
INTERNAL_ERROR_CODES = {
    "1":"[Pydantic] Pydantic validation checkerror",
    "2":"[Opensearch] Create index error",
    "3":"[Opensearch] Delete index error",
    "4":"[Opensearch] Indexing error",
    "5":"[Opensearch] Udate document error",
    "6":"[Opensearch] Delete document error",
    "7":"[Opensearch] Search error",
}

INTERNAL_SUCCESS_CODES = {
    "200":"[Success]",
}

class InternalCodeEnum(str, Enum):
    Error_codes = [key for key in INTERNAL_ERROR_CODES]
    Success_codes = "200"
"""
class InternalCodes(Enum):
    # Error Codes
    PYDANTIC_VALIDATION_ERROR = "1000"
    CREATE_INDEX_ERROR = "1001"
    DELETE_INDEX_ERROR = "1002"
    INDEXING_ERROR = "1003"
    UPDATE_DOCUMENT_ERROR = "1004"
    DELETE_DOCUMENT_ERROR = "1005"
    SEARCH_ERROR = "1006"

    # Success Code
    SUCCESS = auto()

    @staticmethod
    def get_message(code, e=''):
        messages = {
            InternalCodes.PYDANTIC_VALIDATION_ERROR: f"[Pydantic] Pydantic validation check error, detail_message:{e}",
            InternalCodes.CREATE_INDEX_ERROR: f"[Opensearch] Create index error, detail_message:{e}",
            InternalCodes.DELETE_INDEX_ERROR: f"[Opensearch] Delete index error, detail_message:{e}",
            InternalCodes.INDEXING_ERROR: f"[Opensearch] Indexing error, detail_message:{e}",
            InternalCodes.UPDATE_DOCUMENT_ERROR: f"[Opensearch] Update document error, detail_message:{e}",
            InternalCodes.DELETE_DOCUMENT_ERROR: f"[Opensearch] Delete document error, detail_message:{e}",
            InternalCodes.SEARCH_ERROR: f"[Opensearch] Search error, detail_message:{e}",
            InternalCodes.SUCCESS: "[Success]",
        }
        return messages.get(code, f"Undefined code, detail_message:{e}")