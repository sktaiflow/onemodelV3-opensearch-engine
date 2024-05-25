from data_pipe.preprocessor import StreamPreprocessor
from config import index_body
from my_logging import logger
from opensearch_schema import ClientSetting, IndexingSchema

from .func import (
    create_client,
    create_index,
    indexing_data,
    remove_index,
    update_data,
    index_check
)

from datetime import datetime, timedelta

class OpensearchPreprocessor(StreamPreprocessor):
    index_name = "userProfile"
    
    def __init__(self, args, **kwargs):        
        super().__init__(args)
    
    @classmethod
    def set_index_name(cls, new_name):
        cls.index_name = new_name

    @classmethod
    def preprocess(cls, item):
        
        user_vector =  [float(x) for x in item['user_vector']]
        svc_mgmt_num = str(item.get("svc_mgmt_num", "temp"))  
        luna_id = item.get("luna_id", None)
        is_active = True
        is_adot = False if luna_id else True
        mno_profile = item.get("mno_profile", "")
        adot_profile = item.get("adot_profile", "")
        behavior_profiles = item.get("behavior_profiles", "")
        age = item.get("age", 31)
        gender = item.get("gender", "unknown")
        model_version = item["model_version"]

        doc = {
            "_id": svc_mgmt_num,
            "svc_mgmt_num": svc_mgmt_num,
            "luna_id": item.get("luna_id", "temp"),
            "user_embedding":user_vector,
            "mno_profile": mno_profile,
            "adot_profile": adot_profile,
            "behavior_profile": behavior_profiles,
            "gender":gender,
            "age":age,
            "is_adot": is_adot,
            "is_active": is_active,
            "model_version": model_version
        }
        
        try: 
            validated_data = IndexingSchema(**doc)
            yield validated_data.dict()
                
        except Exception as e:
            logger.info(f"Validation error: {e}")
            pass
    
    @classmethod
    def preprocess_map(cls, data):
        for item in cls.preprocess(data):
            yield {
                "_op_type": "index",
                "_index": cls.index_name,
                "_source": item
            }

    @classmethod
    def apply_map(cls, dataset):
        return dataset.map(cls.preprocess_map)
    
    @classmethod
    def indexing_datset(cls, file_path:str):
        dataset = cls.load(file_path=file_path)
        return cls.apply_map(dataset=dataset)




def main(args):

    opensearch_client = create_client(client_setting=args.client_setting, logger=logger)
    dt = datetime.today().strftime('%Y-%m-%d')
    index_name = OpensearchPreprocessor.index_name + '_' + args.env + '_' + dt
    OpensearchPreprocessor.set_index_name(new_name=index_name)
    
    ## local path Success 파일 체크
    local_path = ''
    

    is_created = create_index(client=opensearch_client, index_name=index_name, index_body=index_body, logger=logger)
    
    # iterable Dataset

    dataset = OpensearchPreprocessor.indexing_datset(file_path=local_path)
    response = indexing_data(client=opensearch_client, generator=dataset)