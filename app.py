from fastapi import FastAPI
from pydantic import BaseModel

from load_utils import *

app = FastAPI()


model = None
client = None


if client is None:
    client = get_elastic_client("http://localhost:9200")

if model is None:
    model = load_model()


class Movie(BaseModel):
    title: str
    type: str
    director: str
    cast: str
    rating: str
    description: str
    release_year: int

@app.get("/recommend/{feature}/{count}", response_model=dict[int, Movie])
async def recommend_movie(feature: str, count:int):

    # Encode the feature
    vector = model.encode(feature)

    # Get the top {count} similar movies
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
    response = client.search(
        index = "netflix",
        body = {
            "size" : count,
            "query": script_query,
            "_source": ["title", "type", "director", "cast", "rating", "description", "release_year"]
        }
    )

    # Return the results
    responses = {}

    for i, hit in enumerate(response["hits"]["hits"]):
        mov = Movie(**hit["_source"])
        responses[i+1] = mov
    return responses

    
    


