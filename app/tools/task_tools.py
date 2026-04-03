from sqlalchemy.orm import Session
from app import models


def create_task(db: Session, title: str, description: str = None, due_date: str = None, priority: str = "medium"):
    task = models.Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        status="pending",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session):
    return db.query(models.Task).order_by(models.Task.created_at.desc()).all()


def update_task(db: Session, task_id: int, fields: dict):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None

    for key, value in fields.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def complete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None

    task.status = "completed"
    db.commit()
    db.refresh(task)
    return task

def get_all_tasks(db: Session):
    return db.query(models.Task).order_by(models.Task.created_at.desc()).all()