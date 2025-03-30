from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create a task
@app.post("/tasks/")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(title=task.title, description=task.description, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# ✅ Get all tasks
@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# ✅ Get a single task by ID
@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# ✅ Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed
    db.commit()
    return task

# ✅ Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
