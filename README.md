# Task Manager API

A session-based REST API for managing tasks, built with Python and FastAPI. Each visitor gets their own private task list — no login required. Live demo available.

🔗 **Live Demo:** https://task-manager-api-32z1.onrender.com
📁 **GitHub:** https://github.com/hgnirk1/task-manager-api

---

## Features

-  5 REST API endpoints (GET, POST, PUT, DELETE)
-  Session-based multi-user isolation (each visitor sees only their own tasks)
-  Persistent SQLite storage via SQLAlchemy ORM
-  Interactive frontend UI
-  6 automated pytest tests covering all endpoints
-  Dockerized for containerization
-  CI/CD pipeline via GitHub Actions
-  Deployed to Render

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## Project Structure

task-manager-api/
├── app/
│   ├── init.py
│   ├── main.py        # API endpoints
│   ├── models.py      # Database models
│   ├── schemas.py     # Pydantic schemas
│   ├── database.py    # Database connection
│   └── static/
│       └── index.html # Frontend UI
├── tests/
│   └── test_tasks.py  # Pytest test suite
├── .github/
│   └── workflows/
│       └── ci.yml     # GitHub Actions pipeline
├── Dockerfile
├── requirements.txt
└── README.md

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks?session_id=` | Get all tasks for a session |
| GET | `/tasks/{id}?session_id=` | Get a single task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}?session_id=` | Update a task by ID |
| DELETE | `/tasks/{id}?session_id=` | Delete a task by ID |

### Example Request

```bash
curl -X POST https://task-manager-api-32z1.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs", "status": "todo", "session_id": "my_session"}'
```

### Example Response

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk and eggs",
  "status": "todo",
  "session_id": "my_session",
  "created_at": "2026-04-17T23:34:49"
}
```

---

## Running Locally

### Prerequisites
- Python 3.11+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hgnirk1/task-manager-api.git
cd task-manager-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

5. Open your browser and go to: http://127.0.0.1:8000

---

## Running with Docker

```bash
docker build -t task-manager-api .
docker run -p 8000:8000 task-manager-api
```

---

## Running Tests

```bash
pytest tests/ -v
```

Expected output:

tests/test_tasks.py::test_get_tasks_empty PASSED
tests/test_tasks.py::test_create_task PASSED
tests/test_tasks.py::test_get_task PASSED
tests/test_tasks.py::test_update_task PASSED
tests/test_tasks.py::test_delete_task PASSED
tests/test_tasks.py::test_session_isolation PASSED
6 passed in 0.42s

---

## CI/CD Pipeline

Every push to `main` triggers a GitHub Actions workflow that:
1. Sets up Python 3.11
2. Installs dependencies
3. Runs the full pytest test suite

---

## Author

Haley — [github.com/hgnirk1](https://github.com/hgnirk1)