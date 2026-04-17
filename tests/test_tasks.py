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

# Test GET /tasks (empty)
def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

# Test POST /tasks
def test_create_task():
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "A test",
        "status": "todo"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["id"] is not None

# Test GET /tasks/{id}
def test_get_task():
    create = client.post("/tasks", json={
        "title": "Another task",
        "description": "For get test",
        "status": "todo"
    })
    task_id = create.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

# Test PUT /tasks/{id}
def test_update_task():
    create = client.post("/tasks", json={
        "title": "Old title",
        "description": "Old description",
        "status": "todo"
    })
    task_id = create.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={
        "title": "New title",
        "description": "New description",
        "status": "done"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["status"] == "done"

# Test DELETE /tasks/{id}
def test_delete_task():
    create = client.post("/tasks", json={
        "title": "Task to delete",
        "description": "Will be deleted",
        "status": "todo"
    })
    task_id = create.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404