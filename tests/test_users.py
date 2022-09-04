import pytest
from jose import jwt

from app import schemas
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     assert res.json().get("message") == "Hello world"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "bigsteppers@gmail.com", "password": "bigsteppers"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "bigsteppers@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm) # i think this does the verification
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("stuff@gmail.com", "bigsteppers", 403),
    ("bigsteppers@gmail.com", "wrong", 403),
    ("wrong@gmail.com", "wrong", 403),
    (None, "bigsteppers", 422),
    ("bigsteppers@gmail.com", None, 422)
    ])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"