from ..base import *
from sqlalchemy import DateTime
import datetime

film_genres = Table(
    "film_genres",
    Base.metadata,
    Column("film_id", ForeignKey("Film.id"), primary_key=True),
    Column("genre_id", ForeignKey("Genre.id"), primary_key=True),
)

user_films = Table(
    "user_films",
    Base.metadata,
    Column("film_id", ForeignKey("Film.id"), primary_key=True),
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("watched_at", DateTime, default=datetime.datetime.utcnow)
)