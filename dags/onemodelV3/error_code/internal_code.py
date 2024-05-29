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
    CREATE_CLIENT_ERROR = "1007"

    # Success Code
    SUCCESS = auto()

    # Warning Code
    INDEX_EXIST = '900'
    INDEX_CHECK = '901'
    
    @staticmethod
    def get_message(code, e=''):
        messages = {
            InternalCodes.PYDANTIC_VALIDATION_ERROR: f"[ERROR] Pydantic validation check error, detail_message:{e}",
            InternalCodes.CREATE_INDEX_ERROR: f"[ERROR] Create index error, detail_message:{e}",
            InternalCodes.DELETE_INDEX_ERROR: f"[ERROR] Delete index error, detail_message:{e}",
            InternalCodes.INDEXING_ERROR: f"[ERROR] Indexing error, detail_message:{e}",
            InternalCodes.UPDATE_DOCUMENT_ERROR: f"[ERROR] Update document error, detail_message:{e}",
            InternalCodes.DELETE_DOCUMENT_ERROR: f"[ERROR] Delete document error, detail_message:{e}",
            InternalCodes.SEARCH_ERROR: f"[ERROR] Search error, detail_message:{e}",
            InternalCodes.INDEX_EXIST: "[WARNING] INDEX EXISTS",
            InternalCodes.INDEX_CHECK: "[ERROR] INDEX CHECK FAILED",
            InternalCodes.SUCCESS: "[Success]",
        }
        return messages.get(code, f"Undefined code, detail_message:{e}")