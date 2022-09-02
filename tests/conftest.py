from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# this is a file to store all fixtures that pytest comes to look for fixtures in by default in a particular package. you don't have to import it in your test files

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Chiboy17@localhost:5432/fastap_test"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # you need a session with the database


@pytest.fixture() # setting the scope (scope="module") to module means this fixture gets run only once for a partucular module. function scope is the default
def session():
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


@pytest.fixture # this fixture creates a user first for the login test, so that there's a user to login with
def test_user(client):
    user_data = {"email": "bigsteppers@gmail.com", "password": "bigsteppers"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture # this fixture creates a user first for the login test, so that there's a user to login with
def test_user2(client):
    user_data = {"email": "cactusjack@gmail.com", "password": "cactus"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    }, {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    }, {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    }, {
        "title": "fourth title",
        "content": "fourth content",
        "owner_id": test_user2["id"]
    }]

    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()
    return posts