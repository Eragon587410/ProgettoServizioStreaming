from ..base import *

film_genres = Table(
    "film_genres",
    Base.metadata,
    Column("film_id", ForeignKey("Film.id"), primary_key=True),
    Column("genre_id", ForeignKey("Genre.id"), primary_key=True),
)