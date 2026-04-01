import json
from google import genai

SYSTEM_PROMPT = """
You are a Multi-Agent Productivity Assistant.

Return ONLY valid JSON in this format:
{
  "actions": [
    {
      "agent": "TaskAgent | ScheduleAgent | NotesAgent",
      "tool": "create_task | list_tasks | create_event | list_events | save_note | list_notes",
      "input": {}
    }
  ],
  "final_response": "short human summary",
  "agents_used": ["TaskAgent"]
}

Rules:
- If user asks to create a task, use TaskAgent + create_task
- If user asks to schedule/create a meeting/event, use ScheduleAgent + create_event
- If user asks to save a note, use NotesAgent + save_note
- If the request has multiple parts, return multiple actions
- Output JSON only, no markdown
"""

client = genai.Client()

def build_plan_with_gemini(user_message: str) -> dict:
    prompt = f"""
System instructions:
{SYSTEM_PROMPT}

User message:
{user_message}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)