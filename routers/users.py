from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from db.database import get_db
from models.user import User
from routers.crud import get_current_user
from schemas.users import UserResponse
from services.user import delete_user, change_password

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    delete_user(db, current_user.id)

@user_router.patch("/me", status_code=status.HTTP_200_OK)
def update_password(old_password: str,
                    new_password: str,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    change_password(db, current_user.id, old_password, new_password)
    return {"message": "Password changed Successfully"}


