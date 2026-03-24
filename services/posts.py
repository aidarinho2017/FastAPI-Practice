from datetime import datetime, timedelta, timezone
from typing import Optional, List

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.post import Post
from models.user import User
from schemas.posts import PostCreate, PostUpdate
from schemas.users import UserCreate, UserLogin
from services.auth import hash_password, verify_password
from services.user import get_user_by_id


def get_post_by_id(db:Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()

def get_all_posts(db: Session, page: int = 1, limit: int = 10) -> dict:
    offset = (page - 1) * limit

    total = db.query(Post).filter(Post.is_published==True).count()
    posts = (db.query(Post)
             .filter(Post.is_published == True)
             .offset(offset)
             .limit(limit)
             .all())
    return {
        "posts": posts,
        "total": total,
        "page": page,
        "pages": -(-total // limit)
    }

def get_user_posts(db: Session, user_id: int, page: int = 1, limit: int = 10) -> dict:
    offset = (page - 1) * limit

    total = db.query(Post).filter(Post.user_id == user_id).count()
    posts = (db.query(Post)
             .filter(Post.user_id == user_id)
             .offset(offset)
             .limit(limit)
             .all())

    return {
        "posts": posts,
        "total": total,
        "page": page,
        "pages": -(-total // limit)
    }

def create_post(db: Session, post_data: PostCreate, user_id: int) -> Post:
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        is_published=True,
        user_id=user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def update_post(db: Session, post_id: int, post_data: PostUpdate, user_id: int) -> Post:
    post = get_post_by_id(db, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own posts"
        )

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int, user_id: int) -> None:
    post = get_post_by_id(db, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can edit only your own posts"
        )

    db.delete(post)
    db.commit()