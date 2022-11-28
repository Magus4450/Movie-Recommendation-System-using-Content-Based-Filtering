import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer


class ElasticIndexer:

    def __init__(self, df_file_name:str, feature_names:list[str], lemmatize:list[bool], verbose:bool) -> None:
        self.df = self._load_dataframe(df_file_name)
        self.feature_names = feature_names
        self.lemmatize = lemmatize
        self.verbose = verbose
        self.encoded = None

    
    def _load_dataframe(self, df_file_name:str) -> pd.DataFrame:
        """Loads dataframe in class instance

        Args:
            df_file_name (str): File name of the dataframe

        Returns:
            pd.DataFrame: Loaded dataframe
        """
        # if self.verbose: print("Loading dataframe...")
        try:
            df = pd.read_csv(df_file_name)
            df = self._remove_nan_values(df)
        except Exception as e:
            print("Error loading dataframe")
            print(e)
            exit(1)
        # if self.verbose: print("Dataframe loaded")
        return df

    def _remove_nan_values(self, df:pd.DataFrame):
        """Removes NaN values from the dataframe
        """
        return df.fillna("")
    
    def _generate_features(self):
        """Generates features by comibing and cleaning multiple columns
        """
        # if self.verbose: print("Generating features...")
        for i, feature_name in enumerate(self.feature_names):
            self.df[f'cleaned_{feature_name}'] = self.df[feature_name].apply(lambda x: self.clean_doc(x, lemmatize=self.lemmatize[i]))

        generated_feature_names = [f'cleaned_{feature_name}' for feature_name in self.feature_names]
        self.df['feature'] = self.df[generated_feature_names].agg(" ".join, axis=1)
        # if self.verbose: print("Features generated")


    def _encode_features(self, sentence_encoder:str = 'all-MiniLM-L6-v2'):
        """Encodes the features using the sentence encoder. Generates a list of dict full of data to be indexed

        Args:
            sentence_encoder (str, optional): Name of sentence encoder from SBERT. Defaults to 'all-MiniLM-L6-v2'.
        """
        # if self.verbose: privernt("Encoding features...")

        from sentence_transformers import SentenceTransformer
        try:
            model = SentenceTransformer(sentence_encoder)
        except Exception as e:
            print("Error loading sentence encoder")
            exit(1)
        
        encoded = []
        for _, row in self.df.iterrows():
            dict_ = {
                "title" : row["title"],
                "type" : row["type"],
                "director": row["director"],
                "cast": row["cast"],
                "rating": row["rating"],
                "description": row["description"],
                "release_year": row["release_year"],
                "feature_vector" :model.encode(row["feature"])
            }
            encoded.append(dict_)
        # print(encoded[10])
        self.encoded = encoded


        

        # if self.verbose: print("Features encoded")

    def _create_generator(self):
        """Creates a generator for the dataframe to be indexed into Elasticsearch

        Args:
            df (pd.DataFrame): Dataframe to be indexed

        Raises:
            StopIteration: When the generator is exhausted

        Yields:
            dict : Dictionary containing the data to be indexed
        """
        for i, line in enumerate(self.encoded):
            yield {
                "_index": "netflix",
                "_id": i,
                "_source": {
                    "title" : line['title'],
                    "type" : line['type'],
                    "director": line['director'],
                    "cast": line['cast'],
                    "rating": line['rating'],
                    "description": line['description'],
                    "release_year": line['release_year'],    
                    "feature_vector" : line['feature_vector'],
                }
            }
        raise StopIteration


    def clean_doc(self, doc: str, lemmatize: bool=True) -> str:
        """ Performs basic cleaning of text data. Takes in a sentence, tokenizes it, removes stopwords, and lemmatizes it.

        Args:
            doc (str): document to be cleaned
            lemmatize (bool, optional): whether to lemmatize or not. Defaults to True.

        Returns:
            str: cleaned tokens as a string with ' ' as a delimiter
        """
        if type(doc) != str: return " "
        
        tokenizer = WordPunctTokenizer()
        tokens = tokenizer.tokenize(doc)
        tokens = [word.lower() for word in tokens]

        # Remove stopwords
        stopword = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stopword]

        # Remove punctuations
        tokens = [word for word in tokens if word.isalpha() or word.isnumeric()]
        
        if lemmatize:
            # Lemmatize
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(word) for word in tokens]

        return " ".join(tokens)

    def index(self):
        """Indexes the data into elastic search
        """
        self._generate_features()
        self._encode_features()
        gen = self._create_generator()

        from config import settings
        from ElasticUtil import ElasticUtil

        eu = ElasticUtil(settings.endpoint)
        eu.populate_index(settings.index, gen)
        


if __name__ == "__main__":
    indexer = ElasticIndexer("netflix_titles.csv", ["description", "cast", "title", "director"], [True, False, False, False], verbose=True)
    indexer.index()


