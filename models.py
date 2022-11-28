from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    type: str
    director: str
    cast: str
    rating: str
    description: str
    release_year: int

