from typing import Optional, List
from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor # this is just to display the column names because by default(psycopg2), they don't show
import time
from sqlalchemy.orm import Session
import utils, schemas, models
from database import engine, get_db
from routers import post, user, auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello world"}

