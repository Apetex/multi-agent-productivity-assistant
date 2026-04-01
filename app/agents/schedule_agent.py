from sqlalchemy.orm import Session
from app.tools import calendar_tools


class ScheduleAgent:
    name = "ScheduleAgent"

    def execute(self, db: Session, tool: str, data: dict):
        if tool == "create_event":
            conflicts = calendar_tools.check_conflicts(db, data.get("start_time"))
            if conflicts:
                return {
                    "agent": self.name,
                    "tool": tool,
                    "warning": "Time conflict detected",
                    "conflicts": [{"id": e.id, "title": e.title, "start_time": e.start_time} for e in conflicts],
                }

            event = calendar_tools.create_event(
                db=db,
                title=data.get("title"),
                start_time=data.get("start_time"),
                end_time=data.get("end_time"),
                location=data.get("location"),
                description=data.get("description"),
            )
            return {"agent": self.name, "tool": tool, "result": {"id": event.id, "title": event.title}}

        if tool == "list_events":
            events = calendar_tools.list_events(db)
            return {
                "agent": self.name,
                "tool": tool,
                "result": [{"id": e.id, "title": e.title, "start_time": e.start_time} for e in events],
            }

        if tool == "reschedule_event":
            event = calendar_tools.reschedule_event(db, data["id"], data["new_time"])
            return {
                "agent": self.name,
                "tool": tool,
                "result": None if event is None else {"id": event.id, "start_time": event.start_time},
            }

        if tool == "check_conflicts":
            conflicts = calendar_tools.check_conflicts(db, data["start_time"])
            return {
                "agent": self.name,
                "tool": tool,
                "result": [{"id": e.id, "title": e.title, "start_time": e.start_time} for e in conflicts],
            }

        return {"agent": self.name, "tool": tool, "error": "Unsupported schedule tool"}