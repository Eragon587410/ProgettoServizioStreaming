from ..base import *
from .middle_tables import user_films
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
            