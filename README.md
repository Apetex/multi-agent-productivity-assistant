# Multi-Agent Productivity Assistant

This project is a multi-agent AI system for managing tasks, schedules, and notes. It exposes a FastAPI-based HTTP API and uses SQLAlchemy for storage.

Features included:
- Orchestrator agent coordinating Task, Schedule, and Notes agents
- SQLite (configurable) database with SQLAlchemy models
- Tool adapters for tasks, calendar, and notes
- API endpoints for chat, tasks, events, and notes

Quick start (local, Windows PowerShell):

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

API:
- `POST /chat` - orchestrator chat entry (JSON {"message": "..."})
- `GET /health` - health check

Database: SQLite (assistant.db)

Docker:

Build and run with docker-compose:

```bash
docker compose up --build
```

Development notes:
- The project contains a simple MCP adapter (`app/mcp_adapter.py`) with stubs for integrating external tools.
- See `tests/example_requests.sh` for curl examples.

