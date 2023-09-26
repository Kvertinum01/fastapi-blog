from src.database.models import Post
from src.database.db import session_pool

from typing import Optional, Tuple
from sqlalchemy import select, delete


class PostRepository:
    def __init__(self, post_id: Optional[int] = None) -> None:
        self.post_id = post_id
    
    async def get(self):
        async with session_pool() as session:
            query = select(Post).where(Post.id == self.post_id)
            ex_res = await session.execute(query)
            post: Optional[Post] = ex_res.scalar()
            return post
        
    async def delete_post(self):
        async with session_pool() as session:
            query = delete(Post).where(Post.id == self.post_id)
            await session.execute(query)
            await session.commit()
    
    @classmethod
    async def new(cls, creator_id: int, title: str, desc: str):
        async with session_pool() as session:
            async with session.begin():
                post_obj = Post(
                    creator_id=creator_id,
                    title=title,
                    description=desc,
                )
                session.add(post_obj)

                await session.flush()
                await session.refresh(post_obj)
                await session.commit()

                return post_obj
        
    @classmethod
    async def get_last(cls, limit = 10) -> Tuple[Post]:
        async with session_pool() as session:
            query = select(Post).order_by(Post.created_at).limit(limit)
            ex_res = await session.execute(query)
            posts = ex_res.all()
            return next(zip(*posts), ())
