from db.base import Base
from db.engine import engine

from db.models.user import User
from db.models.film import Film
from db.models.genre import Genre
from db.models.middle_tables import film_genres, user_films

import code

def main():
    code.interact(local=globals())

if __name__ == "__main__":
    main()