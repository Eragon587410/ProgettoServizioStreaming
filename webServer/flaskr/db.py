from sqlalchemy import create_engine, text
from flask import current_app, g, session
import hashlib


#engine = create_engine("sqlite:///mydatabase.db", echo=True)
engine = create_engine("mysql+pymysql://root:root@host.docker.internal:3306/streaming", echo=True)


def get_db():
    db = engine.connect()
    db.execute(text("CREATE TABLE IF NOT EXISTS users (name VARCHAR(50) PRIMARY KEY, password VARCHAR(255) NOT NULL)"))
    db.commit()
    db.execute(text("CREATE TABLE IF NOT EXISTS films (title VARCHAR(50) PRIMARY KEY, type VARCHAR(50) NOT NULL, description VARCHAR(255) NOT NULL, image VARCHAR(255) NOT NULL)"))
    db.commit()
    return db
    
def password_hash(pw):
    hash_pw = hashlib.sha256(pw.encode()) #encode() converte la stringa in bytes
    hash_pw_exadecimal = hash_pw.hexdigest() #converte i bytes in esadecimale
    return hash_pw_exadecimal

def close_db():
    if getattr(g, "db"):
        g.db.close()

def get_films():
    with get_db() as db:
        result = db.execute(text("SELECT * FROM films")).all()
        session["films"] = []
        for film in result:
            session["films"].append({"title": film[0], "type" : film[1], "description" : film[2], "image" : film[3]})


def init_app(app):
    pass
    #app.teardown_appcontext(close_db)
    #app.cli.add_command(get_db)