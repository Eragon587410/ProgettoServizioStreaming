from db.base import Base
from db.engine import engine

from db.models.user import User
from db.models.film import Film
from db.models.genre import Genre
from db.models.film_genres import film_genres


def main():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()