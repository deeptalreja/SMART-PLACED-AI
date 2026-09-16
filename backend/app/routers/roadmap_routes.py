from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import User, StudentProfile
from app.auth import get_current_user
from app.services.roadmap_engine import roadmap_engine
from app.services.recommendation_engine import recommendation_engine

router = APIRouter(tags=["Roadmap & Recommendations"])

@router.get("/roadmap")
async def get_roadmap(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()

    target_role = profile.target_role if profile else current_user.target_role
    dims = {
        "deep_learning": profile.deep_learning_score if profile else 45.0,
        "dsa": profile.dsa_score if profile else 55.0,
        "overall_readiness": profile.overall_readiness if profile else 68.0
    }

    return roadmap_engine.get_roadmap(target_role, dims)

@router.get("/recommendations")
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()

    target_role = profile.target_role if profile else current_user.target_role
    weak_topics = profile.leetcode_weak_topics if profile and profile.leetcode_weak_topics else ["Dynamic Programming"]

    projects = recommendation_engine.get_project_recommendations(target_role, ["Docker", "MLflow", "FastAPI"])
    coding = recommendation_engine.get_coding_recommendations(target_role, weak_topics)

    return {
        "target_role": target_role,
        "recommended_projects": projects,
        "recommended_coding_challenges": coding
    }
