from time import time
import logging
from opensearchpy import helpers, OpenSearch
from datetime import datetime
from dags.onemodelV3.common.my_logging import logger
from opensearch_schema import ClientSetting
import traceback


def create_client(client_setting:ClientSetting,  logger, **kwargs):
    client = OpenSearch(
        hosts = [{"host": client_setting.host, "port": client_setting.port}],
        http_compress=client_setting.http_compress,
        use_ssl=client_setting.use_ssl,
        verify_certs=client_setting.verify_certs,
        timeout=client_setting.timeout,
        pool_maxsize=client_setting.pool_maxsize,
        http_auth=client_setting.http_auth
    )
    logger.info(client)
    return client

def create_index(client, index_name, index_body, logger):
    """ 신규 인덱스를 생성 """
    try:
        is_exists = index_check(client=client, index_name=index_name)
        if not is_exists:
            logger.info("[create_index] create new index")
            client.indices.create(index=index_name, body=index_body)
            return True
        else:
            logger.info(f"[index_check] index: {index_name} exists")
            return False
    except Exception as e:
        logger.error(traceback.format_exc())


def remove_index(client, index_name, logger):
    """인덱스를 삭제한다"""

    if client.indices.exists(index_name):
        client.indices.delete(index=index_name)
        logger.info(f"[remove_index] remove_index {index_name}")

def index_check(client, index_name):
    if client.indices.exists(index_name):
        logger.info(f"[index_check] index: {index_name} exists")
        return True
    else:
        logger.info(f"[index_check] index: {index_name} not exists")
        return False

def indexing_data(client, generator):
    """
    신규 데이터를 지정한 index_name으로 집어 넣는다.
    """
    start_time = time.time()
    resp = helpers.bulk(
        client, 
        generator, 
        chunk_size=4000, 
        request_timeout=300
    )
    inference_time = time.time() - start_time
    return resp, inference_time

def update_data(opensearch, generator):
    pass

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