from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from db.database import get_db
from models.user import User
from routers.crud import get_current_user
from schemas.posts import PostList, PostResponse, PostCreate, PostUpdate
from services.posts import get_all_posts, get_user_posts, create_post, update_post, delete_post

post_router=APIRouter(prefix="/posts", tags=["Posts"])

@post_router.get("/", response_model=PostList)
def get_posts(
        page: int = 1,
        limit: int = 10,
        db: Session = Depends(get_db)
        ):
    return get_all_posts(db, page, limit)

@post_router.get("my-posts", response_model=PostList)
def get_my_posts(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        page: int = 1,
        limit: int = 10
        ):
    return get_user_posts(db, current_user.id, page, limit)

@post_router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def write_post(post_data: PostCreate,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    return create_post(db, post_data, current_user.id)

@post_router.patch("/{post_id}", response_model=PostResponse)
def change_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    return update_post(db, post_id, post_data, current_user.id)

@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    delete_post(db, post_id, current_user.id)