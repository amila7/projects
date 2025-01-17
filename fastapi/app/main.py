from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts


@app.get("/posts")
def get_posts():
    posts= cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.commit()
    print(posts)
    return {"post": posts}

@app.post("/posts")
def create_posts(post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published)
                )
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    return {"data": new_post}



@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    test_post = cursor.fetchone()
    print(test_post)

    if not test_post:
        raise HTTPException(status_code=404, detail="Post with id {id}as not found")

    return {"post_detail": test_post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")

    return {"message": "Post deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")

    return {"data": updated_post}
