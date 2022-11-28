from ElasticUtil import ElasticUtil


def get_elastic_client(endpoint: str):
    try:
        eu = ElasticUtil(endpoint)
    except Exception as e:
        print(e)
        exit(1)
    return eu

def load_model():
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model