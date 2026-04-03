from sqlalchemy.orm import Session
from app import models


def create_event(
    db: Session,
    title: str,
    start_time: str,
    end_time: str = None,
    location: str = None,
    description: str = None,
):
    event = models.Event(
        title=title,
        start_time=start_time,
        end_time=end_time,
        location=location,
        description=description,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_events(db: Session):
    return db.query(models.Event).order_by(models.Event.created_at.desc()).all()


def reschedule_event(db: Session, event_id: int, new_time: str):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        return None

    event.start_time = new_time
    db.commit()
    db.refresh(event)
    return event


def check_conflicts(db: Session, start_time: str):
    return db.query(models.Event).filter(models.Event.start_time == start_time).all()

def get_all_events(db: Session):
    return db.query(models.Event).order_by(models.Event.created_at.desc()).all()