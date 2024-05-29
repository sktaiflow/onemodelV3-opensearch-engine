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

from opensearch_schema import IndexingSchema
from error_code import InternalCodes
from pydantic import BaseModel, ValidationError


from dags.onemodelV3.logging import loguru_logger
from loguru import Logger

class AbstractPreprocessor(metaclass=ABCMeta):
    def __init__(self, args, **kwargs):
        self.args = args
    
    @classmethod
    def load(cls, file_path:Union[str, List], split:str=None, stream:bool=True, keep_in_memory:bool=True, is_cache:bool=False, cache_dir:str='./.cache') -> IterableDataset:
        if isinstance(file_path, List):
            dataset = load_dataset("parquet", 
                                   data_files=file_path, 
                                   split=split, 
                                   keep_in_memory=keep_in_memory,
                                   streaming=stream,
                                   cache_dir=cache_dir)

        elif isinstance(file_path, str):
            if os.path.isfile(file_path):
                dataset = load_dataset("parquet", 
                                       data_files=file_path, 
                                       split=split, 
                                       keep_in_memory=keep_in_memory, 
                                       streaming=stream,
                                       cache_dir=cache_dir)
            
            elif os.path.isdir(file_path):
                dataset = load_dataset(file_path, 
                                       streaming=stream,
                                       cache_dir=cache_dir)
            else:
                msg = f"{file_path} should be dir_path | file_path"
                raise FileNotFoundError(msg)
        else:
            msg = f"path should be in type (STR or List)"
            raise TypeError(msg)
        
        if split is None:
            dataset = dataset['train']
        
        return dataset

    @abstractmethod
    def preprocess(self, item):
        f"""code for apply to map function"""

class OpensearchPreprocessor(AbstractPreprocessor):
    def __init__(self, args, **kwargs):        
        super().__init__(args)
    
    @classmethod
    def load(cls, file_path:Union[str, List], split:str=None, keep_in_memory:bool=True, is_cache:bool=True) -> IterableDataset:        
        stream = True
        dataset = super(OpensearchPreprocessor, cls).load(
                file_path=file_path, 
                split=split, 
                stream=stream, 
                keep_in_memory=keep_in_memory,
                is_cache=is_cache
        )
        return dataset
    
    @classmethod
    def doc_validation_check(cls, doc_body):
        try:
            data = IndexingSchema(**doc_body)
            code = InternalCodes.SUCCESS
            message = InternalCodes.get_message(code=code)
        except ValidationError as e:
            data = None
            code = InternalCodes.PYDANTIC_VALIDATION_ERROR
            message = InternalCodes.get_message(code=code, e=e)
        finally:
            return {"data":data, "code":code, "message":message, "doc":doc_body}

    @classmethod
    def profile_normalize(cls, profile:str, delimiter='<|n|>'):
        """성별, 나이"""
        mno_profiles = profile.split(delimiter)

        
        

    @classmethod
    def preprocess(cls, item):
        
        user_vector =  [float(x) for x in item['user_vector']]
        svc_mgmt_num = str(item.get("svc_mgmt_num", "unk"))  
        luna_id = item.get("luna_id", "unk")
        is_active = True
        is_adot = False if luna_id else True
        mno_profile = item.get("mno_profile", "")
        adot_profile = item.get("adot_profile", "")
        behavior_profiles = item.get("behavior_profiles", "")
        age = item.get("age", "unk")
        gender = item.get("gender", "unk")
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