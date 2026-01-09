from ..base import *
from .middle_tables import *

class Genre(Base):
    __tablename__ = "Genre"

    name: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    films: Mapped[list["Film"]] = relationship(secondary=film_genres, back_populates="genres")