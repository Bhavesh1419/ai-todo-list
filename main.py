from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, Task  # Import database models

app = FastAPI()

# Serve static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI To-Do List!"}

# Get all tasks
@app.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# Add a new task
@app.post("/add-task/")
def add_task(description: str, db: Session = Depends(get_db)):
    new_task = Task(description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added!", "task": new_task}
