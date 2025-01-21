import pytest
from uuid import uuid4

from starlette.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sqlmodel.pool import StaticPool

from app.main import app
from app.models.core import Base
from app.models.database import get_db
from app.models.core import User


@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_db] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()  

def test_create_user(client: TestClient):  
    response = client.post(
            "/users", json={"email": "test@test.com", "password": "test"}
        )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 201
    assert data["email"] == 'test@test.com'
    assert data["name"] is None
    assert data["surname"] is None
    assert data["id"] is not None

def test_read_users(session: Session, client: TestClient):
    user_1 = User(email="test1@test.com",
                  hashed_password="test_pass_1",
                  name="test_name_1",
                  surname="test_surname_1",
                  s3_folder_id=uuid4())
    user_2 = User(email="test2@test.com",
                  hashed_password="test_pass_2",
                  name="test_name_2",
                  surname="test_surname_2",
                  s3_folder_id=uuid4())
    session.add(user_1)
    session.add(user_2)
    session.commit()

    response = client.get("/users/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["email"] == user_1.email
    assert data[0]["id"] == user_1.id
    assert data[0]["is_active"] == user_1.is_active
    assert data[0]["s3_folder_id"] == str(user_1.s3_folder_id)
    assert data[0]["items"] == []

    assert data[1]["email"] == user_2.email
    assert data[1]["id"] == user_2.id
    assert data[1]["is_active"] == user_2.is_active
    assert data[1]["s3_folder_id"] == str(user_2.s3_folder_id)
    assert data[1]["items"] == []

def test_update_user(client: TestClient):  
    response_create_user = client.post(
            "/users", json={"email": "test@test.com", "password": "test"}
        )
    data_create_user = response_create_user.json()
    
    response_token = client.post(
            "/tokens", json={"email": "test@test.com", "password": "test"}
        )
    data_token = response_token.json()
    token = data_token["access_token"]
    
    header = {
        "Authorization": token
    }
    update_json = {
        "email": "test_update@test.com",
        "password": "test_update",
        "name": "name_update",
        "surname": "surname_update"
    }
    response_update = client.put(
            "/users/self", json=update_json, headers=header
        )
    app.dependency_overrides.clear()
    data_update = response_update.json()
    
    assert response_update.status_code == 200
    assert data_update["email"] == update_json["email"]
    assert data_update["name"] == update_json["name"]
    assert data_update["surname"] == update_json["surname"]
    assert data_update["id"] == data_create_user["id"]