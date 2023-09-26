from src.database.db import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from datetime import datetime


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    creator_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String(50))
    description = Column(String(200))


    def __repr__(self):
        return f'<Post: {self.id}>'
