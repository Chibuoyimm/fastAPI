from typing import Optional, List
from multiprocessing import synchronize
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor # this is just to display the column names because by default(psycopg2), they don't show
import time
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db


models.Base.metadata.create_all(bind=engine) # this creates all the tables/models. kind of like migrate in django but this DOES NOT MODIFY EXIXSTING TABLES

app = FastAPI()



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#         password='Chiboy17', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() # this is what is used to execute SQL statements
#         print("Database connection was successful")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error", error)
#         time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of the post 1", "id": 1}, {"title": "favorite food",
"content": "i like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


@app.get("/")
def root():
    return {"message": "Hello world"}



@app.get("/posts", response_model=List[schemas.Post])  # you have to let the schema know that a list of data is coming through otherwise, it will return an error because it will think it's just one data
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)  # this is how you type SQL commands
    # posts = cursor.fetchall()  # this actually executes the SQL command, and fetches multiple data
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # this is to change status code; 201 status code is mostly used after post requests
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): # post is a pydantic model

    # post.dict() is to convert a pydantic model to a dictionary

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, # '%s' is for security, it basically sanitizes the input
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()  # this fetches one data with the SQL command

    # conn.commit() # this is necessary when you want to push changes to your database like saving stuff

    new_post = models.Post(**post.dict()) # creation of post
    db.add(new_post) # add post to database
    db.commit() # commit or save it
    db.refresh(new_post) # this retrieves the newly created post and stores it in that variable

    return new_post  # it is conventional for the backend to send back the post detials including the id after storing


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):  # this is basically typecasting, but it handles error responses
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND  # editing the status code of the response
        # return {"message": f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")


    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # 204 is the status code sent after deleting something
def delete_post(id: int,  db: Session = Depends(get_db)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id))) # it is convention to return deleted post
    # deleted_post = cursor.fetchone()
    # conn.commit() # you must commit when you want to make changes to the database

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,  db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False) # unlike creating a post, update takes in the dictionary as opposed to the unpacked dictionary for create
    db.commit()
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

