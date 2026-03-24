from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from db.database import get_db
from models.user import User
from schemas.users import UserResponse, UserCreate, UserLogin
from services.auth import verify_token, create_access_token
from services.user import get_user_by_username, create_user, authenticate_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    username = verify_token(token)
    user = get_user_by_username(db, username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    user = authenticate_user(db, user_login)

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}