from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor # this is just to display the column names because by default(psycopg2), they don't show
import time

app = FastAPI()


class Post(BaseModel):  # defining a schema of what to expect from the frontend and this automitcally does the validation
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='Chiboy17', cursor_factory=RealDictCursor)
        cursor = conn.cursor() # this is what is used to execute SQL statements
        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        time.sleep(2)


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


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)  # this is how you type SQL commands
    posts = cursor.fetchall()  # this actually executes the SQL command, and fetches multiple data
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) # this is to change status code; 201 status code is mostly used after post requests
def create_posts(post: Post): # post is a pydantic model

    # post.dict() is to convert a pydantic model to a dictionary

    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, # '%s' is for security, it basically sanitizes the input
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()  # this fetches one data with the SQL command

    conn.commit() # this is necessary when you want to push changes to your database like saving stuff

    return {"data": new_post}  # it is conventional for the backend to send back the post detials including the id after storing


@app.get("/posts/{id}")
def get_post(id: int, response: Response):  # this is basically typecasting, but it handles error responses
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND  # editing the status code of the response
        # return {"message": f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")


    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # 204 is the status code sent after deleting something
def delete_post(id: int):

    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id))) # it is convention to return deleted post
    deleted_post = cursor.fetchone()
    conn.commit() # you must commit when you want to make changes to the database
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return {"data": updated_post}
