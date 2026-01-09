from db.base import Base
from db.engine import engine

from db.models.user import User
from db.models.film import Film
from db.models.genre import Genre
from db.models.middle_tables import film_genres, user_films

genres = [
    "Azione",
    "Avventura",
    "Animazione",
    "Biografico",
    "Commedia",
    "Drammatico",
    "Fantasy",
    "Fantascienza",
    "Guerra",
    "Horror",
    "Musical",
    "Poliziesco / Crime",
    "Romantico",
    "Storico",
    "Thriller",
    "Western",
    "Documentario"
]

def main():
    Base.metadata.create_all(bind=engine)

    with Genre.session() as session:
        for name in genres:
            genre = Genre(name=name)
            session.add(genre)
        session.commit()

if __name__ == "__main__":
    main()