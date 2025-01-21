from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post,user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="123456",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connected to the database")
        break
    except Exception as e:
        print(e)

my_posts = [{
    "title": "post1",
    "content": "this is my first post",
    "id": 1},
    {
    "title": "post2",
    "content": "this is my second post",
    "id": 2
    }]

def find__posts(id):
    for post_new in my_posts:
        if post_new["id"] == id:
            return post_new
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
