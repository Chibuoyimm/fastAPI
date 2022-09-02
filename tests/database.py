from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

from app.main import app
from app.config import settings
from app.database import get_db, Base

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Chiboy17@localhost:5432/fastap_test"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # you need a session with the database


@pytest.fixture() # setting the scope (scope="module") to module means this fixture gets run only once for a partucular module. function scope is the default
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db # this line basically overrides our get_db function with override_get_db. means that it's the one going to be called as a dependency
    yield TestClient(app)
    # run our code after our test finishes