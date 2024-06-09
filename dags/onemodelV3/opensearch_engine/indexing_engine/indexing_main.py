from dags.onemodelV3.opensearch_engine.indexing_engine.preprocessor import OpensearchPreprocessor
from config import index_body
from dags.onemodelV3.logging.my_logging import loguru_logger
from dags.onemodelV3.opensearch_engine.indexing_engine.opensearch_schema import ClientSetting, IndexingSchema

from .func import (
    create_client,
    create_index,
    indexing_data,
    remove_index,
    update_data,
    index_check
)

from datetime import datetime, timedelta
import os



def main(args):

    os.environ['env'] = args.env
    from dags.onemodelV3.opensearch_engine.indexing_engine.config import index_body

    client_setting = ClientSetting(**{
        "host": args.vpce_endpoint,
        "port": args.https_port,
        "http_auth": (f"{args.opensearch_id}", f"{args.opensearch_path}"),
        "timeout": 10,
        "pool_maxsize": 40,
        "http_compress": True,
        "use_ssl": True,
        "verify_certs": True
    })
    
    opensearch_client = create_client(client_setting=client_setting, logger=loguru_logger)


    dt = datetime.today().strftime('%Y-%m-%d')
    index_name = OpensearchPreprocessor.index_name + '_' + args.env + '_' + dt
    OpensearchPreprocessor.set_index_name(new_name=index_name)
    
    ## local path Success 파일 체크
    local_path = ''

    is_created = create_index(client=opensearch_client, index_name=index_name, index_body=index_body, logger=loguru_logger)
    
    # iterable Dataset

    dataset = OpensearchPreprocessor.indexing_datset(file_path=local_path)
    response = indexing_data(client=opensearch_client, generator=dataset)

if __name__ == "__main__":
    main(args=args)
