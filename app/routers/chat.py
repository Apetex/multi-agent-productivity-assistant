from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatRequest
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/chat", tags=["Chat"])
orchestrator = OrchestratorAgent()


@router.post("/")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    return orchestrator.process(db, payload.message)