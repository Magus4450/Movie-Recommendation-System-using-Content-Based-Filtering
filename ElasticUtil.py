from elasticsearch import Elasticsearch


class ElasticUtil:
    """Simple Util class to connect to ElasticSearch
    """

    def __init__(self, endpoint: str) -> None:
        """Set up required variables

        Args:
            endpoint (str): Endpoint of ElasticSearch
        """
        self.endpoint = endpoint
        self._e_user, self._e_pass = self._load_user_pass()
        self._elastic_client = self._connect_to_elastic()
    
    def _load_user_pass(self):
        """Load username and password from file

        Returns:
            (str, str): username and password
        """
        from config import settings
        return settings.elastic_username, settings.elastic_password


    def _connect_to_elastic(self):
        """Connects to elastic search

        Raises:
            Exception: If error in connecting to ElasticSearch, raise Exception

        Returns:
            ElasticSearch: ElasticSearch client
        """
        es = Elasticsearch(
            self.endpoint,
            http_auth=(self._e_user, self._e_pass),
        )
        if not es.ping():
            raise Exception("Could not connect to ElasticSearch")
            
        return es
    
    def get_elastic_client(self):
        """Returns elastic search client

        Returns:
            ElasticSearch: ElasticSearch client
        """
        return self._elastic_client
    
    


    def _create_index(self, index_name:str):
        """Create index in ElasticSearch

        Args:
            index_name (str): Name for the index
        """
        settings = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1,
            },
            "mappings": {
                "properties": {
                    "title": {
                        "type" : "text",
                    },
                    "type": {
                        "type" : "text",
                    },
                    "director": {
                        "type" : "text",
                    },
                    "cast": {
                        "type" : "text",
                    },
                    "rating": {
                        "type" : "text",
                    },  
                    "description": {
                        "type" : "text",
                    },
                    "release_year": {
                        "type" : "integer",
                    },
                    "feature_vector":{
                        "type" : "dense_vector",
                        "dims" : 384 
                    }
                }
            }
        }
        self._elastic_client.indices.create(index=index_name, body=settings, ignore=400)

    def populate_index(self, index_name, gen):
        """Populated data in the index from the generator

        Args:
            index_name (_type_): name for the index
            gen (generator): generator that yields data
        """
        # Deleting the index if it exists
        self._elastic_client.indices.delete(index=index_name, ignore=[400, 404])
        
        self._create_index("netflix")
        from elasticsearch.helpers import bulk
        try:
            bulk(self._elastic_client, gen)
        except Exception as e:
            print(e)
            print("Data indexing complete!")


    def generate_recommendations(self, vector: list[float], n_recommendations: int):
        """Generate recommendations by performing a vector search on the basis of cosine similarity

        Args:
            vector (list[float]): Feature vector
            n_recommendations (int): Number of recommendatiosn to generate

        Returns:
            dict : Metadata of the recommendations
        """

        script_query = {
            "script_score" : {
                "query" : {
                    "match_all" : {}
                },
                "script" : {
                    "params": {"query_vector": vector},
                    "source" : "cosineSimilarity(params.query_vector, 'feature_vector') + 1.0"
                }
                
                }
        }   
        response = self._elastic_client.search(
            index = "netflix",
            body = {
                "size" : n_recommendations,
                "query": script_query,
                "_source": ["title", "type", "director", "cast", "rating", "description", "release_year"]
            }
        )

        return response["hits"]["hits"]
        
