from sqlalchemy import create_engine, text
from flask import current_app, g


#engine = create_engine("sqlite:///mydatabase.db", echo=True)
engine = create_engine("mysql+pymysql://root:root@localhost:3306/streaming", echo=True)


def get_db():
    db = engine.connect()
    db.execute(text("CREATE TABLE IF NOT EXISTS users (name VARCHAR(50) PRIMARY KEY, password VARCHAR(255) NOT NULL)"))
    db.commit()
    return db
    


def close_db():
    if getattr(g, "db"):
        g.db.close()


def init_app(app):
    pass
    #app.teardown_appcontext(close_db)
    #app.cli.add_command(get_db)