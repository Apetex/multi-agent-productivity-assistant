"""Simple MCP adapter and connector stubs for calendar, tasks, and notes.

These are lightweight wrappers that the orchestrator can call instead
of real external MCP integrations. Replace with real connectors for production.
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.tools import calendar_tools, task_tools, notes_tools


class MCPAdapter:
    def __init__(self, db: Session):
        self.db = db

    def call(self, tool_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # route to local tool implementations
        if tool_name == "calendar.create_event":
            ev = calendar_tools.create_event(
                db=self.db,
                title=data.get("title"),
                start_time=data.get("start_time"),
                end_time=data.get("end_time"),
                location=data.get("location"),
                description=data.get("description"),
            )
            return {"id": ev.id, "title": ev.title}

        if tool_name == "tasks.create_task":
            t = task_tools.create_task(
                db=self.db,
                title=data.get("title"),
                description=data.get("description"),
                due_date=data.get("due_date"),
                priority=data.get("priority", "medium"),
            )
            return {"id": t.id, "title": t.title}

        if tool_name == "notes.save_note":
            n = notes_tools.save_note(
                db=self.db, title=data.get("title"), content=data.get("content"), tags=data.get("tags")
            )
            return {"id": n.id}

        # fallback: unsupported
        return {"error": "unsupported_tool", "tool": tool_name}


def create_adapter(db: Session) -> MCPAdapter:
    return MCPAdapter(db)
