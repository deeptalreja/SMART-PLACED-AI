from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Dict, List, Any

from app.database import get_db
from app.models import User, StudentProfile, AssessmentLog, ReadinessHistory
from app.auth import get_current_user
from app.services.assessment_engine import skill_assessment_engine
from app.services.readiness_engine import readiness_engine

router = APIRouter(prefix="/assessment", tags=["AI Skill Assessment"])

class AssessmentSubmission(BaseModel):
    track: str = "AI / ML"
    answers: Dict[int, int] # question_id -> chosen option index

@router.get("/questions")
async def get_questions(track: str = "AI / ML"):
    raw_qs = skill_assessment_engine.get_assessment_questions(track)
    # Strip correct answers before returning to frontend
    safe_qs = []
    for q in raw_qs:
        safe_qs.append({
            "id": q["id"],
            "topic": q["topic"],
            "dimension": q["dimension"],
            "question": q["question"],
            "options": q["options"]
        })
    return {"track": track, "total_questions": len(safe_qs), "questions": safe_qs}

@router.post("/submit")
async def submit_assessment(
    payload: AssessmentSubmission,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    eval_res = skill_assessment_engine.evaluate_answers(payload.track, payload.answers)

    # Save to database
    log = AssessmentLog(
        user_id=current_user.id,
        track=payload.track,
        answers_data=payload.answers,
        overall_score=eval_res["overall_score"],
        concept_understanding=eval_res["dimension_scores"].get("Concept Understanding", 50.0),
        problem_solving=eval_res["dimension_scores"].get("Problem Solving", 50.0),
        practical_knowledge=eval_res["dimension_scores"].get("Practical Knowledge", 50.0),
        system_design=eval_res["dimension_scores"].get("System Design", 50.0),
        tech_communication=eval_res["dimension_scores"].get("Technical Communication", 50.0),
        weak_topics=eval_res["weak_topics"],
        strong_topics=eval_res["strong_topics"]
    )
    db.add(log)

    # Closed-loop update into StudentProfile
    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()

    if profile:
        old_readiness = profile.overall_readiness
        # Update ML and DL scores based on assessment performance
        # E.g. Concept & Problem solving map to ML; System Design & Practical map to DL & Python
        profile.ml_score = round(max(profile.ml_score, eval_res["overall_score"] * 0.9 + 10.0), 1)
        profile.deep_learning_score = round(max(profile.deep_learning_score, eval_res["dimension_scores"].get("Practical Knowledge", 45.0) * 0.8 + 15.0), 1)
        
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
            trigger_event=f"Skill Assessment Completed ({payload.track})",
            score_change=score_change
        )
        db.add(history)

    await db.commit()

    return {
        "overall_score": eval_res["overall_score"],
        "dimension_scores": eval_res["dimension_scores"],
        "proficiency_tier": eval_res["proficiency_tier"],
        "weak_topics": eval_res["weak_topics"],
        "strong_topics": eval_res["strong_topics"],
        "correct_answers": eval_res["correct_answers"],
        "total_questions": eval_res["total_questions"],
        "updated_overall_readiness": profile.overall_readiness if profile else eval_res["overall_score"],
        "priority_actions": profile.priority_actions if profile else []
    }
