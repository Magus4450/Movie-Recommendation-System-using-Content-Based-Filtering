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
        import os

        import dotenv
        dotenv.load_dotenv()
        return os.getenv('ELASTICSEARCH_USERNAME'), os.getenv("ELASTICSEARCH_PASSWORD")


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
