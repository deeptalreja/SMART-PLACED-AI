from typing import Dict, List, Any

class RecommendationEngine:
    def get_project_recommendations(self, target_role: str, tech_stack_gaps: List[str]) -> List[Dict[str, Any]]:
        """Generates actionable portfolio projects specifically tailored to close detected tech stack gaps."""
        projects = []
        if target_role == "AI / ML Engineer":
            projects.append({
                "id": "proj_ml_pipeline",
                "title": "End-to-End ML Pipeline with FastAPI & Docker",
                "difficulty": "Advanced",
                "target_gaps_addressed": ["Docker", "FastAPI", "MLflow", "ML Deployment"],
                "description": "Develop and containerize a high-performance machine learning inference API. Track training runs and hyperparameters with MLflow, package the application in a multi-stage Docker container, and expose REST endpoints with Pydantic validation.",
                "deliverables": [
                    "Data preprocessing & model training pipeline",
                    "MLflow experiment logging script",
                    "FastAPI prediction endpoints with automated OpenAPI docs",
                    "Production Dockerfile with health check probes"
                ],
                "github_template_prompt": "Template structure: /src, /models, Dockerfile, requirements.txt, test_api.py"
            })
            projects.append({
                "id": "proj_rag_eval",
                "title": "RAG-Powered Technical Document Search with Sentence-Transformers",
                "difficulty": "Intermediate-Advanced",
                "target_gaps_addressed": ["Embeddings", "Deep Learning", "Vector Search", "Transformers"],
                "description": "Build a semantic document retrieval system using pre-trained sentence transformer embeddings and cosine similarity to index and answer queries over technical documentation.",
                "deliverables": [
                    "Document chunking and embedding generator",
                    "FAISS / in-memory vector index",
                    "Prompt template with strict grounding against hallucination"
                ],
                "github_template_prompt": "Embeddings script, vector store loader, query pipeline"
            })
        elif target_role == "Full Stack Developer":
            projects.append({
                "id": "proj_fullstack_dashboard",
                "title": "Real-time Collaborative Analytics Dashboard",
                "difficulty": "Advanced",
                "target_gaps_addressed": ["React", "PostgreSQL", "JWT Auth", "Docker"],
                "description": "Architect a full-stack edtech/career platform featuring interactive KPI charts, PostgreSQL database schema with indexing, and JWT authentication.",
                "deliverables": [
                    "React + Tailwind frontend with component architecture",
                    "FastAPI / Node backend with transactional database operations",
                    "Docker compose environment"
                ],
                "github_template_prompt": "Fullstack monorepo with client and server folders"
            })
        else:
            projects.append({
                "id": "proj_devops_iac",
                "title": "Automated Cloud Infrastructure with Terraform & GitHub Actions",
                "difficulty": "Advanced",
                "target_gaps_addressed": ["Terraform", "CI/CD", "Docker", "AWS"],
                "description": "Deploy containerized services to cloud infrastructure with automated CI/CD validation on every pull request.",
                "deliverables": [
                    "Terraform HCL manifests",
                    "GitHub Actions workflow pipeline",
                    "Docker container image push to registry"
                ],
                "github_template_prompt": ".github/workflows/deploy.yml, main.tf, Dockerfile"
            })
            
        return projects

    def get_coding_recommendations(self, target_role: str, weak_topics: List[str]) -> List[Dict[str, Any]]:
        """Generates targeted coding practice sets prioritizing weakest algorithmic topics."""
        questions = []
        # Prioritize Dynamic Programming and Trees if identified
        if any("dynamic programming" in t.lower() or "dp" in t.lower() for t in weak_topics):
            questions.extend([
                {
                    "title": "Coin Change (Min Coins to make amount)",
                    "difficulty": "Medium",
                    "topic": "Dynamic Programming",
                    "problem_id": "coin_change",
                    "pattern": "Unbounded Knapsack / Bottom-Up DP",
                    "link": "https://leetcode.com/problems/coin-change/",
                    "time_complexity": "O(amount * n)",
                    "space_complexity": "O(amount)"
                },
                {
                    "title": "Longest Increasing Subsequence",
                    "difficulty": "Medium",
                    "topic": "Dynamic Programming",
                    "problem_id": "lis",
                    "pattern": "1D DP or Patience Sorting (Binary Search)",
                    "link": "https://leetcode.com/problems/longest-increasing-subsequence/",
                    "time_complexity": "O(n^2) or O(n log n)",
                    "space_complexity": "O(n)"
                },
                {
                    "title": "Unique Paths in a Grid",
                    "difficulty": "Medium",
                    "topic": "Dynamic Programming",
                    "problem_id": "unique_paths",
                    "pattern": "2D Grid DP",
                    "link": "https://leetcode.com/problems/unique-paths/",
                    "time_complexity": "O(m * n)",
                    "space_complexity": "O(n)"
                }
            ])

        questions.extend([
            {
                "title": "Lowest Common Ancestor of a Binary Tree",
                "difficulty": "Medium",
                "topic": "Trees & Graphs",
                "problem_id": "lca_tree",
                "pattern": "Depth-First Search (DFS) Post-Order",
                "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
                "time_complexity": "O(n)",
                "space_complexity": "O(h)"
            },
            {
                "title": "Two Sum II - Input Array Is Sorted",
                "difficulty": "Medium",
                "topic": "Two Pointers",
                "problem_id": "two_sum_sorted",
                "pattern": "Two Pointer Inward Scan",
                "link": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)"
            }
        ])

        return questions

recommendation_engine = RecommendationEngine()
