#~movie-bag/database/models.py
from .utils import db

class Movie(db.Document):
    name = db.StringField(required=True)
    route_url = db.StringField(required=True)
    is_scraped = db.BooleanField(required=True, default= False)
    rating = db.StringField()
    score = db.StringField()
    votes_nb = db.StringField()
    director = db.StringField()
    writers = db.ListField(db.StringField())
    movie_duration = db.StringField()
    types = db.ListField(db.StringField())
    release_date = db.StringField()
    release_country = db.StringField()
    filming_location = db.ListField(db.StringField())
    reviews_nb = db.StringField()
    storyline = db.StringField()
    budget = db.StringField()
    opening_weekend_usa = db.StringField()
    gross_usa = db.StringField()
    cumulative_worldwide_gross = db.StringField()
    runtime = db.StringField()
    color = db.ListField(db.StringField())
    sound_mix = db.ListField(db.StringField())
    aspect_ratio = db.ListField(db.StringField())

__all__ = ["Movie"]