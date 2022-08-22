from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import get_db
from typing import List
from sqlalchemy.orm import Session

from app import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",  # this simplifies having to put "/posts" in all of your routes, it's a base prefix for all the routes here
    tags=["Posts"]  # this is to group them on the documentation
)

@router.get("/", response_model=List[schemas.Post])  # you have to let the schema know that a list of data is coming through otherwise, it will return an error because it will think it's just one data
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts """)  # this is how you type SQL commands
    # posts = cursor.fetchall()  # this actually executes the SQL command, and fetches multiple data
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # this is to change status code; 201 status code is mostly used after post requests
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)): # post is a pydantic model

    # post.dict() is to convert a pydantic model to a dictionary

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, # '%s' is for security, it basically sanitizes the input
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()  # this fetches one data with the SQL command

    # conn.commit() # this is necessary when you want to push changes to your database like saving stuff
    print(user_id)
    new_post = models.Post(**post.dict()) # creation of post
    db.add(new_post) # add post to database
    db.commit() # commit or save it
    db.refresh(new_post) # this retrieves the newly created post and stores it in that variable

    return new_post  # it is conventional for the backend to send back the post detials including the id after storing


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):  # this is basically typecasting, but it handles error responses
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND  # editing the status code of the response
        # return {"message": f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")


    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) # 204 is the status code sent after deleting something
def delete_post(id: int,  db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id))) # it is convention to return deleted post
    # deleted_post = cursor.fetchone()
    # conn.commit() # you must commit when you want to make changes to the database

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,  db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False) # unlike creating a post, update takes in the dictionary as opposed to the unpacked dictionary for create
    db.commit()
    return post_query.first()