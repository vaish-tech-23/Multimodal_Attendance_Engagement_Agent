import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Application configuration settings."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-multimodal-agent")
    
    # SQLite Database Configuration
    DATABASE_PATH = BASE_DIR / "attendance_engagement.db"
    
    # File Storage Folders
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    REPORT_FOLDER = BASE_DIR / "reports"
    
    # Video & Presence Thresholds (in seconds)
    MIN_SUSTAINED_PRESENCE_SECONDS = 30
    ENGAGEMENT_UPDATE_INTERVAL_SECONDS = 5
    
    # Gemini AI API Configuration (Optional)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
