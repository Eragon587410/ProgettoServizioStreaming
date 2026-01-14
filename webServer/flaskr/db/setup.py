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
    "Crime",
    "Romantico",
    "Storico",
    "Thriller",
    "Western",
    "Documentario",
    "Sportivo",
    "Supereroi"
]

def main():
    Base.metadata.create_all(bind=engine)

    with Genre.session() as session:
        for name in genres:
            genre = Genre(name=name)
            session.add(genre)
        session.commit()

    import json
    from pathlib import Path

    file_path = Path(__file__).parent / "default_films.json"


    with open(file_path, "r", encoding="utf-8") as f:
        films_data = json.load(f)


    print(f"Caricati {len(films_data)} film")

    for f in films_data:

        film = Film(
            title=f["titolo"],
            year=f["anno_uscita"],
            description=f["descrizione"]
        )


        for g_name in f["generi"]:

            genre = Genre(session=session, name=g_name)
            film.genres.append(genre)

        session.add(film)

    session.commit()
    print("Film importati!")


if __name__ == "__main__":
    main()