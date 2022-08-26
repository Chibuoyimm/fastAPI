from fastapi import FastAPI

import models
from database import engine
from routers import post, user, auth, vote
from config import settings

models.Base.metadata.create_all(bind=engine) # this creates all the tables/models. kind of like migrate in django but this DOES NOT MODIFY EXIXSTING TABLES

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello world"}

