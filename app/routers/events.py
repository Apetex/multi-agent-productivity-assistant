from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import EventCreate
from app.tools import calendar_tools

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/")
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = calendar_tools.create_event(
        db=db,
        title=payload.title,
        start_time=payload.start_time,
        end_time=payload.end_time,
        location=payload.location,
        description=payload.description,
    )
    return {"message": "Event created", "event": event}


@router.get("/")
def list_events(db: Session = Depends(get_db)):
    return {"events": calendar_tools.list_events(db)}


@router.put("/{event_id}/reschedule")
def reschedule_event(event_id: int, new_time: str, db: Session = Depends(get_db)):
    event = calendar_tools.reschedule_event(db, event_id, new_time)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event rescheduled", "event": event}