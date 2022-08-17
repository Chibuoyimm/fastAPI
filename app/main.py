from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):  # defining a schema of what to expect from the frontend and this automitcally does the validation
    title: str
    content: str
    publshed: bool = True
    rating: Optional[int] = None


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
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) # this is to change status code; 201 status code is mostly used after post requests
def create_posts(post: Post): # post is a pydantic model

    # post.dict() is to convert a pydantic model to a dictionary

    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}  # it is conventional for the backend to send back the post detials including the id after storing


@app.get("/posts/{id}")
def get_post(id: int, response: Response):  # this is basically typecasting, but it handles error responses
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND  # editing the status code of the response
        # return {"message": f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # 204 is the status code sent after deleting something
def delete_post(id: int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
