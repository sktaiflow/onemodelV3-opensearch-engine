from typing import List, Dict, Any

from typing import List, Dict, Any

def keyword_get_base_query(
        source: List = [], 
        must_query: List = [], 
        should_query: List = [], 
        filter_query: Dict = {},
        W: Dict = {}, 
        function_score_query: Dict = {}, 
        functions: List = [],
        is_highlight:bool=False
        ) -> Dict[str, Any]:
    
    must_not_filter = filter_query.get('must_not', [])
    must_filter = filter_query.get('must', [])
    size = W.get("size", 5)
    if is_highlight:
        highlight_statement = {
                "require_field_match": "false",
                "fields": {
                    "mno_profiles": {},
                    "adot_profiles": {},
                    "behavior_profiles": {}
                }
            }
    else:
        highlight_statement = {}

    base_query_dsl = {
        "_source": source,
        "size": size,
        "query": {
            "bool": {
                "must": [{
                    "bool": {
                        "should": must_query,
                        "minimum_should_match": 1
                    }
                }],
                "should": should_query,
                "filter": [{
                    "bool": {
                        "must_not": must_not_filter,
                        "must": must_filter
                    }
                }]
            }
        },
        "highlight": highlight_statement,
        "sort": ["_score"],
    }

    # Check if function_score_query and functions are provided
    if function_score_query or functions:
        function_score_part = {
            "query": base_query_dsl["query"],
            "functions": functions,
            **function_score_query
        }
        
        # If script score is provided, add it to the function score part
        if "script_score" in function_score_query:
            function_score_part["script_score"] = function_score_query["script_score"]
        
        base_query_dsl["query"] = {
            "function_score": function_score_part
        }

    return base_query_dsl

def vector_get_base_query(
        vector,
        source: List = [], 
        W: Dict = {},
    ) -> Dict[str, Any]:
    size = W.get("size", 5)
    base_query_dsl = {
        "_source": source,
        "size": size,
        "query": {
            "knn": {
                "user_embedding": {
                    "vector": vector,
                    "k": size
                }
            }
        }
    }
    return base_query_dsl

def hybrid_get_base_query(
        
        source: List = [], 
        must_query: List = [], 
        should_query: List = [], 
        filter_query: Dict = {},
        W: Dict = {}, 
        function_score_query: Dict = {}, 
        functions: List = []
        ):
    
    must_not_filter = filter_query.get('must_not', [])
    must_filter = filter_query.get('must', [])
    size = W.get("size", 5)

    base_query_dsl = {
        "_source": source,
        "size": size,
        "query": {
            "bool": {
                "must": [{
                    "bool": {
                        "should": must_query,
                        "minimum_should_match": 1
                    }
                }],
                "should": should_query,
                "filter": [{
                    "bool": {
                        "must_not": must_not_filter,
                        "must": must_filter
                    }
                }]
            }
        },
        "sort": ["_score"],
    }

    # Check if function_score_query and functions are provided
    if function_score_query or functions:
        function_score_part = {
            "query": base_query_dsl["query"],
            "functions": functions,
            **function_score_query
        }
        
        # If script score is provided, add it to the function score part
        if "script_score" in function_score_query:
            function_score_part["script_score"] = function_score_query["script_score"]
        
        base_query_dsl["query"] = {
            "function_score": function_score_part
        }

    return base_query_dsl

def vector_get_base_query(
        vector,
        source: List = [], 
        W: Dict = {},
    ) -> Dict[str, Any]:
    
    size = W.get("size", 5)
    base_query_dsl = {
        "_source": source,
        "size": size,
        "query": {
            "knn": {
                "user_embedding": {
                    "vector": vector,
                    "k": size
                }
            }
        }
    }
    return base_query_dsl

def hybrid_get_base_query(
        
        source: List = [], 
        must_query: List = [], 
        should_query: List = [], 
        filter_query: Dict = {},
        W: Dict = {}, 
        function_score_query: Dict = {}, 
        functions: List = []
        ):
    
    must_not_filter = filter_query.get('must_not', [])
    must_filter = filter_query.get('must', [])
    size = W.get("size", 5)

    base_query_dsl = {
        "_source": source,
        "size": size,
        "query": {
            "bool": {
                "must": [{
                    "bool": {
                        "should": must_query,
                        "minimum_should_match": 1
                    }
                }],
                "should": should_query,
                "filter": [{
                    "bool": {
                        "must_not": must_not_filter,
                        "must": must_filter
                    }
                }]
            }
        },
        "sort": ["_score"],
    }

    # Check if function_score_query and functions are provided
    if function_score_query or functions:
        function_score_part = {
            "query": base_query_dsl["query"],
            "functions": functions,
            **function_score_query
        }
        
        # If script score is provided, add it to the function score part
        if "script_score" in function_score_query:
            function_score_part["script_score"] = function_score_query["script_score"]
        
        base_query_dsl["query"] = {
            "function_score": function_score_part
        }

    return base_query_dsl