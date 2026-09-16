from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.database import get_db
from app.models import User, StudentProfile, CodingSubmission, ReadinessHistory
from app.auth import get_current_user
from app.services.coding_engine import coding_engine
from app.services.readiness_engine import readiness_engine

router = APIRouter(prefix="/coding", tags=["Coding Practice & Evaluation"])

class CodeSubmissionRequest(BaseModel):
    problem_id: str
    code: str

@router.get("/problems")
async def get_problems():
    return {"problems": coding_engine.get_problems()}

@router.post("/submit")
async def submit_code(
    payload: CodeSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    problem = coding_engine.get_problem_by_id(payload.problem_id)
    eval_res = coding_engine.evaluate_code(payload.problem_id, payload.code)

    submission = CodingSubmission(
        user_id=current_user.id,
        problem_id=payload.problem_id,
        problem_title=problem["title"],
        topic=problem.get("topic", "DSA"),
        code=payload.code,
        passed_tests=eval_res["passed_tests"],
        total_tests=eval_res["total_tests"],
        status=eval_res["status"],
        score=eval_res["score"]
    )
    db.add(submission)

    # Closed-loop update: If tests passed, raise DSA readiness score!
    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()

    if profile:
        old_readiness = profile.overall_readiness
        if eval_res["passed_tests"] > 0:
            # Boost DSA score proportionally
            gain = (eval_res["passed_tests"] / eval_res["total_tests"]) * 12.0
            profile.dsa_score = round(min(100.0, profile.dsa_score + gain), 1)

            # If problem is dynamic programming, remove from weak topics if previously marked
            if "dynamic programming" in problem.get("topic", "").lower():
                current_weaks = list(profile.leetcode_weak_topics or [])
                if "Dynamic Programming" in current_weaks:
                    current_weaks.remove("Dynamic Programming")
                    profile.leetcode_weak_topics = current_weaks

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
                profile.target_role, dims
            )
            profile.overall_readiness = overall
            profile.readiness_tier = tier
            profile.priority_actions = priority_actions

            score_change = round(overall - old_readiness, 1)
            history = ReadinessHistory(
                user_id=current_user.id,
                overall_readiness=overall,
                dimension_scores=dims,
                trigger_event=f"Solved Coding Challenge: {problem['title']}",
                score_change=score_change
            )
            db.add(history)

    await db.commit()

    return {
        "problem_id": payload.problem_id,
        "status": eval_res["status"],
        "passed_tests": eval_res["passed_tests"],
        "total_tests": eval_res["total_tests"],
        "score": eval_res["score"],
        "feedback": eval_res["feedback"],
        "updated_dsa_readiness": profile.dsa_score if profile else 55.0,
        "updated_overall_readiness": profile.overall_readiness if profile else 68.0,
        "priority_actions": profile.priority_actions if profile else []
    }
