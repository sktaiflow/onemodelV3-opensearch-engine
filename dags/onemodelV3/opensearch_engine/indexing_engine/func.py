from time import time
import logging
from opensearchpy import helpers, OpenSearch
from datetime import datetime
from dags.onemodelV3.logging import loguru_logger
from dags.onemodelV3.error_code import InternalCodes
from dags.onemodelV3.opensearch_engine.indexing_engine.opensearch_schema import ClientSetting, IndexingSchema

import traceback
from pydantic import BaseModel, ValidationError
from functools import wraps
from typing import Callable, Any, Dict, Optional

def handle_operation(error_code: InternalCodes):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                code = InternalCodes.SUCCESS
                message = InternalCodes.get_message(code)
            except Exception as e:
                code = error_code
                message = InternalCodes.get_message(code, e)
                response = None
            finally:
                return {"response": response, "code": code, "message": message}
        return wrapper
    return decorator

@handle_operation(InternalCodes.DELETE_DOCUMENT_ERROR)
def delete_documents(client, index_name, doc_id, logger):
    logger.info(f"Deleting document {doc_id} from index {index_name}")
    return client.delete(index=index_name, id=doc_id)
    

@handle_operation(InternalCodes.UPDATE_DOCUMENT_ERROR)
def update_documents(client, index_name, doc_id, doc_body, logger):
    update_body = {
        "doc": doc_body,
        "doc_as_upsert": True
    }
    logger.info(f"Updating document {doc_id} in index {index_name}")
    return client.update(index=index_name, id=doc_id, body=update_body)

@handle_operation(InternalCodes.CREATE_CLIENT_ERROR)
def create_client(client_setting:ClientSetting,  logger, **kwargs):        
    return OpenSearch(
        hosts = [{"host": client_setting.host, "port": client_setting.port}],
        http_compress=client_setting.http_compress,
        use_ssl=client_setting.use_ssl,
        verify_certs=client_setting.verify_certs,
        timeout=client_setting.timeout,
        pool_maxsize=client_setting.pool_maxsize,
        http_auth=client_setting.http_auth
    )

@handle_operation(InternalCodes.CREATE_INDEX_ERROR)
def create_index(client, index_name, index_body, logger):
    """ 신규 인덱스를 생성 """
    is_exists = index_check(client=client, index_name=index_name)
    if not is_exists:
        logger.info("[create_index] create new index")
        return client.indices.create(index=index_name, body=index_body)
    else:
        logger.info(f"[index_check] index: {index_name} exists")
        code = InternalCodes.INDEX_EXIST
        message = InternalCodes.get_message(code)
        return {"response": None, "code": code, "message": message}  
        

@handle_operation(InternalCodes.DELETE_INDEX_ERROR)
def remove_index(client, index_name, logger):
    """인덱스를 삭제한다"""
    logger.info(f"[remove_index] remove_index {index_name}")
    return client.indices.delete(index=index_name)  
        
def index_check(client, index_name):
    return client.indices.exists(index_name)

@handle_operation(InternalCodes.INDEXING_ERROR)
def indexing_data(client, generator, logger, **kwargs):
    """ data indexing """
    return helpers.bulk(
        client, generator, chunk_size=kwargs.get('chunk_size', 100), request_timeout=kwargs.get('chunk_size', 300)
    )


def analyze_query(client, index_name, query, analyzer:str=None):
    if analyzer is None:
        analyzer = 'standard'
    
    body =  {
        "analyzer": analyzer,
        "text": query
    }

    response = client.indices.analyze(
        index=index_name,
        body=body
    )
    return response