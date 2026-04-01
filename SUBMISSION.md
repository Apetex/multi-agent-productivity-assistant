# Hackathon Submission Notes

Project: Multi-Agent Productivity Assistant

What to run:

1. Local (recommended for judging):

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

2. Docker (recommended for consistent environment):

```bash
docker compose up --build
```

Description of features delivered:
- Orchestrator agent coordinating TaskAgent, ScheduleAgent, and NotesAgent.
- Local MCP adapter stubs to simulate integrations with calendar, task stores, and notes.
- SQLite-backed persistence with SQLAlchemy models and migrations handled on startup.
- API endpoints for chat orchestration and direct resource access.
- Basic tests and CI workflow.

How to evaluate:
- Hit `POST /chat` with natural language prompts (see `tests/example_requests.sh`).
- Check `/health` for service status.

Optional improvements (not required for submission):
- Integrate real external tools (Google Calendar, Trello, etc.).
- Add LLM-based planner to replace `utils.build_orchestrator_output`.
