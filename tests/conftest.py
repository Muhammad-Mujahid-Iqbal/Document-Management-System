from fastapi.testclient import TestClient
from app.main import app
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.databasecon import get_db
from app.databasecon import Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# Fixture connects to the Database, drops all old data in tables and creates a new one


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fixture is a fresh database client
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# Fixture creates a User before attempting the test_login_user
@pytest.fixture
def test_user(client):
    user_data = {
          "fname": "string",
          "lname": "string",
          "email": "user@example.com",
          "role": "developer",
          "password": "123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data['password']
    return new_user


# Fixture creates a User with admin role, authenticates it and returns headers for authentication for all API calls
@pytest.fixture
def test_headers(client):
    """
    Fixture to create a user, authenticate header create and also create a customer
    """
    user_data = {
        "fname": "string",
        "lname": "string",
        "email": "user@example.com",
        "role": "developer",
        "password": "123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    res = client.post(
        "/authenticate/", data={"username": new_user['email'], "password": new_user['password']})
    token = res.json()['access_token']
    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}

    # create a new customer also for all subsequent api calls
    customer = {"name": "Dummy User", "company": "Architrave"}
    res_customer = client.post("/customers/", headers=headers, json=customer)
    assert res_customer.status_code == 201

    res_customer = res_customer.json()
    headers['customerId'] = res_customer['id']

    return headers
