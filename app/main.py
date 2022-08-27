from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.routers import post, user, auth, vote
from app.config import settings

# models.Base.metadata.create_all(bind=engine) this creates all the tables/models with sqlalchemy. kind of like migrate in django but this DOES NOT MODIFY EXIXSTING TABLES

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello, new world"}

