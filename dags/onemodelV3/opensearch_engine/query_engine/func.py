def analyze_query(client, index_name, query, analyzer:str='standard'):    
    body =  {
        "analyzer": analyzer,
        "text": query
    }

    response = client.indices.analyze(
        index=index_name,
        body=body
    )
    return response