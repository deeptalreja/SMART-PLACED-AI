from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.database import get_db
from app.models import User, StudentProfile, ReadinessHistory, CodingSubmission, InterviewSession, AssessmentLog
from app.auth import get_current_user
from app.services.readiness_engine import readiness_engine
from app.config import settings

router = APIRouter(prefix="/dashboard", tags=["Student Dashboard"])

class TargetRoleUpdate(BaseModel):
    target_role: str

@router.get("/overview")
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fetch profile
    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()

    if not profile:
        # Fallback create if somehow missing
        profile = StudentProfile(user_id=current_user.id, target_role=current_user.target_role)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    dims = {
        "python": profile.python_score,
        "sql": profile.sql_score,
        "ml": profile.ml_score,
        "deep_learning": profile.deep_learning_score,
        "dsa": profile.dsa_score,
        "projects": profile.projects_score,
        "resume_quality": profile.resume_quality_score,
        "interview_readiness": profile.interview_readiness_score,
        "comm_readiness": profile.comm_readiness_score,
    }

    overall, tier, priority_actions, diagnostics = readiness_engine.calculate_readiness(
        profile.target_role, dims
    )

    # Fetch counts
    assess_res = await db.execute(select(AssessmentLog).where(AssessmentLog.user_id == current_user.id))
    assessments_count = len(assess_res.scalars().all())

    coding_res = await db.execute(select(CodingSubmission).where(CodingSubmission.user_id == current_user.id))
    coding_count = len(coding_res.scalars().all())

    interview_res = await db.execute(select(InterviewSession).where(InterviewSession.user_id == current_user.id))
    interview_count = len(interview_res.scalars().all())

    # Fetch history
    history_res = await db.execute(
        select(ReadinessHistory).where(ReadinessHistory.user_id == current_user.id).order_by(ReadinessHistory.timestamp.asc())
    )
    history_records = history_res.scalars().all()
    history_data = [
        {
            "timestamp": h.timestamp.isoformat(),
            "overall_readiness": h.overall_readiness,
            "trigger_event": h.trigger_event,
            "score_change": h.score_change
        }
        for h in history_records
    ]

    return {
        "user_id": current_user.id,
        "full_name": current_user.full_name,
        "target_role": profile.target_role,
        "supported_roles": settings.SUPPORTED_ROLES,
        "overall_readiness": overall,
        "readiness_tier": tier,
        "dimension_scores": dims,
        "priority_actions": priority_actions,
        "diagnostics": diagnostics,
        "readiness_history": history_data,
        "leetcode_stats": {
            "url": profile.leetcode_url,
            "total_solved": profile.leetcode_total_solved,
            "medium_solved": profile.leetcode_medium_solved,
            "weak_topics": profile.leetcode_weak_topics or ["Dynamic Programming", "Graphs", "Trie"]
        },
        "portfolio_links": {
            "github": profile.github_url,
            "linkedin": profile.linkedin_url
        },
        "self_assessed_skills": profile.self_assessed_skills,
        "quick_stats": {
            "assessments_completed": assessments_count,
            "coding_challenges_solved": coding_count,
            "interviews_evaluated": interview_count
        }
    }

@router.post("/set-role")
async def set_target_role(
    role_in: TargetRoleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if role_in.target_role not in settings.SUPPORTED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Target role must be one of {settings.SUPPORTED_ROLES}"
        )

    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()

    if profile:
        profile.target_role = role_in.target_role
        dims = {
            "python": profile.python_score,
            "sql": profile.sql_score,
            "ml": profile.ml_score,
            "deep_learning": profile.deep_learning_score,
            "dsa": profile.dsa_score,
            "projects": profile.projects_score,
            "resume_quality": profile.resume_quality_score,
            "interview_readiness": profile.interview_readiness_score,
            "comm_readiness": profile.comm_readiness_score,
        }
        overall, tier, priority_actions, _ = readiness_engine.calculate_readiness(
            role_in.target_role, dims
        )
        profile.overall_readiness = overall
        profile.readiness_tier = tier
        profile.priority_actions = priority_actions

    current_user.target_role = role_in.target_role
    await db.commit()

    return {"message": "Target role updated", "target_role": role_in.target_role}
