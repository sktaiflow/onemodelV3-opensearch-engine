

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
            "is_adot": {"type": "boolean"},
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
    "index": {
        "number_of_shards": 4,
        "number_of_replicas": 1,
        "knn": True,
        "analysis":{
            "analyzer": {
                "default": {
                    "type": "standard"
                }
            }
        }        
    }
}

index_body = {
    "settings": settings,
    "mappings": mappings
}