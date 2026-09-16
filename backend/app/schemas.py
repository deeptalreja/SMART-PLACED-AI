from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field
import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    target_role: Optional[str] = "AI / ML Engineer"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    target_role: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Dimension & Readiness Schemas ---
class DimensionScores(BaseModel):
    python: float = Field(..., ge=0, le=100)
    sql: float = Field(..., ge=0, le=100)
    ml: float = Field(..., ge=0, le=100)
    deep_learning: float = Field(..., ge=0, le=100)
    dsa: float = Field(..., ge=0, le=100)
    projects: float = Field(..., ge=0, le=100)
    resume_quality: float = Field(..., ge=0, le=100)
    interview_readiness: float = Field(..., ge=0, le=100)
    comm_readiness: float = Field(..., ge=0, le=100)

class PriorityAction(BaseModel):
    priority: str # P1, P2, P3, P4, P5
    title: str
    description: str
    dimension: str
    current_score: float
    recommended_action: str
    action_type: str # "course", "practice", "project", "resume", "interview"

class DashboardOverview(BaseModel):
    user_id: int
    full_name: str
    target_role: str
    overall_readiness: float
    readiness_tier: str
    dimension_scores: DimensionScores
    priority_actions: List[PriorityAction]
    readiness_history: List[Dict[str, Any]]
    leetcode_stats: Dict[str, Any]
    quick_stats: Dict[str, Any]

# --- Resume Schemas ---
class ResumeAnalysisResponse(BaseModel):
    id: int
    original_filename: str
    ats_score: float
    formatting_score: float
    keyword_score: float
    extracted_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    tech_stack_gaps: List[str]
    achievement_metric_gaps: List[str]
    suggestions: List[str]
    target_role: str

# --- Assessment Schemas ---
class AssessmentQuestion(BaseModel):
    id: int
    track: str
    topic: str
    dimension: str
    question: str
    options: List[str]

class AssessmentSubmitRequest(BaseModel):
    track: str
    answers: Dict[int, int] # question_id -> chosen option index

class AssessmentResultResponse(BaseModel):
    overall_score: float
    dimension_scores: Dict[str, float]
    proficiency_tier: str
    weak_topics: List[str]
    strong_topics: List[str]
    updated_readiness_score: float
    new_priority_actions: List[PriorityAction]

# --- Interview Schemas ---
class InterviewQuestionRequest(BaseModel):
    interview_type: str = "technical" # technical or hr
    target_role: Optional[str] = None
    focus_topic: Optional[str] = None

class InterviewQuestionResponse(BaseModel):
    session_id: int
    interview_type: str
    target_role: str
    question: str
    context_source: str

class InterviewEvaluateRequest(BaseModel):
    session_id: int
    student_response: str

class InterviewEvaluationResponse(BaseModel):
    session_id: int
    score: float # 0 - 10
    relevance_score: float
    structure_score: float
    correctness_score: float
    depth_score: float
    strengths: str
    improvements: str
    model_answer: str
    updated_interview_readiness: float
    updated_overall_readiness: float

# --- Coding Practice Schemas ---
class CodingProblem(BaseModel):
    id: str
    title: str
    difficulty: str
    topic: str
    description: str
    starter_code: str
    test_cases: List[Dict[str, Any]]

class CodingSubmitRequest(BaseModel):
    problem_id: str
    code: str

class CodingSubmitResponse(BaseModel):
    problem_id: str
    status: str
    passed_tests: int
    total_tests: int
    score: float
    feedback: str
    updated_dsa_readiness: float
    updated_overall_readiness: float

# --- Roadmap Schemas ---
class RoadmapNode(BaseModel):
    stage: int
    title: str
    subtitle: str
    skills: List[Dict[str, Any]] # {"name": "React", "completed": True}
    status: str # "completed", "in_progress", "locked"
    description: str

class RoadmapResponse(BaseModel):
    target_role: str
    current_stage: int
    stage_name: str
    nodes: List[RoadmapNode]
    recommended_next_steps: List[str]
