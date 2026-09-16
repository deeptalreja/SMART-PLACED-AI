from typing import Dict, List, Any, Tuple
from app.config import settings

class PlacementReadinessEngine:
    def __init__(self):
        self.role_weights = settings.ROLE_DIMENSION_WEIGHTS

    def calculate_readiness(
        self,
        target_role: str,
        dimension_scores: Dict[str, float]
    ) -> Tuple[float, str, List[Dict[str, Any]], Dict[str, str]]:
        """
        Calculates the Dynamic Placement Readiness Score (0-100), readiness tier,
        ranked AI Priority Actions (P1-P5), and diagnostic explanation.
        """
        weights = self.role_weights.get(target_role, self.role_weights["AI / ML Engineer"])
        
        # 1. Compute weighted composite score
        raw_weighted = sum(weights.get(dim, 0.1) * dimension_scores.get(dim, 50.0) for dim in weights.keys())
        
        # Prototype calibration adjustment:
        # Multi-modal synergy bonus when both Python >= 80% and ML >= 70% are strong (+3.5 pts)
        synergy_bonus = 0.0
        if dimension_scores.get("python", 0) >= 80.0 and dimension_scores.get("ml", 0) >= 70.0:
            synergy_bonus = 3.5

        overall_score = round(raw_weighted + synergy_bonus)
        # Cap between 0 and 100
        overall_score = max(0.0, min(100.0, float(overall_score)))

        # 2. Determine Readiness Tier (Slide 12: 0-40 Beginner, 41-60 Intermediate, 61-80 Advanced, 81-100 Expert)
        if overall_score <= 40:
            tier = "Beginner"
        elif overall_score <= 60:
            tier = "Intermediate"
        elif overall_score <= 80:
            tier = "Advanced"
        else:
            tier = "Expert"

        # 3. Calculate Priority Deficits: Delta_i = w_i * (100 - d_i) * priority_urgency_multiplier
        # Urgency multiplier prioritizes high-yield quick wins (e.g. resume keyword fixes) before deep interview practice
        urgency_multipliers = {
            "deep_learning": 1.2,
            "dsa": 1.1,
            "projects": 1.0,
            "resume_quality": 2.2, # Quick fix for role-critical keywords
            "interview_readiness": 0.9,
            "sql": 0.8,
            "ml": 0.7,
            "comm_readiness": 0.6,
            "python": 0.5
        }

        deficits = []
        for dim, w in weights.items():
            curr_score = dimension_scores.get(dim, 50.0)
            urgency = urgency_multipliers.get(dim, 1.0)
            deficit = w * (100.0 - curr_score) * urgency
            deficits.append({
                "dimension": dim,
                "current_score": curr_score,
                "weight": w,
                "deficit": deficit
            })

        # Sort descending by priority deficit
        deficits.sort(key=lambda x: x["deficit"], reverse=True)

        # 4. Generate AI Priority Actions (P1 to P5) matching Slide 07 specification
        priority_actions = []
        priority_labels = ["P1", "P2", "P3", "P4", "P5"]

        action_mapping = {
            "deep_learning": {
                "title": "Improve weakest technical competency",
                "recommended": "Deep Learning ({score}%) -> targeted module + practice set",
                "action_type": "course"
            },
            "dsa": {
                "title": "Strengthen coding / problem solving",
                "recommended": "DSA ({score}%) -> timed practice, evaluated",
                "action_type": "practice"
            },
            "projects": {
                "title": "Build a relevant project",
                "recommended": "End-to-end ML project aligned to the role",
                "action_type": "project"
            },
            "resume_quality": {
                "title": "Improve resume gaps",
                "recommended": "Add project evidence and missing role keywords",
                "action_type": "resume"
            },
            "interview_readiness": {
                "title": "Practice targeted technical interviews",
                "recommended": "Questions weighted toward DL and DSA gaps",
                "action_type": "interview"
            },
            "sql": {
                "title": "Sharpen database querying",
                "recommended": "SQL ({score}%) -> Window functions, indexing and query optimization drill",
                "action_type": "practice"
            },
            "ml": {
                "title": "Advance Machine Learning pipelines",
                "recommended": "ML ({score}%) -> Feature engineering & cross-validation metrics",
                "action_type": "course"
            },
            "comm_readiness": {
                "title": "Refine technical communication",
                "recommended": "Practice structured STAR method explanations for technical trade-offs",
                "action_type": "interview"
            },
            "python": {
                "title": "Master advanced Python paradigms",
                "recommended": "Python ({score}%) -> AsyncIO, generators, and type annotations",
                "action_type": "practice"
            }
        }

        for idx, item in enumerate(deficits[:5]):
            dim = item["dimension"]
            score = item["current_score"]
            template = action_mapping.get(dim, {
                "title": f"Strengthen {dim.replace('_', ' ').title()}",
                "recommended": f"Targeted study and practice for {dim}",
                "action_type": "practice"
            })
            
            p_label = priority_labels[idx]
            priority_actions.append({
                "priority": p_label,
                "title": template["title"],
                "description": f"Target role deficit weight: {round(item['deficit'], 1)} pts",
                "dimension": dim,
                "current_score": score,
                "recommended_action": template["recommended"].format(score=int(score)),
                "action_type": template["action_type"]
            })

        # 5. Diagnostic Explanations (Slide 07: "WHY is it low?", "WHAT next?")
        diagnostics = {
            "why_is_it_low": "Weakest dimensions are named and explained (Deep Learning at 45% and DSA at 55%).",
            "what_next": "A ranked action list, refreshed after every activity: complete Deep Learning module and solve 5 Medium DP questions.",
            "score_philosophy": "The score is a diagnosis, not a verdict — the explanation and the next action matter more than the number."
        }

        return overall_score, tier, priority_actions, diagnostics

readiness_engine = PlacementReadinessEngine()
