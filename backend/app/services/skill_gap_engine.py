from typing import Dict, List, Any
from app.services.nlp_engine import ROLE_BENCHMARKS, ESCO_TAXONOMY

class SkillGapEngine:
    def __init__(self):
        self.role_benchmarks = ROLE_BENCHMARKS

    def compute_gap_matrix(
        self,
        target_role: str,
        resume_skills: List[str],
        self_assessed_skills: Dict[str, str],
        leetcode_weak_topics: List[str],
        dimension_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Derives Gap Matrix = Target Role Requirements - Candidate Profile Signals
        """
        role_info = self.role_benchmarks.get(target_role, self.role_benchmarks["AI / ML Engineer"])
        essential = [s.lower() for s in role_info["essential_skills"]]
        
        # Aggregate all candidate declared/detected skills
        candidate_skills = set(s.lower() for s in resume_skills)
        for s in self_assessed_skills.keys():
            candidate_skills.add(s.lower())

        # Determine missing technical stack
        missing_tech = [s for s in essential if s not in candidate_skills]
        
        # Determine weak competencies based on dimension scores (< 60%)
        weak_competencies = []
        for dim, score in dimension_scores.items():
            if score < 60.0:
                weak_competencies.append({
                    "dimension": dim,
                    "score": score,
                    "status": "Critical Gap" if score < 50.0 else "Needs Improvement"
                })

        # Coding gaps (e.g. Dynamic Programming, Graphs from LeetCode)
        coding_gaps = []
        for topic in leetcode_weak_topics:
            coding_gaps.append({
                "topic": topic,
                "urgency": "High" if topic.lower() in ["dynamic programming", "graphs"] else "Medium",
                "recommended_focus": f"Solve 5 Medium {topic} problems"
            })

        # Formulate industry ready comparison
        coverage_pct = round((len(essential) - len(missing_tech)) / max(1, len(essential)) * 100, 1)

        return {
            "target_role": target_role,
            "skill_coverage_pct": coverage_pct,
            "missing_essential_skills": [s.title() for s in missing_tech],
            "weak_dimensions": weak_competencies,
            "coding_gaps": coding_gaps,
            "identified_tech_stack_gaps": [s.title() for s in missing_tech[:4]],
            "is_placement_ready": coverage_pct >= 75.0 and all(d["score"] >= 60.0 for d in weak_competencies)
        }

skill_gap_engine = SkillGapEngine()
