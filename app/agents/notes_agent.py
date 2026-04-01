from sqlalchemy.orm import Session
from app.tools import notes_tools


class NotesAgent:
    name = "NotesAgent"

    def execute(self, db: Session, tool: str, data: dict):
        if tool == "save_note":
            note = notes_tools.save_note(
                db=db,
                title=data.get("title"),
                content=data.get("content"),
                tags=data.get("tags"),
            )
            return {"agent": self.name, "tool": tool, "result": {"id": note.id, "title": note.title}}

        if tool == "list_notes":
            notes = notes_tools.list_notes(db)
            return {
                "agent": self.name,
                "tool": tool,
                "result": [{"id": n.id, "title": n.title, "content": n.content} for n in notes],
            }

        if tool == "search_notes":
            notes = notes_tools.search_notes(db, data.get("query", ""))
            return {
                "agent": self.name,
                "tool": tool,
                "result": [{"id": n.id, "title": n.title, "content": n.content} for n in notes],
            }

        if tool == "summarize_notes":
            summary = notes_tools.summarize_notes(db)
            return {"agent": self.name, "tool": tool, "result": summary}

        return {"agent": self.name, "tool": tool, "error": "Unsupported notes tool"}