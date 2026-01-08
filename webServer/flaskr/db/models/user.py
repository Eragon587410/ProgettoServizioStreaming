from ..base import *

class User(Base):
    __tablename__ = "User"

    username: Mapped[str] = mapped_column(String(16), unique=True)
    password: Mapped[str] = mapped_column(String(64))

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