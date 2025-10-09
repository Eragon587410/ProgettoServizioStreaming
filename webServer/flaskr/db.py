from sqlalchemy import create_engine, text
from flask import current_app, g

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


def get_db():
    if not getattr(g, "db"):
        g.db = engine.connect()
        g.db.execute(text("CREATE TABLE users (name VARCHAR PRIMARY KEY, password VARCHAR NOT NULL)"))
        g.commit()
    return g.db
    
get_db()

def close_db():
    if getattr(g, "db"):
        g.db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    #app.cli.add_command(get_db)