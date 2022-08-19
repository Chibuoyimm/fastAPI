from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Chiboy17@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # you need a session with the database

Base = declarative_base()  # all models will extend this class

# a function to connect to the database via the session and then closing the connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

