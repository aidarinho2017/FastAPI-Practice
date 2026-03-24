
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

from db.database import Base, engine
from routers.crud import auth_router
from models.user import User
from models.post import Post
from routers.posts import post_router
from routers.users import user_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
@app.get("/")
def index():
    return {"message": "Hellow, World!"}

