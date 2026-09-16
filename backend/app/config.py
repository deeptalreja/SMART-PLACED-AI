import os
from typing import Dict, List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SMART PLACED AI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "smart_placed_ai_super_secret_jwt_key_capstone_2025")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database: Default to SQLite for zero-config plug-and-play, supports PostgreSQL via env
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./smart_placed_ai.db")
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL", "sqlite:///./smart_placed_ai.db")
    
    # External LLM configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini") # gemini, openai, or local_heuristic
    
    # Available Career Roles
    SUPPORTED_ROLES: List[str] = [
        "AI / ML Engineer",
        "Full Stack Developer",
        "Cloud / DevOps Engineer"
    ]
    
    # Configurable weights across the NINE TRACKED DIMENSIONS per Target Role (Slide 07 & Slide 10)
    # Dimensions: [python, sql, ml, deep_learning, dsa, projects, resume_quality, interview_readiness, comm_readiness]
    ROLE_DIMENSION_WEIGHTS: Dict[str, Dict[str, float]] = {
        "AI / ML Engineer": {
            "python": 0.14,
            "sql": 0.05,
            "ml": 0.18,
            "deep_learning": 0.16,
            "dsa": 0.14,
            "projects": 0.11,
            "resume_quality": 0.10,
            "interview_readiness": 0.08,
            "comm_readiness": 0.04,
        },
        "Full Stack Developer": {
            "python": 0.08,
            "sql": 0.12,
            "ml": 0.02,
            "deep_learning": 0.00,
            "dsa": 0.18,
            "projects": 0.20,
            "resume_quality": 0.12,
            "interview_readiness": 0.14,
            "comm_readiness": 0.14,
        },
        "Cloud / DevOps Engineer": {
            "python": 0.12,
            "sql": 0.08,
            "ml": 0.04,
            "deep_learning": 0.02,
            "dsa": 0.12,
            "projects": 0.18,
            "resume_quality": 0.12,
            "interview_readiness": 0.16,
            "comm_readiness": 0.16,
        }
    }

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
