from ..base import *
from .middle_tables import user_films
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = "User"

    username: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    films: Mapped[list["Film"]] = relationship(secondary=user_films, back_populates="users",  order_by=user_films.c.watched_at)

    def __new__(cls, session = None, **kwargs):
        if session and "username" in kwargs:
            query = select(cls).where(cls.username == kwargs["username"])
            record = session.execute(query).scalars().first()
            if record:
                return record
        record = super().__new__(cls)
        record.__init__(**kwargs)
        return record
    
    @classmethod
    def get_user(cls, session, username):
        query = select(cls).where(cls.username == username)
        return session.execute(query).scalars().first()
    
    def login(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_recent_genres(self):
        genres = defaultdict(int)
        for film in self.films[:10]:
            for genre in film.genres:
                genres[genre.id] += 1
        touple_list = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:3]
        return [genre[0] for genre in touple_list]
    
    def get_recommended_films(self):
        from .film import Film
        film_list = []
        added_ids = set()
        genres = self.get_recent_genres() * 6
        for genre in genres[:6]:
            top_genre_films = Film.get_most_popular_films(genre=genre)
            for film in top_genre_films:
                if film.id not in added_ids:
                    film_list.append(film)
                    added_ids.add(film.id)
                    break
        return film_list
