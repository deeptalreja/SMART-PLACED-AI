import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import User, StudentProfile, ReadinessHistory
from app.schemas import UserRegister, UserLogin, Token
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.services.readiness_engine import readiness_engine

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    stmt = select(User).where(User.email == user_in.email)
    res = await db.execute(stmt)
    existing_user = res.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # Create User
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        target_role=user_in.target_role or "AI / ML Engineer"
    )
    db.add(new_user)
    await db.flush()

    # Slide 07 baseline dimensions for AI / ML Engineer:
    # Python 85%, SQL 60%, ML 75%, DL 45%, DSA 55%, Projects 60%, Resume 80%, Interview 50%, Communication 65%
    initial_dims = {
        "python": 85.0,
        "sql": 60.0,
        "ml": 75.0,
        "deep_learning": 45.0,
        "dsa": 55.0,
        "projects": 60.0,
        "resume_quality": 80.0,
        "interview_readiness": 50.0,
        "comm_readiness": 65.0
    }
    
    overall, tier, priority_actions, _ = readiness_engine.calculate_readiness(
        new_user.target_role, initial_dims
    )

    profile = StudentProfile(
        user_id=new_user.id,
        target_role=new_user.target_role,
        python_score=initial_dims["python"],
        sql_score=initial_dims["sql"],
        ml_score=initial_dims["ml"],
        deep_learning_score=initial_dims["deep_learning"],
        dsa_score=initial_dims["dsa"],
        projects_score=initial_dims["projects"],
        resume_quality_score=initial_dims["resume_quality"],
        interview_readiness_score=initial_dims["interview_readiness"],
        comm_readiness_score=initial_dims["comm_readiness"],
        overall_readiness=overall,
        readiness_tier=tier,
        priority_actions=priority_actions
    )
    db.add(profile)
    await db.flush()

    # Log initial readiness history
    history = ReadinessHistory(
        user_id=new_user.id,
        overall_readiness=overall,
        dimension_scores=initial_dims,
        trigger_event="Account Registration Baseline",
        score_change=0.0
    )
    db.add(history)
    await db.commit()

    token = create_access_token({"sub": new_user.email, "user_id": new_user.id})
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=new_user.id,
        full_name=new_user.full_name,
        target_role=new_user.target_role
    )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == form_data.username)
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        full_name=user.full_name,
        target_role=user.target_role
    )

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "target_role": current_user.target_role
    }
