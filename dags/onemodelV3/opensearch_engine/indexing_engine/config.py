mappings = {
        "properties": {
            "svc_mgmt_num": {"type": "keyword"},
            "luna_id": {"type": "keyword"},
            "age": {"type": "short"},
            "gender": {"type": "short"},
            "mno_profiles": {"type": "text", "analyzer": "standard", "search_analyzer": "standard"},
            "adot_profiles": {"type": "text", "analyzer": "standard", "search_analyzer": "standard"},
            "behavior_profiles": {"type": "text", "analyzer": "standard", "search_analyzer": "standard"},
            "created_at": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
            "is_active": {"type": "boolean"},
            "is_adot": {"type": "boolean"},
            "model_version": {"type": "keyword"},
            "user_embedding": {
                "type": "knn_vector",
                "dimension": 2048,
                "method": {
                    "name": "hnsw",
                    "space_type": "l2",
                    "engine": "nmslib",
                    "parameters": {"ef_construction": 16, "m": 16},
                },
            },
        }
    }

settings = {
    "index.mapping.ignore_malformed": True,
    "index.search.slowlog.threshold.query.warn": "1s",
    "index": {
        "number_of_shards": 4,
        "number_of_replicas": 1,
        "knn": True,
        "analysis":{
            "analyzer": {
                "standard": {
                    "type": "custom",
                    "char_filter":["html_strip"],
                    "tokenizer": "standard",
                    "filter": ["synonyms", "stopwords", "trim", "lowercase"]
                },
                "seunjeon":{
                    "type": "custom",
                    "char_filter":["html_strip"],
                    "tokenizer": "seunjeon_tokenizer",
                    "filter": ["synonyms", "stopwords", "trim", "lowercase"]
                },
                "ngram":{
                    "type": "custom",
                    "char_filter":["html_strip"],
                    "tokenizer": "ngram_tokenizer",
                    "filter": ["synonyms", "stopwords", "trim", "lowercase"]
                },
                "nori_tokenizer": {
                    "type": "custom",
                    "char_filter":["html_strip"],
                    "tokenizer": "nori_tokenizer",
                    "filter": ["synonyms", "stopwords", "trim", "lowercase"]
            }
        },
        "tokenizer":{
            "seunjeon_tokenizer":{
                "type": "seunjeon_tokenizer",
                "user_dict_path": "temp",
                "index_poses":[
                               
                ],
            },
            "nori_tokenizer": {
                "type": "nori_tokenizer",
                "decompound_mode": "mixed",
                "discard_punctuation": "true"
            },
        }
    }}
}

index_body = {
    "settings": settings,
    "mappings": mappings
}