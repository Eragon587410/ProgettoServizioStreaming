from ..base import *
from  .middle_tables import *

class Film(Base):
    __tablename__ = "Film"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    year: Mapped[str] = mapped_column(String(4))


    genres: Mapped[list["Genre"]] = relationship(secondary=film_genres, back_populates="films")
    users: Mapped[list["User"]] = relationship(secondary=user_films, back_populates="films")

    def __new__(cls, session = None, **kwargs):
        if session and "id" in kwargs:
            query = select(cls).where(cls.id == kwargs["id"])
            record = session.execute(query).scalars().first()
            if record:
                return record
        record = super().__new__(cls)
        record.__init__(**kwargs)
        return record
    
    @property
    def views(self):
        return len(self.users)
    
    @classmethod
    def get_films(cls, session = None):
        films = None
        if session is None:
            with cls.session() as session:
                films = session.query(cls).all()
        else:
            films = session.query(cls).all()
        return films
    
    @classmethod
    def get_most_popular_films(cls, genre = None):
        from .genre import Genre
        with cls.session() as session:
            query = select(cls).order_by(desc(cls.views))
            if genre:
                #query = query.where(genre in cls.genres)
                query = query.join(cls.genres).where(Genre.name == genre)
            films = session.execute(query).scalars().all()
        return films
    
    @classmethod
    def searchbar(cls, txt):
        film_list = []
        with cls.session() as session:
            films = cls.get_films(session=session)
            for film in films:
                if txt in film.title:
                    film_list.append(film)
            film_list.sort(key=lambda x: x.views, reverse=True)
        return [film.title for film in film_list[:20]]

    
    