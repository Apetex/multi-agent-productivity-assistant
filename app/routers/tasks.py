from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate
from app.tools import task_tools

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = task_tools.create_task(
        db=db,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        priority=payload.priority,
    )
    return {"message": "Task created", "task": task}


@router.get("/")
def list_tasks(db: Session = Depends(get_db)):
    return {"tasks": task_tools.list_tasks(db)}


@router.put("/{task_id}")
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    updated = task_tools.update_task(db, task_id, payload.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated", "task": updated}


@router.put("/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_tools.complete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task completed", "task": task}