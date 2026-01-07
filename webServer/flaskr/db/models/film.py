from ..base import *
from  .film_genres import *

class Film(Base):
    __tablename__ = "Film"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    views: Mapped[int] = mapped_column(Integer)

    genres: Mapped[list["Genre"]] = relationship(secondary=film_genres, back_populates="films")

    def __new__(cls, session = None, **kwargs):
        if session and "id" in kwargs:
            query = select(cls).where(cls.id == kwargs["id"])
            record = session.execute(query).scalars().first()
            if record:
                return record
        record = super().__new__(cls)
        record.__init__(**kwargs)
        return record
