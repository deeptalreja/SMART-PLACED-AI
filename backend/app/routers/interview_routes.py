from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models import User, StudentProfile, InterviewSession, ReadinessHistory
from app.auth import get_current_user
from app.services.interview_engine import interview_engine
from app.services.readiness_engine import readiness_engine

router = APIRouter(prefix="/interview", tags=["Adaptive Interview Intelligence"])

class QuestionRequest(BaseModel):
    interview_type: str = "technical" # "technical" or "hr"

class EvaluationRequest(BaseModel):
    session_id: int
    student_response: str

@router.post("/generate-question")
async def generate_interview_question(
    req: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()
    target_role = profile.target_role if profile else current_user.target_role

    q_data = interview_engine.generate_question(
        interview_type=req.interview_type,
        target_role=target_role
    )

    session = InterviewSession(
        user_id=current_user.id,
        interview_type=req.interview_type,
        target_role=target_role,
        question=q_data["question"],
        context_source=q_data["context_source"]
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return {
        "session_id": session.id,
        "interview_type": req.interview_type,
        "target_role": target_role,
        "question": session.question,
        "context_source": session.context_source
    }

@router.post("/evaluate")
async def evaluate_interview_response(
    req: EvaluationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(InterviewSession).where(InterviewSession.id == req.session_id, InterviewSession.user_id == current_user.id)
    res = await db.execute(stmt)
    session = res.scalars().first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found."
        )

    eval_result = await interview_engine.evaluate_response(
        question=session.question,
        student_response=req.student_response,
        target_role=session.target_role
    )

    # Update session record
    session.student_response = req.student_response
    session.score = eval_result["score"]
    session.relevance_score = eval_result["relevance_score"]
    session.structure_score = eval_result["structure_score"]
    session.correctness_score = eval_result["correctness_score"]
    session.depth_score = eval_result["depth_score"]
    session.strengths = eval_result["strengths"]
    session.improvements = eval_result["improvements"]
    session.model_answer = eval_result["model_answer"]

    # Closed-loop update to StudentProfile
    stmt_prof = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res_prof = await db.execute(stmt_prof)
    profile = res_prof.scalars().first()

    if profile:
        old_readiness = profile.overall_readiness
        # Scale 0-10 interview score to 0-100 and blend
        new_interview_score = round(min(100.0, profile.interview_readiness_score * 0.4 + (eval_result["score"] * 10.0) * 0.6), 1)
        new_comm_score = round(min(100.0, profile.comm_readiness_score * 0.5 + (eval_result["structure_score"] * 10.0) * 0.5), 1)
        
        profile.interview_readiness_score = new_interview_score
        profile.comm_readiness_score = new_comm_score

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
            trigger_event=f"Interview Evaluated ({session.interview_type.upper()})",
            score_change=score_change
        )
        db.add(history)

    await db.commit()

    return {
        "session_id": session.id,
        "score": eval_result["score"],
        "relevance_score": eval_result["relevance_score"],
        "structure_score": eval_result["structure_score"],
        "correctness_score": eval_result["correctness_score"],
        "depth_score": eval_result["depth_score"],
        "strengths": eval_result["strengths"],
        "improvements": eval_result["improvements"],
        "model_answer": eval_result["model_answer"],
        "updated_interview_readiness": profile.interview_readiness_score if profile else 60.0,
        "updated_overall_readiness": profile.overall_readiness if profile else 70.0,
        "priority_actions": profile.priority_actions if profile else []
    }
