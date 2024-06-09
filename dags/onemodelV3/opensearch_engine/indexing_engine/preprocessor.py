import pyarrow.parquet as pq
from abc import *
from typing import (
    Union, 
    Dict, 
    Set, 
    List, 
    Callable, 
    Tuple, 
    Any
) 
import pyarrow as pa
import os
from torch.utils.data import (
    IterableDataset, 
    Dataset
)
from datasets import (
    load_dataset, 
    Dataset, 
    DatasetDict,
    IterableDatasetDict
)
from pydantic import (
    BaseModel, 
    ValidationError
)

from dags.onemodelV3.opensearch_engine.indexing_engine.opensearch_schema import IndexingSchema
from dags.onemodelV3.error_code import InternalCodes
from dags.onemodelV3.logging import loguru_logger
from dags.onemodelV3.opensearch_engine.mapper import (
    MNO_DEFAULT_VALUES, 
    MnoprofileKeys, 
    mno_select_default_value, 
    mno_profile_mappings,
    new_mno_profile_mappings,
    ADOT_DEFAULT_VALUES,
    AdotprofileKeys,
    adot_select_default_value,
    adot_profile_mappings,
    new_adot_profile_mappings
)

from dags.onemodelV3.opensearch_engine.indexing_engine.regex import (
    adot_profile_regex
)

from dags.onemodelV3.opensearch_engine.indexing_engine import (
    RawInputSchema,
    IndexingSchema
)

import re
from collections import defaultdict

def read_blacklist(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        blacklist_words = [line.strip() for line in file]
    return blacklist_words


def normalize_adot_profiels(adot_profile, delimiter ="<|n|>"):
    if not adot_profile:
        return ""
     
    adot_profiles = adot_profile.split(delimiter)
    adot_profile_dict = dict()
    for profile in adot_profiles:
        key, val = profile.split(':', 1)
        key = key.strip()
        val = val.strip()
        null_values = adot_profile_mappings[key]
            
        if val in adot_select_default_value(field_name=null_values):
            pass
        else:
            adot_profile_dict[key] = val
            
    adot_template_dict = defaultdict(list)
    for key, val in new_adot_profile_mappings.items():
        adot_template_dict[val] = []

    domain = adot_profile_dict.get('선호 도메인', '')
    category = adot_profile_dict.get('선호 카테고리', '')
    item = adot_profile_dict.get('선호 아이템','')
    
    if domain:
        preference_template = f"{domain}"
        preference_item_template = ''
    else:
        preference_template = ''
        preference_item_template = ''
    
    pattern = r'^(.*?)\((.*?)\)$'
    if category:
        match = re.search(pattern, category)
        prefix = match.group(1)
        cate = match.group(2)
        if cate:
            preference_template +=f",{prefix}:{cate}"
    
    if item:
        match = re.search(pattern, item)
        if match:
            # Extract the string between parentheses
            item = match.group(2)
            preference_item_template = f"{item}"
            
        preference_template = re.sub(r'\s+(?=:)', '', preference_template)
        preference_template = re.sub(r':\s+', ':', preference_template)
        # Remove spaces after the colon
        preference_item_template = re.sub(r'\s+(?=:)', '', preference_item_template)
        preference_item_template = re.sub(r':\s+', ':', preference_item_template)
        adot_template_dict['preference'] = preference_template
        adot_template_dict['preference_item'] = preference_item_template
        #adot_preferences = adot_template_dict.get('preference', [])
        return dict(adot_template_dict)

def normalize_mno_profiels(mno_profile, delimiter ="<|n|>"):
    if not mno_profile:
        return ""
    mno_profiles = mno_profile.split(delimiter)
    mno_profile_dict = dict()
    for profile in mno_profiles:
        key, val = profile.split(':')
        null_values = mno_profile_mappings[key]
        if val in mno_select_default_value(field_name=null_values):
            """ 없음 모름 '' ... etc 이면 값을 제거한다."""
            continue
        elif val.strip() =="있음":
            mno_profile_dict[key] = key.split("이력")[0].strip()
        else:
            mno_profile_dict[key] = val.strip()

    mno_template_dict = defaultdict(list)

    for key, val in mno_profile_dict.items():
        new_feature = new_mno_profile_mappings[key]
        mno_template_dict[new_feature].append(val)

    mno_preferences = mno_template_dict.get('preference', [])
    mno_preference_template = ""        

    if mno_preferences:
        mno_preference_dict = defaultdict(set)
        mno_preference = mno_preferences[0]
        mnopreference_list = mno_preference.split(',')
        for mno_prefernce in mnopreference_list:
            split_mno_preference = mno_prefernce.split('_')
            if len(split_mno_preference) == 2:
                upper_cate, lower_cate = split_mno_preference
            else:
                upper_cate = split_mno_preference[0]

            mno_preference_dict[upper_cate].add(lower_cate)

        for key, val in mno_preference_dict.items():
            val_str = ','.join(val)
            if mno_preference_template == "": mno_preference_template = f"{key}: {val_str}"
            else: mno_preference_template += '\n' + f"{key}: {val_str}"              
        
    mno_template_dict['preference'] = mno_preference_template
    return dict(mno_template_dict)

def batch_normalize_mno_profiels(mno_profile, delimiter ="<|n|>"):
    pass


def normalize_behavior_profiels(profile):
    pass


class BaseParquetProcessor(metaclass=ABCMeta):

    @classmethod
    def load(
            cls, 
            file_path_list:List, 
            split:str=None, 
            stream:bool=True, 
            keep_in_memory:bool=False, 
            cache_dir:str='./.cache'
        ) -> Dataset:
        """ load datset from parquet files"""

        if isinstance(file_path_list, List):
            dataset = load_dataset(
                                path ="parquet", 
                                data_files=file_path_list, 
                                split=split, 
                                keep_in_memory=keep_in_memory,
                                streaming=stream,
                                cache_dir=cache_dir
                                )

        else:
            msg = f"path should be in type (List)"
            raise TypeError(msg)
        
        if split is None: dataset = dataset['train']
        
        return dataset

    @abstractmethod
    def preprocess(self, item):
        f"""code for apply to map function"""

class OpensearchPreprocessor(BaseParquetProcessor):
    index_name = "onemodelV3"
    
    def __init__(self, args, **kwargs):        
        super().__init__(args)
    
    @classmethod
    def set_index_name(cls, new_name):
        cls.index_name = new_name

    @classmethod
    def load(
            cls, 
            file_path_list:List, 
            split:str=None, 
            stream=True,
            keep_in_memory:bool=False,
            cache_dir:str='./.cache'
        ) -> IterableDataset:        
        
        dataset = super(OpensearchPreprocessor, cls).load(
                file_path_list=file_path_list, 
                split=split, 
                stream=stream, 
                keep_in_memory=keep_in_memory,
                cache_dir=cache_dir
        )
        return dataset
    
    @classmethod
    def _validate_component_inputs(cls, doc_body:Dict, schema:BaseModel) -> Dict:
        try:
            result = schema(**doc_body)
            code = InternalCodes.SUCCESS
            message = InternalCodes.get_message(code=code)
            failed_doc = None

        except ValidationError as e:
            result = None
            code = InternalCodes.PYDANTIC_VALIDATION_ERROR
            message = InternalCodes.get_message(code=code, e=e)
            failed_doc = doc_body

        finally:
            return {"result":result, "code":code, "message":message, "failed_doc":failed_doc}

    @classmethod
    def _profile_normalize(cls, data:str):
        try:
            mno_profile = normalize_mno_profiels(data["mno_profile_feature"])
            adot_profile = normalize_adot_profiels(data["adot_profile_feature"])
            behavior_profile = normalize_behavior_profiels(data["behavior_profile_feature"])
            data["mno_profile_feature"] = mno_profile
            data["adot_profile_feature"] = adot_profile
            data["behavior_profile_feature"] = behavior_profile
            data["gender"] = data.gender.value
            result = data
            failed_doc = None
            code =  InternalCodes.SUCCESS
            message = "SUCCESS"
        except Exception as e:
            result = None 
            failed_doc = data
            code  = InternalCodes.PREPROCESSING_ERROR
            message = e
        finally:
            return {"result":result, "code": code, "message": message, "failed_doc":failed_doc}

    @classmethod
    def preprocess(cls, doc:Dict) -> Dict:
        """ bulk indexing example
        actions = [
            {"_op_type": "index", "_index": "test-index", "_id": 1, "_source": {"field1": "value1"}},
            {"_op_type": "index", "_index": "test-index", "_id": 2, "_source": {"field1": "value2"}},
            {"_op_type": "update", "_index": "test-index", "_id": 1, "doc": {"field1": "updated_value1"}},
            {"_op_type": "delete", "_index": "test-index", "_id": 2}
        ]
        success, failed = bulk(client, actions)
        """
        validation_response = cls._validate_component_inputs(doc_body=doc, schema=RawInputSchema)
        if validation_response["code"] == InternalCodes.SUCCESS:
            data = validation_response["result"]
            normalize_response = cls._profile_normalize(data.dict())
            if normalize_response["code"] == InternalCodes.SUCCESS:
                data = normalize_response["result"]
                indexing_template = {
                    "_op_type": "index",
                    "_index": cls.index_name,
                    "_id": data["svc_mgmt_num"],
                    "_source": data
                }
                return {"result":indexing_template, "code":InternalCodes.SUCCESS.value, "message": "SUCCESS", "failed_doc":None}
            else:
                return normalize_response
        else:
            return validation_response         
    
    @classmethod
    def batch_process(cls, batch_docs:List) -> Dict:
        """ usage: dataloader: DataLoader(dataset, batch_size:10, collate_fn=OpensearchPreprocessor.batch_process)"""
        batch_results = []
        failed_docs = []

        for doc in batch_docs:
            response = cls.preprocess(doc=doc)
            if response["code"] == InternalCodes.SUCCESS.value:
                batch_results.append(response)
            else:
                failed_docs.append(response)

        return batch_results, failed_docs
    
    @classmethod
    def apply_maps(cls, dataset:Dataset, functions_list: List[Tuple[Callable[..., Any], bool]]) -> Dataset:
        """ instance method for apply list of functions"""
        for func, with_indices in functions_list:
            dataset = cls.apply_map(dataset=dataset, func=func, with_indices=with_indices)
        
        return dataset
    
    @classmethod
    def apply_map(cls, dataset: Dataset, func:Callable, with_indices: bool = True) -> Dataset:
        """ instance method for apply only one function"""
        dataset = dataset.map(func, with_indices=with_indices)
        return dataset