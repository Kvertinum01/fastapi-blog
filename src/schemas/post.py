from pydantic import BaseModel
from typing import Tuple, List

from src.database.models import Post as PostModel


class PostToDelete(BaseModel):
    id: int


class Post(BaseModel):
    id: int
    title: str
    description: str


class UserPost(BaseModel):
    title: str
    description: str


def model_to_schema(post_models: Tuple[PostModel]) -> List[Post]:
    schemas = []

    for model in post_models:
        schemas.append(Post(
            id = model.id,
            title=model.title,
            description=model.description
        ))
    
    return schemas
