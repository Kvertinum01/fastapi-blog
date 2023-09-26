from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated

from src.schemas import User, Post, UserPost, PostToDelete
from src.schemas.post import model_to_schema
from src.auth.utils import get_current_user
from src.database.repositories import PostRepository


router = APIRouter(prefix="/social")


@router.post("/new-post", response_model=Post)
async def new_post(post: UserPost, current_user: Annotated[User, Depends(get_current_user)]):
    """
    Creates a new post
    """
    post_rep = PostRepository()
    new_post = await post_rep.new(
        creator_id=current_user.id,
        title=post.title,
        desc=post.description
    )

    return {
        "message": "post was successfully created",
        "detail": {
            "post_id": new_post.id,
        }
    }


@router.delete("/delete-post")
async def del_post(post: PostToDelete, current_user: Annotated[User, Depends(get_current_user)]):
    """
    Deletes a post if the current user created it
    """
    post_rep = PostRepository(post.id)
    post_info = await post_rep.get()

    if post_info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post was not found",
        )
    
    if post_info.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have access to this post",
        )
    
    await post_rep.delete_post()

    return {
        "message": "post was successfuly deleted"
    }


@router.get("/get-post/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """
    Returns post by id
    """
    curr_post = await PostRepository(post_id).get()

    if curr_post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post was not found",
        )
    
    return Post(
        id=curr_post.id,
        title=curr_post.title,
        description=curr_post.description,
    )


@router.get("/get-posts/{limit}")
async def get_posts(limit: int):
    """
    Returns the last N posts
    """
    posts = await PostRepository().get_last(limit)

    post_schemas = model_to_schema(posts)

    return {
        "detail": {
            "posts": post_schemas,
        }
    }
