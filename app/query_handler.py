from app.tools import task_tools, calendar_tools, notes_tools
from app.utils import is_task_query, is_event_query, is_note_query, is_today_query


def handle_query(db, message: str):
    text = message.lower()

    if is_task_query(text):
        tasks = task_tools.get_all_tasks(db)

        if is_today_query(text):
            filtered = [
                t for t in tasks
                if t.due_date and "today" in str(t.due_date).lower()
            ]
            if not filtered:
                return {"final_response": "You have no tasks today."}

            lines = ["Your tasks for today:"]
            for task in filtered[:5]:
                lines.append(f"• {task.title}")
            return {"final_response": "\n".join(lines)}

        if not tasks:
            return {"final_response": "You have no tasks yet."}

        lines = ["Your tasks are:"]
        for task in tasks[:5]:
            due = f" (Due: {task.due_date})" if task.due_date else ""
            lines.append(f"• {task.title}{due}")
        return {"final_response": "\n".join(lines)}

    if is_event_query(text):
        events = calendar_tools.get_all_events(db)

        if is_today_query(text):
            filtered = [
                e for e in events
                if e.start_time and "today" in str(e.start_time).lower()
            ]
            if not filtered:
                return {"final_response": "You have no events today."}

            lines = ["Your events for today are:"]
            for event in filtered[:5]:
                lines.append(f"• {event.title} at {event.start_time}")
            return {"final_response": "\n".join(lines)}

        if not events:
            return {"final_response": "You have no events yet."}

        lines = ["Your events are:"]
        for event in events[:5]:
            lines.append(f"• {event.title} at {event.start_time}")
        return {"final_response": "\n".join(lines)}

    if is_note_query(text):
        notes = notes_tools.get_all_notes(db)

        if not notes:
            return {"final_response": "You have no notes yet."}

        lines = ["Your recent notes are:"]
        for note in notes[:5]:
            content = note.content[:60] if note.content else "No content"
            lines.append(f"• {content}")
        return {"final_response": "\n".join(lines)}

    return None