import re
from typing import Dict, List
from datetime import datetime


def normalize_text(text: str) -> str:
    return text.strip().lower()


def extract_note_content(message: str) -> str:
    patterns = [
        r"save note[:\-]?\s*(.*)",
        r"note[:\-]?\s*(.*)",
        r"remember this[:\-]?\s*(.*)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match and match.group(1).strip():
            return match.group(1).strip()
    return message.strip()


def extract_task_title(message: str) -> str:
    patterns = [
        r"add a task to\s+(.*)",
        r"create a task to\s+(.*)",
        r"add task\s+(.*)",
        r"task[:\-]?\s*(.*)",
        r"remind me to\s+(.*)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match and match.group(1).strip():
            return cleanup_phrase(match.group(1))
    return "New Task"


def extract_event_title(message: str) -> str:
    patterns = [
        r"schedule\s+(?:a\s+)?(.*?)(?:\s+tomorrow|\s+today|\s+on\s+|\s+at\s+|$)",
        r"create (?:an\s+)?event\s+(.*?)(?:\s+tomorrow|\s+today|\s+on\s+|\s+at\s+|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match and match.group(1).strip():
            return cleanup_phrase(match.group(1)).title()
    if "meeting" in message.lower():
        return "Meeting"
    if "interview" in message.lower():
        return "Interview"
    if "appointment" in message.lower():
        return "Appointment"
    return "New Event"


def extract_time_phrase(message: str) -> str:
    patterns = [
        r"(today(?:\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?)?)",
        r"(tomorrow(?:\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?)?)",
        r"((?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)(?:\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?)?)",
        r"(on\s+[A-Za-z0-9,\s]+\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?)",
        r"(at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm))",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "unspecified"


def detect_intents(message: str) -> List[str]:
    text = normalize_text(message)
    intents = []

    task_keywords = ["task", "todo", "remind", "reminder", "complete task", "finish", "submit"]
    schedule_keywords = ["schedule", "meeting", "appointment", "calendar", "event", "reschedule", "interview"]
    notes_keywords = ["note", "save", "remember this", "notes", "write down"]

    if any(word in text for word in task_keywords):
        intents.append("task")
    if any(word in text for word in schedule_keywords):
        intents.append("schedule")
    if any(word in text for word in notes_keywords):
        intents.append("notes")

    return list(dict.fromkeys(intents))


def cleanup_phrase(text: str) -> str:
    text = re.sub(r"\band\b.*$", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"\s+", " ", text).strip(" .,:;-")
    return text


def build_orchestrator_output(message: str) -> Dict:
    intents = detect_intents(message)
    actions = []
    agents_used = []

    if "schedule" in intents:
        action = {
            "agent": "ScheduleAgent",
            "tool": "create_event" if any(k in message.lower() for k in ["schedule", "meeting", "appointment", "interview", "event"]) else "list_events",
            "input": {
                "title": extract_event_title(message),
                "start_time": extract_time_phrase(message),
                "end_time": None,
                "location": None,
                "description": message.strip(),
            },
        }
        actions.append(action)
        agents_used.append("ScheduleAgent")

    if "task" in intents:
        due_date = None
        if "before" in message.lower():
            due_date = "before event"
        else:
            time_phrase = extract_time_phrase(message)
            due_date = time_phrase if time_phrase != "unspecified" else None

        action = {
            "agent": "TaskAgent",
            "tool": "create_task" if any(k in message.lower() for k in ["add", "create", "remind", "task", "todo"]) else "list_tasks",
            "input": {
                "title": extract_task_title(message).title(),
                "description": message.strip(),
                "due_date": due_date,
                "priority": "medium",
            },
        }
        actions.append(action)
        agents_used.append("TaskAgent")

    if "notes" in intents:
        action = {
            "agent": "NotesAgent",
            "tool": "save_note" if any(k in message.lower() for k in ["save", "note", "remember this", "write down"]) else "list_notes",
            "input": {
                "title": "Quick Note",
                "content": extract_note_content(message),
                "tags": None,
            },
        }
        actions.append(action)
        agents_used.append("NotesAgent")

    if not actions:
        actions.append(
            {
                "agent": "NotesAgent",
                "tool": "save_note",
                "input": {
                    "title": "General Note",
                    "content": message.strip(),
                    "tags": "general",
                },
            }
        )
        agents_used.append("NotesAgent")

    final_response = build_human_response(actions)

    return {
        "actions": actions,
        "final_response": final_response,
        "agents_used": list(dict.fromkeys(agents_used)),
    }


def build_human_response(actions: List[Dict]) -> str:
    messages = []
    for action in actions:
        tool = action["tool"]
        data = action["input"]

        if tool == "create_event":
            messages.append(f"{data.get('title', 'Event')} scheduled for {data.get('start_time', 'unspecified time')}")
        elif tool == "create_task":
            messages.append(f"task '{data.get('title', 'New Task')}' added")
        elif tool == "save_note":
            messages.append("note saved")
        elif tool == "list_tasks":
            messages.append("fetched tasks")
        elif tool == "list_events":
            messages.append("fetched events")
        elif tool == "list_notes":
            messages.append("fetched notes")

    if not messages:
        return "Request processed."

    return ". ".join(messages).capitalize() + "."


def is_task_query(message: str) -> bool:
    text = message.lower()
    return "task" in text and any(word in text for word in ["what", "show", "list", "today"])


def is_event_query(message: str) -> bool:
    text = message.lower()
    return any(word in text for word in ["event", "meeting", "schedule"]) and any(
        word in text for word in ["what", "show", "list", "today"]
    )


def is_note_query(message: str) -> bool:
    text = message.lower()
    return "note" in text and any(word in text for word in ["what", "show", "list"])


def is_today_query(message: str) -> bool:
    return "today" in message.lower()

def is_task_query(message: str) -> bool:
    text = message.lower()
    return (
        "task" in text and any(word in text for word in ["what", "show", "list"])
    ) or ("what are my tasks" in text)


def is_event_query(message: str) -> bool:
    text = message.lower()
    return (
        any(word in text for word in ["event", "events", "meeting", "meetings"])
        and any(word in text for word in ["what", "show", "list"])
    ) or ("what events" in text)


def is_note_query(message: str) -> bool:
    text = message.lower()
    return "note" in text and any(word in text for word in ["what", "show", "list"])
    
    
def is_today_query(message: str) -> bool:
    return "today" in message.lower()