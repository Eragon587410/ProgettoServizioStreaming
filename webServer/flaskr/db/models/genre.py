from ..base import *
from .middle_tables import *

class Genre(Base):
    __tablename__ = "Genre"

    name: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    films: Mapped[list["Film"]] = relationship(secondary=film_genres, back_populates="genres")

    def __new__(cls, session = None, **kwargs):
        if session and "name" in kwargs:
            query = select(cls).where(cls.name == kwargs["name"])
            record = session.execute(query).scalars().first()
            if record:
                return record
        record = super().__new__(cls)
        record.__init__(**kwargs)
        return record
    
    @classmethod
    def get_genres_names(cls):
        with cls.session() as session:
            genres = session.query(cls).all()
            return [genre.name for genre in genres]
        
    
