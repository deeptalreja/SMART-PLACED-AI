import asyncio
import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.database import async_engine, Base
from app.seed_data import seed_prototype_user
from app.services.readiness_engine import readiness_engine
from app.services.nlp_engine import nlp_analyzer
from app.services.skill_gap_engine import skill_gap_engine
from app.services.interview_engine import interview_engine
from app.services.coding_engine import coding_engine
from app.services.assessment_engine import skill_assessment_engine

FULL_SAMPLE_RESUME = (
    "ALEX CHEN\n"
    "Email: alex.chen@university.edu | Phone: +1-555-0199 | LinkedIn: linkedin.com/in/alexchen-ai | GitHub: github.com/alexchen-ml\n\n"
    "EDUCATION\n"
    "B.Tech in Computer Science & Engineering | VIT Bhopal University | CGPA: 8.8/10.0 | Expected 2025\n\n"
    "TECHNICAL SKILLS\n"
    "Languages: Python, SQL, C++, Bash, HTML, CSS\n"
    "ML/Data Science: Machine Learning, Scikit-learn, Pandas, NumPy, Deep Learning, Matplotlib, Seaborn, Feature Engineering\n"
    "Web & Tools: FastAPI, Git, GitHub, REST APIs, Linux, SQLite\n"
    "Foundations: Data Structures, Algorithms, Dynamic Programming, Database Management (SQL)\n\n"
    "PROJECTS\n"
    "1. Predictive Customer Churn Analytics Platform\n"
    "- Engineered supervised classification models using Scikit-Learn Random Forest and XGBoost.\n"
    "- Addressed class imbalance using SMOTE and evaluated models using Precision-Recall AUC.\n"
    "- Served inference API using FastAPI, handling 150 requests per minute with 92% precision.\n\n"
    "2. Algorithmic Trading Backtester\n"
    "- Implemented quantitative strategy simulator in Python evaluating risk-adjusted Sharpe ratios.\n"
    "- Utilized SQL databases for time-series tick retrieval, improving query execution time by 40%.\n\n"
    "EXPERIENCE\n"
    "Machine Learning Intern | DataCore Solutions (Summer 2024)\n"
    "- Developed automated data validation pipelines using Pandas and Scikit-learn.\n"
    "- Collaborated with senior engineers to implement RESTful endpoints in Python."
)

async def run_tests():
    print("==================================================================")
    print("RUNNING AUTOMATED VERIFICATION SUITE FOR SMART PLACED AI (MVP)")
    print("==================================================================")

    # 1. Test Database Initialization & Table Creation
    print("\n[TEST 1] Initializing SQLite / PostgreSQL Database Tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[PASS] Tables created successfully.")

    # 2. Test Prototype Seed Data (Slide 07 baseline)
    print("\n[TEST 2] Seeding Slide 07 Prototype Baseline User...")
    await seed_prototype_user()
    print("[PASS] Prototype student account seeded (alex.chen@university.edu).")

    # 3. Test Placement Readiness Score Calculation (Exact Slide 07 match)
    print("\n[TEST 3] Testing 9-Dimension Placement Readiness Algorithm...")
    baseline_dims = {
        "python": 85.0,
        "sql": 60.0,
        "ml": 75.0,
        "deep_learning": 45.0,
        "dsa": 55.0,
        "projects": 60.0,
        "resume_quality": 80.0,
        "interview_readiness": 50.0,
        "comm_readiness": 65.0,
    }
    score, tier, priority_actions, diag = readiness_engine.calculate_readiness("AI / ML Engineer", baseline_dims)
    print(f"Calculated Score: {score}/100 | Tier: {tier}")
    assert score == 68.0, f"Expected 68.0 matching Slide 07, got {score}"
    assert len(priority_actions) == 5, f"Expected 5 priority actions (P1-P5), got {len(priority_actions)}"
    assert priority_actions[0]["priority"] == "P1"
    assert "deep_learning" in priority_actions[0]["dimension"]
    print(f"[PASS] Dynamic Placement Readiness Score verified: {score}/100 (Exact match to Slide 07)")
    print(f"[PASS] P1 Action verified: {priority_actions[0]['title']} -> {priority_actions[0]['recommended_action']}")
    print(f"[PASS] P2 Action verified: {priority_actions[1]['title']} -> {priority_actions[1]['recommended_action']}")

    # 4. Test Resume NLP & ATS Scoring
    print("\n[TEST 4] Testing Resume NLP & ESCO Skill Extraction Engine...")
    analysis = nlp_analyzer.evaluate_ats(FULL_SAMPLE_RESUME, "AI / ML Engineer")
    print(f"Extracted Skills count: {len(analysis['extracted_skills'])}")
    print(f"ATS Score: {analysis['ats_score']}/100")
    print(f"Identified Tech Stack Gaps: {analysis['tech_stack_gaps']}")
    assert "Python" in analysis["extracted_skills"]
    assert "Scikit-Learn" in analysis["extracted_skills"]
    assert analysis["ats_score"] >= 70.0
    print("[PASS] Resume extraction and ATS scoring verified.")

    # 5. Test Skill Gap Matrix
    print("\n[TEST 5] Testing Central Skill Gap Matrix Engine...")
    gaps = skill_gap_engine.compute_gap_matrix(
        target_role="AI / ML Engineer",
        resume_skills=analysis["extracted_skills"],
        self_assessed_skills={"Python": "Advanced"},
        leetcode_weak_topics=["Dynamic Programming", "Graphs"],
        dimension_scores=baseline_dims
    )
    print(f"Identified Missing Essential Skills: {gaps['missing_essential_skills']}")
    assert "Docker" in gaps["missing_essential_skills"] or "Mlflow" in gaps["missing_essential_skills"]
    print("[PASS] Skill gap engine correctly detected missing stack (Docker / MLflow).")

    # 6. Test Adaptive Interview Generator & Rubric Scorer
    print("\n[TEST 6] Testing Adaptive Interview Engine & Rubric Scorer...")
    q = interview_engine.generate_question("technical", "AI / ML Engineer")
    print(f"Generated Question: {q['question']}")
    assert "churn" in q["question"].lower() or "imbalance" in q["question"].lower() or "model" in q["question"].lower()

    sample_answer = "We used SMOTE oversampling and focal loss to address the 90:10 imbalance, evaluating with PR-AUC and F1-score rather than raw accuracy."
    eval_out = await interview_engine.evaluate_response(q["question"], sample_answer, "AI / ML Engineer")
    print(f"Rubric Score: {eval_out['score']}/10")
    print(f"Strengths: {eval_out['strengths']}")
    assert eval_out["score"] >= 6.0
    assert "relevance_score" in eval_out
    assert "model_answer" in eval_out
    print("[PASS] Interview rubric evaluation verified.")

    # 7. Test Coding Sandbox Evaluation
    print("\n[TEST 7] Testing Coding Practice Sandbox Runner...")
    prob = coding_engine.get_problem_by_id("coin_change")
    test_code = (
        "def coinChange(coins: list[int], amount: int) -> int:\n"
        "    dp = [float('inf')] * (amount + 1)\n"
        "    dp[0] = 0\n"
        "    for a in range(1, amount + 1):\n"
        "        for c in coins:\n"
        "            if a - c >= 0:\n"
        "                dp[a] = min(dp[a], 1 + dp[a - c])\n"
        "    return dp[amount] if dp[amount] != float('inf') else -1\n"
    )
    code_eval = coding_engine.evaluate_code("coin_change", test_code)
    print(f"Coding Result: {code_eval['status']} ({code_eval['passed_tests']}/{code_eval['total_tests']} tests passed)")
    assert code_eval["status"] == "Accepted"
    assert code_eval["passed_tests"] == code_eval["total_tests"]
    print("[PASS] Coding sandbox runner verified with 100% test pass.")

    # 8. Test AI Skill Assessment 5-Dimension Scoring
    print("\n[TEST 8] Testing AI Skill Assessment 5-Dimension Scoring...")
    sample_answers = {1: 0, 2: 1, 3: 1, 4: 0, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1} # all correct
    assess_eval = skill_assessment_engine.evaluate_answers("AI / ML", sample_answers)
    print(f"Assessment Overall: {assess_eval['overall_score']}% | Band: {assess_eval['proficiency_tier']}")
    print(f"5 Dimensions: {assess_eval['dimension_scores']}")
    assert assess_eval["overall_score"] == 100.0
    assert assess_eval["proficiency_tier"] == "Expert"
    print("[PASS] AI Skill assessment verified across all 5 dimensions.")

    print("\n==================================================================")
    print("ALL 8 VERIFICATION TESTS PASSED SUCCESSFULLY! [100% OK]")
    print("==================================================================")

if __name__ == "__main__":
    asyncio.run(run_tests())
