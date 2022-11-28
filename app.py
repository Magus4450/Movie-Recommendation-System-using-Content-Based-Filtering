from fastapi import FastAPI

from config import settings
from load_utils import get_elastic_client, load_model
from models import Movie

elastic_util = get_elastic_client(settings.endpoint)
model = load_model()

app = FastAPI()



@app.get("/recommend/{feature}/{count}", response_model=dict[int, Movie])
async def recommend_movie(feature: str, count:int = 10):

    # Encode the feature
    vector = model.encode(feature)

    # Get recommendations
    recommendations = elastic_util.generate_recommendations(vector, count)

    # Return the results
    responses = {}
    for i, hit in enumerate(recommendations):
     
        mov = Movie(**hit["_source"])
        responses[i+1] = mov

    return responses

    
    


