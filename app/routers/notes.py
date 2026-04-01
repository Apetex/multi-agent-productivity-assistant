from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import NoteCreate
from app.tools import notes_tools

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/")
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    note = notes_tools.save_note(
        db=db,
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
    )
    return {"message": "Note saved", "note": note}


@router.get("/")
def list_notes(db: Session = Depends(get_db)):
    return {"notes": notes_tools.list_notes(db)}


@router.get("/search")
def search_notes(query: str, db: Session = Depends(get_db)):
    return {"notes": notes_tools.search_notes(db, query)}


@router.get("/summary")
def summarize_notes(db: Session = Depends(get_db)):
    return notes_tools.summarize_notes(db)