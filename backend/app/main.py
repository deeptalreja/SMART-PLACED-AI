import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import async_engine, Base
from app.routers import (
    auth_routes,
    dashboard_routes,
    resume_routes,
    assessment_routes,
    interview_routes,
    coding_routes,
    roadmap_routes,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Auto-seed prototype user if database is fresh
    from app.seed_data import seed_prototype_user
    await seed_prototype_user()
    
    yield

app = FastAPI(
    title="SMART PLACED AI - Intelligence Core API",
    description=(
        "Capstone Project Phase 1 · Review 1 · VIT Bhopal University (Course Code DSN4091).\n"
        "AI-Powered Career Intelligence, Placement Readiness & Adaptive Interview Preparation Platform."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for development & React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api/v1
api_prefix = settings.API_V1_STR
app.include_router(auth_routes.router, prefix=api_prefix)
app.include_router(dashboard_routes.router, prefix=api_prefix)
app.include_router(resume_routes.router, prefix=api_prefix)
app.include_router(assessment_routes.router, prefix=api_prefix)
app.include_router(interview_routes.router, prefix=api_prefix)
app.include_router(coding_routes.router, prefix=api_prefix)
app.include_router(roadmap_routes.router, prefix=api_prefix)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "system": settings.PROJECT_NAME,
        "phase": "Phase 1 Core (MVP)",
        "university": "VIT Bhopal University - DSN4091 Review 1"
    }

# Mount React production build if present (enables single-command unified server on port 8000)
dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
assets_dir = os.path.join(dist_dir, "assets")

if os.path.exists(dist_dir):
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api") or full_path.startswith("health") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        file_path = os.path.join(dist_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(dist_dir, "index.html"))
