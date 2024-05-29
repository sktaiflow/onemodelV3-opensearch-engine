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
    PYDANTIC_VALIDATION_ERROR = auto()
    CREATE_INDEX_ERROR = auto()
    DELETE_INDEX_ERROR = auto()
    INDEXING_ERROR = auto()
    UPDATE_DOCUMENT_ERROR = auto()
    DELETE_DOCUMENT_ERROR = auto()
    SEARCH_ERROR = auto()

    # Success Code
    SUCCESS = auto()

    @staticmethod
    def get_message(code):
        messages = {
            InternalCodes.PYDANTIC_VALIDATION_ERROR: "[Pydantic] Pydantic validation check error",
            InternalCodes.CREATE_INDEX_ERROR: "[Opensearch] Create index error",
            InternalCodes.DELETE_INDEX_ERROR: "[Opensearch] Delete index error",
            InternalCodes.INDEXING_ERROR: "[Opensearch] Indexing error",
            InternalCodes.UPDATE_DOCUMENT_ERROR: "[Opensearch] Update document error",
            InternalCodes.DELETE_DOCUMENT_ERROR: "[Opensearch] Delete document error",
            InternalCodes.SEARCH_ERROR: "[Opensearch] Search error",
            InternalCodes.SUCCESS: "[Success]",
        }
        return messages.get(code, "Unknown code")