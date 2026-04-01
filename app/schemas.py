from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: str = "medium"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[str]
    priority: str
    status: str

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    title: str
    start_time: str
    end_time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class EventResponse(BaseModel):
    id: int
    title: str
    start_time: str
    end_time: Optional[str]
    location: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    title: Optional[str] = None
    content: str
    tags: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    title: Optional[str]
    content: str
    tags: Optional[str]

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ActionItem(BaseModel):
    agent: str
    tool: str
    input: Dict[str, Any]


class ChatResponse(BaseModel):
    actions: List[ActionItem]
    final_response: str
    agents_used: List[str]
    execution_results: List[Dict[str, Any]]