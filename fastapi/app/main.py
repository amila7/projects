from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine,get_db
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
        

@app.get("/")
def root():
    return {"message": "hey amila"}



@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()   
    print(posts)
    return posts


@app.post("/posts", response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post



@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    post =db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    return post

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, post_update: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    post_query.update(post_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post_query.first()



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    #hash the password - user.password
    hash_password=pwd_context.hash(user.password)
    user.password=hash_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
