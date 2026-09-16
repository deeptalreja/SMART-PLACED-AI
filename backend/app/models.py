import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    target_role = Column(String(100), default="AI / ML Engineer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="user", uselist=False)
    resumes = relationship("ResumeAnalysis", back_populates="user")
    assessments = relationship("AssessmentLog", back_populates="user")
    interviews = relationship("InterviewSession", back_populates="user")
    coding_submissions = relationship("CodingSubmission", back_populates="user")
    readiness_history = relationship("ReadinessHistory", back_populates="user")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    target_role = Column(String(100), default="AI / ML Engineer")
    
    # The Nine Tracked Dimensions (0-100) (Slide 07)
    python_score = Column(Float, default=85.0)
    sql_score = Column(Float, default=60.0)
    ml_score = Column(Float, default=75.0)
    deep_learning_score = Column(Float, default=45.0)
    dsa_score = Column(Float, default=55.0)
    projects_score = Column(Float, default=60.0)
    resume_quality_score = Column(Float, default=80.0)
    interview_readiness_score = Column(Float, default=50.0)
    comm_readiness_score = Column(Float, default=65.0)

    # Dynamic Placement Readiness Score (0-100)
    overall_readiness = Column(Float, default=68.0)
    readiness_tier = Column(String(50), default="Advanced") # Beginner, Intermediate, Advanced, Expert
    
    # External Integrations (Slide 05, Slide 11)
    leetcode_url = Column(String(255), default="https://leetcode.com/u/student_prototype")
    leetcode_total_solved = Column(Integer, default=142)
    leetcode_medium_solved = Column(Integer, default=68)
    leetcode_weak_topics = Column(JSON, default=lambda: ["Dynamic Programming", "Graphs", "Trie"])
    
    github_url = Column(String(255), default="https://github.com/student_prototype")
    linkedin_url = Column(String(255), default="https://linkedin.com/in/student_prototype")
    
    # Validated self-assessed skills
    self_assessed_skills = Column(JSON, default=lambda: {
        "Python": "Advanced",
        "FastAPI": "Intermediate",
        "SQL": "Intermediate",
        "PyTorch": "Beginner",
        "Docker": "Beginner"
    })
    
    # Generated Priority Actions & Next Best Action
    priority_actions = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_filename = Column(String(255), default="resume.pdf")
    parsed_text = Column(Text, nullable=True)
    ats_score = Column(Float, default=78.0) # 0-100 visual gauge
    formatting_score = Column(Float, default=85.0)
    keyword_score = Column(Float, default=72.0)
    extracted_skills = Column(JSON, default=list)
    matched_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    tech_stack_gaps = Column(JSON, default=list) # e.g. ["Docker", "MLflow"]
    suggestions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="resumes")


class AssessmentLog(Base):
    __tablename__ = "assessment_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    track = Column(String(100), default="AI / ML") # Cloud, Full Stack, AI / ML
    questions_data = Column(JSON, default=list)
    answers_data = Column(JSON, default=dict)
    overall_score = Column(Float, default=0.0)
    
    # 5 Evaluation Dimensions (from SVG diagram)
    concept_understanding = Column(Float, default=0.0)
    problem_solving = Column(Float, default=0.0)
    practical_knowledge = Column(Float, default=0.0)
    system_design = Column(Float, default=0.0)
    tech_communication = Column(Float, default=0.0)
    
    weak_topics = Column(JSON, default=list)
    strong_topics = Column(JSON, default=list)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="assessments")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interview_type = Column(String(50), default="technical") # "technical" or "hr"
    target_role = Column(String(100), default="AI / ML Engineer")
    question = Column(Text, nullable=False)
    context_source = Column(String(255), default="Resume ML Project & DL Gap")
    student_response = Column(Text, nullable=True)
    
    # Rubric-anchored evaluation
    score = Column(Float, default=0.0) # 0-10 or 0-100
    relevance_score = Column(Float, default=0.0)
    structure_score = Column(Float, default=0.0)
    correctness_score = Column(Float, default=0.0)
    depth_score = Column(Float, default=0.0)
    
    strengths = Column(Text, nullable=True)
    improvements = Column(Text, nullable=True)
    model_answer = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="interviews")


class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(String(100), nullable=False)
    problem_title = Column(String(255), nullable=False)
    topic = Column(String(100), default="Dynamic Programming")
    code = Column(Text, nullable=False)
    passed_tests = Column(Integer, default=0)
    total_tests = Column(Integer, default=0)
    status = Column(String(50), default="Accepted") # Accepted, Wrong Answer, Runtime Error
    score = Column(Float, default=100.0)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="coding_submissions")


class ReadinessHistory(Base):
    __tablename__ = "readiness_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    overall_readiness = Column(Float, nullable=False)
    dimension_scores = Column(JSON, nullable=False)
    trigger_event = Column(String(100), default="initial_assessment")
    score_change = Column(Float, default=0.0)

    user = relationship("User", back_populates="readiness_history")
