import pytest
import json

from starlette.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sqlmodel.pool import StaticPool

from app.main import app
from app.models.core import Base
from app.models.database import get_db
from app.models.core import Item


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

def test_create_item(client: TestClient):  
    response_create_user = client.post(
            "/users", json={"email": "test@test.com", "password": "test"}
        )
    print(f"response_create_user: {response_create_user}")
    response_token = client.post(
            "/tokens", json={"email": "test@test.com", "password": "test"}
        )
    print(f"response_token: {response_token}")

    data_token = response_token.json()
    token = data_token["access_token"]
    print(f"token: {token}")

    item_create_json = {
        "title": "test_title",
        "description": "test_description"
    }
    test_data = [
        {
            "test1": 1
        },
        {
            "test2": 2
        }
    ]
    test_bytes = str.encode(json.dumps(test_data))
    file={
        "item_data": ('json_test.json', test_bytes)
    }
    header = {
        "Authorization": token
    }
    try:
        response_item_create = client.post(
                "/items",
                params=item_create_json,
                files=file,
                headers=header
            )
    except Exception as e:
        print(f"response_item_create error: {repr(e)}")
    app.dependency_overrides.clear()
    
    print(response_item_create)

    data_item_create = response_item_create.json()
    assert response_item_create.status_code == 201
    assert data_item_create["title"] == item_create_json["title"]
    assert data_item_create["description"] == item_create_json["description"]
    assert data_item_create["s3_path"] is not None
    assert data_item_create["id"] is not None

def test_read_items(session: Session, client: TestClient):
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
    
    item_1 = Item(title="title_test1",
                  description="description_test1",
                  s3_path="s3_path_test1",
                  owner_id=data_create_user["id"])
    item_2 = Item(title="title_test2",
                  description="description_test2",
                  s3_path="s3_path_test2",
                  owner_id=data_create_user["id"])
    session.add(item_1)
    session.add(item_2)
    session.commit()

    response_all_items = client.get("/items/", headers=header)
    data_all_items = response_all_items.json()
    assert response_all_items.status_code == 200
    assert len(data_all_items) == 2
    assert data_all_items[0]["title"] == item_1.title
    assert data_all_items[0]["description"] == item_1.description
    assert data_all_items[0]["id"] == item_1.id
    assert data_all_items[0]["owner_id"] == item_1.owner_id
    assert data_all_items[0]["s3_path"] == item_1.s3_path

    response_item = client.get(f"/items/{item_2.id}", headers=header)
    app.dependency_overrides.clear()

    data_item = response_item.json()
    assert response_item.status_code == 200
    assert data_item["title"] == item_2.title
    assert data_item["description"] == item_2.description
    assert data_item["id"] == item_2.id
    assert data_item["s3_path"] == item_2.s3_path

def test_update_item(session: Session, client: TestClient):  
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
    
    item_1 = Item(title="title_test1",
                  description="description_test1",
                  s3_path="s3_path_test1",
                  owner_id=data_create_user["id"])
    session.add(item_1)
    session.commit()
    
    update_json = {
        "item_id": item_1.id,
        "title": "test_update_title",
        "description": "test_update_description"
    }
    response_update = client.put(
            f"/items/{item_1.id}", params=update_json, headers=header
        )
    app.dependency_overrides.clear()
    data_update = response_update.json()
    
    assert response_update.status_code == 201
    assert data_update["title"] == update_json["title"]
    assert data_update["description"] == update_json["description"]
    assert data_update["s3_path"] == item_1.s3_path
    assert data_update["id"] == update_json["item_id"]