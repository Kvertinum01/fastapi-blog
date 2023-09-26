from src.database.db import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    username = Column(String(25), unique=True)
    password_hash = Column(String(128))


    def __repr__(self):
        return f'<User: {self.id}>'
