import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)
SESSION_ID = "test_session_123"

def test_get_tasks_empty():
    response = client.get(f"/tasks?session_id={SESSION_ID}")
    assert response.status_code == 200
    assert response.json() == []

def test_create_task():
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "A test",
        "status": "todo",
        "session_id": SESSION_ID
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["id"] is not None

def test_get_task():
    create = client.post("/tasks", json={
        "title": "Another task",
        "description": "For get test",
        "status": "todo",
        "session_id": SESSION_ID
    })
    task_id = create.json()["id"]
    response = client.get(f"/tasks/{task_id}?session_id={SESSION_ID}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task():
    create = client.post("/tasks", json={
        "title": "Old title",
        "description": "Old description",
        "status": "todo",
        "session_id": SESSION_ID
    })
    task_id = create.json()["id"]
    response = client.put(f"/tasks/{task_id}?session_id={SESSION_ID}", json={
        "title": "New title",
        "description": "New description",
        "status": "done"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["status"] == "done"

def test_delete_task():
    create = client.post("/tasks", json={
        "title": "Task to delete",
        "description": "Will be deleted",
        "status": "todo",
        "session_id": SESSION_ID
    })
    task_id = create.json()["id"]
    response = client.delete(f"/tasks/{task_id}?session_id={SESSION_ID}")
    assert response.status_code == 204
    get_response = client.get(f"/tasks/{task_id}?session_id={SESSION_ID}")
    assert get_response.status_code == 404

def test_session_isolation():
    client.post("/tasks", json={
        "title": "Session A task",
        "description": "Belongs to A",
        "status": "todo",
        "session_id": "session_A"
    })
    response = client.get("/tasks?session_id=session_B")
    assert response.json() == []