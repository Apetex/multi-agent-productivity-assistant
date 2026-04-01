from sqlalchemy.orm import Session
from app import models


def save_note(db: Session, content: str, title: str = None, tags: str = None):
    note = models.Note(title=title, content=content, tags=tags)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db: Session):
    return db.query(models.Note).order_by(models.Note.created_at.desc()).all()


def search_notes(db: Session, query: str):
    return db.query(models.Note).filter(models.Note.content.ilike(f"%{query}%")).all()


def summarize_notes(db: Session):
    notes = db.query(models.Note).order_by(models.Note.created_at.desc()).all()
    return {
        "count": len(notes),
        "titles": [note.title for note in notes if note.title],
    }