from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext # type: ignore
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models, schemas
from ..database import engine,get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()   
    print(posts)
    return posts


@router.post("/", response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    post =db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

@router.put("/{id}")
def update_post(id: int, post_update: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    post_query.update(post_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post_query.first()