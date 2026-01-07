from ..base import *
from .film_genres import *

class Genre(Base):

    name: Mapped[str] = mapped_column(String(36), unique=True)
    films: Mapped[list["Film"]] = relationship(secondary=film_genres, back_populates="genres")