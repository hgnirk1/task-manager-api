from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db

# Create all database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A session-based REST API for managing tasks.",
    version="1.0.0"
)

# Serve static files (frontend UI)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    """Serve the frontend UI."""
    return FileResponse("app/static/index.html")

@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(session_id: str, db: Session = Depends(get_db)):
    """Retrieve all tasks belonging to a specific session."""
    return db.query(models.Task).filter(models.Task.session_id == session_id).all()

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, session_id: str, db: Session = Depends(get_db)):
    """Retrieve a single task by ID, scoped to the session."""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.session_id == session_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task and save it to the database."""
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, session_id: str, updated: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task by ID, scoped to the session."""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.session_id == session_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated.model_dump().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session_id: str, db: Session = Depends(get_db)):
    """Delete a task by ID, scoped to the session."""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.session_id == session_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()