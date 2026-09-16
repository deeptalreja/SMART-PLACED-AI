from typing import Dict, List, Any

ROADMAPS_BY_ROLE: Dict[str, List[Dict[str, Any]]] = {
    "AI / ML Engineer": [
        {
            "stage": 1,
            "title": "Programming & Data Fundamentals",
            "subtitle": "Get the Basics Right",
            "description": "Build clean, object-oriented code, data structures, and algorithmic complexity in Python.",
            "skills": [
                {"name": "Python 3 OOP & Iterators", "completed": True},
                {"name": "Data Structures & Complexity", "completed": True},
                {"name": "Git & GitHub Version Control", "completed": True}
            ]
        },
        {
            "stage": 2,
            "title": "Data Manipulation & Analytics",
            "subtitle": "Master the Data Pipeline",
            "description": "Perform robust data wrangling, exploratory analysis, and relational querying.",
            "skills": [
                {"name": "NumPy & Matrix Operations", "completed": True},
                {"name": "Pandas Data Wrangling", "completed": True},
                {"name": "SQL Joins & Grouping", "completed": True}
            ]
        },
        {
            "stage": 3,
            "title": "Classical Machine Learning",
            "subtitle": "Learn Predictive Modeling",
            "description": "Supervised, unsupervised algorithms, cross-validation, and ROC/PR metric evaluations.",
            "skills": [
                {"name": "Scikit-Learn Pipeline Design", "completed": True},
                {"name": "Feature Engineering & Imputation", "completed": True},
                {"name": "Classification & Regression Metrics", "completed": True}
            ]
        },
        {
            "stage": 4,
            "title": "Deep Learning & Neural Architectures",
            "subtitle": "Tackle Complex Representations",
            "description": "Master gradient descent backprop, PyTorch tensors, CNNs, and sequence models.",
            "skills": [
                {"name": "PyTorch Fundamentals & Autograd", "completed": False},
                {"name": "Convolutional & Attention Networks", "completed": False},
                {"name": "Hyperparameter Optimization & Regularization", "completed": False}
            ]
        },
        {
            "stage": 5,
            "title": "Modern NLP & Embeddings",
            "subtitle": "Harness Semantic AI",
            "description": "Sentence transformers, cosine vector similarity, HuggingFace tokenizers, and RAG pipelines.",
            "skills": [
                {"name": "Sentence-Transformers & Embeddings", "completed": False},
                {"name": "Vector Stores & RAG Architectures", "completed": False},
                {"name": "LLM Prompting & Rubric Scoring", "completed": True}
            ]
        },
        {
            "stage": 6,
            "title": "API Serving & Containerization",
            "subtitle": "Turn Models into Microservices",
            "description": "Build high-throughput REST APIs and bundle production inference into Docker images.",
            "skills": [
                {"name": "FastAPI Async Endpoints", "completed": True},
                {"name": "Docker Container Packaging", "completed": False},
                {"name": "Pydantic Request Validation", "completed": True}
            ]
        },
        {
            "stage": 7,
            "title": "MLOps & Experiment Tracking",
            "subtitle": "Automate the Lifecycle",
            "description": "Track parameters and model artifacts with MLflow, CI/CD automated validation.",
            "skills": [
                {"name": "MLflow Experiment Tracking", "completed": False},
                {"name": "GitHub Actions CI/CD Testing", "completed": False},
                {"name": "Model Registry & Versioning", "completed": False}
            ]
        },
        {
            "stage": 8,
            "title": "Production AI & System Design",
            "subtitle": "Scale to Placement Ready",
            "description": "Low-latency inference, caching, distributed training, and production interview mastery.",
            "skills": [
                {"name": "End-to-End System Design", "completed": False},
                {"name": "Interview Technical Defense", "completed": False},
                {"name": "Scalable Model Serving", "completed": False}
            ]
        }
    ],
    "Full Stack Developer": [
        {
            "stage": 1,
            "title": "Programming Fundamentals",
            "subtitle": "Get the Basics Right",
            "description": "Build the foundation for web development.",
            "skills": [
                {"name": "HTML5 Semantic Elements", "completed": True},
                {"name": "Modern CSS & Flexbox/Grid", "completed": True},
                {"name": "JavaScript ES6+ Fundamentals", "completed": True}
            ]
        },
        {
            "stage": 2,
            "title": "Frontend Development",
            "subtitle": "Build Beautiful UIs",
            "description": "Create dynamic and responsive web applications.",
            "skills": [
                {"name": "React Components & Hooks", "completed": True},
                {"name": "Tailwind CSS Styling", "completed": True},
                {"name": "State Management & Context API", "completed": False}
            ]
        },
        {
            "stage": 3,
            "title": "Backend Development",
            "subtitle": "Power the Logic",
            "description": "Build server-side applications and handle business logic.",
            "skills": [
                {"name": "Python FastAPI / Node Express", "completed": True},
                {"name": "RESTful API Design", "completed": True},
                {"name": "Data Serialization & Pydantic", "completed": True}
            ]
        },
        {
            "stage": 4,
            "title": "Database",
            "subtitle": "Store and Manage Data",
            "description": "Work with databases to store and retrieve data efficiently.",
            "skills": [
                {"name": "PostgreSQL & Relational Design", "completed": True},
                {"name": "Indexing & Query Optimization", "completed": False},
                {"name": "ORM / SQLAlchemy Integration", "completed": True}
            ]
        },
        {
            "stage": 5,
            "title": "Authentication & Security",
            "subtitle": "Keep It Safe",
            "description": "Secure your application and manage user access.",
            "skills": [
                {"name": "JWT (JSON Web Token)", "completed": True},
                {"name": "Password Hashing & Salt", "completed": True},
                {"name": "Role-Based Access Control", "completed": False}
            ]
        },
        {
            "stage": 6,
            "title": "APIs & Integration",
            "subtitle": "Connect Everything",
            "description": "Enable communication between frontend, backend and third-party services.",
            "skills": [
                {"name": "RESTful Client Integration", "completed": True},
                {"name": "API Testing with Postman/cURL", "completed": True},
                {"name": "CORS & Security Headers", "completed": True}
            ]
        },
        {
            "stage": 7,
            "title": "DevOps & Deployment",
            "subtitle": "Take It Live",
            "description": "Deploy your application and manage the lifecycle.",
            "skills": [
                {"name": "Git & GitHub Workflows", "completed": True},
                {"name": "Docker Containerization", "completed": False},
                {"name": "Cloud Deployment (AWS/Render)", "completed": False}
            ]
        },
        {
            "stage": 8,
            "title": "Advanced & System Design",
            "subtitle": "Level Up & Placement Ready",
            "description": "Build scalable and high-performance applications.",
            "skills": [
                {"name": "System Design Fundamentals", "completed": False},
                {"name": "Microservices Architecture", "completed": False},
                {"name": "CI/CD Deployment Pipelines", "completed": False}
            ]
        }
    ]
}

class RoadmapEngine:
    def get_roadmap(self, target_role: str, dimension_scores: Dict[str, float]) -> Dict[str, Any]:
        stages = ROADMAPS_BY_ROLE.get(target_role, ROADMAPS_BY_ROLE["AI / ML Engineer"])
        
        # Determine current stage based on dimension scores
        # E.g. If Deep Learning < 50%, student is at Stage 4
        dl_score = dimension_scores.get("deep_learning", 45.0)
        dsa_score = dimension_scores.get("dsa", 55.0)
        overall_ready = dimension_scores.get("overall_readiness", 68.0)
        
        current_stage = 4
        if dl_score >= 70.0 and dsa_score >= 70.0:
            current_stage = 6
        elif dl_score >= 80.0 and dsa_score >= 80.0:
            current_stage = 7

        processed_nodes = []
        for stage_data in stages:
            st_num = stage_data["stage"]
            if st_num < current_stage:
                status = "completed"
            elif st_num == current_stage:
                status = "in_progress"
            else:
                status = "locked"

            processed_nodes.append({
                "stage": st_num,
                "title": stage_data["title"],
                "subtitle": stage_data["subtitle"],
                "description": stage_data["description"],
                "skills": stage_data["skills"],
                "status": status
            })

        # Generate recommended next steps
        curr_node = processed_nodes[current_stage - 1]
        next_steps = [s["name"] for s in curr_node["skills"] if not s["completed"]]
        if not next_steps:
            next_steps = ["Review advanced system design questions", "Complete full mock interview"]

        return {
            "target_role": target_role,
            "current_stage": current_stage,
            "stage_name": curr_node["title"],
            "nodes": processed_nodes,
            "recommended_next_steps": next_steps
        }

roadmap_engine = RoadmapEngine()
