
from app import schemas
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get('/')
    assert (res.json().get('message')) == "Welcome to DMS APP by Mujahid"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json= {
        "fname": "string",
        "lname": "string",
        "email": "user@example.com",
        "role": "developer",
        "password": "123"
    })

    res_json = res.json()
    assert res_json['email'] == "user@example.com"
    assert res.status_code == 201


def test_create_user_fail(client):
    res = client.post("/users/", json={
        "wrongType": 1,
        "password": "cs123"
    })
    assert res.status_code == 422


def test_get_users(client, test_headers):
    res = client.get("/users/", headers=test_headers)
    assert res.status_code == 200


def test_delete_user(client,test_headers):
    res = client.delete("/users/1", headers=test_headers)
    assert res.status_code == 204


def test_delete_user_fail(client, test_headers):
    res = client.delete("/users/22", headers=test_headers)
    assert res.status_code == 404


def test_login_user(test_user, client):
    res = client.post(
        "/authenticate/", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    role: str = payload.get("role")
    assert id == test_user['id']
    assert role == test_user['role']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200
