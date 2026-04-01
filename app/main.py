from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_NAME
from app.database import Base, engine
from app.routers import chat, tasks, events, notes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description="Multi-Agent Productivity Assistant API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {
        "message": APP_NAME,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}