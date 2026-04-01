import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Multi-Agent Productivity Assistant")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./assistant.db")