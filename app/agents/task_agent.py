from sqlalchemy.orm import Session
from app.tools import task_tools


class TaskAgent:
    name = "TaskAgent"

    def execute(self, db: Session, tool: str, data: dict):
        if tool == "create_task":
            task = task_tools.create_task(
                db=db,
                title=data.get("title"),
                description=data.get("description"),
                due_date=data.get("due_date"),
                priority=data.get("priority", "medium"),
            )
            return {"agent": self.name, "tool": tool, "result": {"id": task.id, "title": task.title}}

        if tool == "list_tasks":
            tasks = task_tools.list_tasks(db)
            return {
                "agent": self.name,
                "tool": tool,
                "result": [{"id": t.id, "title": t.title, "status": t.status} for t in tasks],
            }

        if tool == "complete_task":
            task = task_tools.complete_task(db, data["id"])
            return {
                "agent": self.name,
                "tool": tool,
                "result": None if task is None else {"id": task.id, "status": task.status},
            }

        if tool == "update_task":
            task = task_tools.update_task(db, data["id"], data.get("fields", {}))
            return {
                "agent": self.name,
                "tool": tool,
                "result": None if task is None else {"id": task.id, "title": task.title},
            }

        return {"agent": self.name, "tool": tool, "error": "Unsupported task tool"}