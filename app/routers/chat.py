from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatRequest
from app.agents.orchestrator import OrchestratorAgent
from app.query_handler import handle_query

router = APIRouter(prefix="/chat", tags=["Chat"])
orchestrator = OrchestratorAgent()


@router.post("/")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):

    # 🔹 Step 1: Check if it's a query (today tasks, events, notes)
    query_result = handle_query(db, payload.message)

    if query_result:
        return {
            "actions": [],
            "final_response": query_result["final_response"],
            "agents_used": ["QueryHandler"],
            "execution_results": [],
        }

    # 🔹 Step 2: Otherwise use normal AI agents
    return orchestrator.process(db, payload.message)