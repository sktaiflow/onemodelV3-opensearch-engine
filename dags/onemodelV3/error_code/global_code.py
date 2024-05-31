GLOBAL_ERROR_CODES = {
    "403":"[GlobalCode]Forbidden (API 접근권한 미존재)",
    "404":"[GlobalCode]Internet Error (Internet 연결 오류)",
    "405":"[GlobalCode]Invalid Method (Request Method <Get, Post> 불일치)",
    "422":"[GlobalCode]Invalid Input Type (Request Body 내, Input Key 값 오류 혹은 필수 Input Key 값 누락)",
    "444":"[CustomCode]Engine Logic Error (Engine 내부 동작 오류)",
    "500":"[GlobalCode]Internet Server Error (Engine Code or Traffic 과부하 오류)",
    "445":"[CustomCode]Engine Server Error(Engine 인덱스 업데이트 속도 오류)",
    "446":"[CustomCode]Opensearch Index Error(오픈서치 인덱스 오류)",
    "447":"[CustomCode]Opensearch  Error(오픈서치 검색 API 오류)",
    "448":"[CustomCode]Category Classifier model Error(카테고리 모델 오류)",
    "449":"[CustomCode]MirrorDB Connection Error(DB Connection 오류)",
    "450":"[CustomCode]질의분석기 오류",
    "451":"[CustomCode]Geo Reverse API Error(위경도 변환 오류)"
}