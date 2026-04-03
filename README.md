# 🤖 Multi-Agent Productivity Assistant

This project is an AI-powered productivity assistant that can **manage tasks, events, and notes** and also **answer natural language queries** like a smart chatbot.

---

## 🚀 Features

* 🧠 Multi-agent system:

  * TaskAgent → create/update tasks
  * ScheduleAgent → manage events
  * NotesAgent → save notes
  * QueryHandler → answer user queries

* 💬 Chat-based interaction:

  * Add tasks, schedule events, save notes
  * Example:

    * "Add a task to prepare resume today"
    * "Schedule interview at 5 PM"
    * "Save note: revise FastAPI"

* 🔍 Query capability:

  * What are my tasks today?
  * What events do I have today?
  * Show my notes

* 🖥️ Dashboard UI (React)

* ⚡ FastAPI backend

* 🗄️ SQLite database

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* Pydantic
* SQLite

### Frontend

* React (Vite)
* CSS

---

## ⚙️ Backend Setup (Windows PowerShell)

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Backend URL:

```
http://localhost:8000
```

---

## 🌐 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```
http://localhost:5173
```

---

## 📡 API Endpoints

* `POST /chat` → Main AI assistant entry
* `GET /health` → Health check
* `/tasks`, `/events`, `/notes` → Data endpoints

---

## 🧪 Example Usage

### Create Task

```json
{
  "message": "Add a task to prepare resume today"
}
```

### Create Event

```json
{
  "message": "Schedule interview today at 5 PM"
}
```

### Save Note

```json
{
  "message": "Save note: revise FastAPI concepts"
}
```

### Query Tasks

```json
{
  "message": "What are my tasks today?"
}
```

---

## 🧠 How It Works

1. User sends message to `/chat`
2. System decides:

   * Action → TaskAgent / ScheduleAgent / NotesAgent
   * Query → QueryHandler
3. Data stored in SQLite database
4. Response returned to frontend UI

---

## 📁 Project Structure

```
app/
 ├── agents/
 ├── routers/
 ├── tools/
 ├── query_handler.py
 ├── models.py
 ├── database.py

frontend/
 ├── src/
 ├── App.jsx
 ├── App.css
```

---

## 🐳 Docker (Optional)

```bash
docker compose up --build
```
