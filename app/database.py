from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor # this is just to display the column names because by default(psycopg2), they don't show
import time
from config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

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



# while True: # connecting to the database manually to run raw SQLQ
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
