from src.database.models import User
from src.database.db import session_pool

from typing import Optional
from sqlalchemy import select


class UserRepository:
    def __init__(self, username: Optional[str] = None):
        self.username = username

    async def get(self) -> Optional[User]:
        async with session_pool() as session:
            query = select(User).where(User.username == self.username)
            ex_res = await session.execute(query)
            user: Optional[User] = ex_res.scalar()
            return user
        
    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with session_pool() as session:
            query = select(User).where(User.id == user_id)
            ex_res = await session.execute(query)
            user: Optional[User] = ex_res.scalar()
            return user
        
    async def new(self, password_hash: str):
        async with session_pool() as session:
            async with session.begin():
                user_obj = User(
                    username=self.username,
                    password_hash=password_hash
                )
                session.add(user_obj)
                await session.commit()
