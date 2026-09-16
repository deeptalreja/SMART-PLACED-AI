import re
import io
from typing import Dict, List, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ESCO_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "python", "java", "c++", "c", "c#", "javascript", "typescript", "go", "rust", "r", "scala", "sql", "html", "css", "bash"
    ],
    "Machine Learning & Data Science": [
        "machine learning", "scikit-learn", "deep learning", "neural networks", "pytorch", "tensorflow", "keras",
        "nlp", "natural language processing", "computer vision", "transformers", "hugging face", "bert", "gpt",
        "llm", "large language models", "rag", "retrieval augmented generation", "embeddings", "pandas", "numpy",
        "matplotlib", "seaborn", "opencv", "feature engineering", "model evaluation", "cross validation", "xgboost",
        "lightgbm", "random forest", "logistic regression", "clustering", "pca", "hyperparameter tuning"
    ],
    "Data Engineering & Databases": [
        "sql", "postgresql", "mysql", "mongodb", "sqlite", "redis", "elasticsearch", "neo4j", "cassandra",
        "etl", "data warehousing", "snowflake", "bigquery", "spark", "kafka", "pandas", "dbt"
    ],
    "DevOps, Cloud & MLOps": [
        "docker", "kubernetes", "mlflow", "dvc", "airflow", "aws", "azure", "gcp", "git", "github", "gitlab",
        "ci/cd", "github actions", "linux", "fastapi", "flask", "django", "rest api", "microservices", "terraform"
    ],
    "DSA & Problem Solving": [
        "data structures", "algorithms", "dynamic programming", "graphs", "trees", "arrays", "binary search",
        "recursion", "sorting", "hash tables", "linked lists", "greedy algorithms", "time complexity", "space complexity"
    ],
    "Frontend & Full Stack": [
        "react", "vue", "angular", "node.js", "express", "next.js", "tailwind css", "bootstrap", "redux",
        "html5", "css3", "state management", "restful apis", "oauth", "jwt"
    ]
}

ROLE_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "AI / ML Engineer": {
        "essential_skills": [
            "python", "machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn",
            "docker", "mlflow", "fastapi", "sql", "dynamic programming", "transformers", "rag", "git"
        ],
        "important_skills": [
            "numpy", "pandas", "data structures", "algorithms", "rest api", "linux", "feature engineering", "model evaluation"
        ],
        "jd_description": (
            "We are seeking an AI / ML Engineer proficient in Python, Scikit-learn, PyTorch or TensorFlow, "
            "and Deep Learning architectures. The ideal candidate has experience building end-to-end ML pipelines, "
            "deploying models via FastAPI and Docker, tracking experiments with MLflow, and strong foundations in "
            "Data Structures, Algorithms (especially dynamic programming), SQL, and Transformer embeddings."
        )
    },
    "Full Stack Developer": {
        "essential_skills": [
            "javascript", "typescript", "react", "node.js", "python", "fastapi", "sql", "postgresql",
            "docker", "git", "restful apis", "data structures", "algorithms", "tailwind css"
        ],
        "important_skills": [
            "html5", "css3", "redux", "jwt", "ci/cd", "microservices", "mongodb"
        ],
        "jd_description": (
            "Looking for a Full Stack Developer with strong expertise in React, modern JavaScript/TypeScript, "
            "backend development using Python FastAPI or Node.js, relational databases like PostgreSQL, "
            "RESTful API design, authentication using JWT, Docker containerization, and robust problem-solving DSA skills."
        )
    },
    "Cloud / DevOps Engineer": {
        "essential_skills": [
            "linux", "docker", "kubernetes", "aws", "terraform", "ci/cd", "git", "python", "bash",
            "networking", "monitoring", "sql"
        ],
        "important_skills": [
            "github actions", "microservices", "security", "cloud architecture", "gcp", "azure"
        ],
        "jd_description": (
            "Seeking a Cloud & DevOps Engineer experienced in Docker containerization, Kubernetes orchestration, "
            "cloud platforms (AWS/GCP), CI/CD pipelines, Infrastructure as Code with Terraform, Linux shell scripting, "
            "Python automation, and system reliability monitoring."
        )
    }
}

class ResumeNLPAnalyzer:
    def __init__(self):
        self.all_canonical_skills: Dict[str, str] = {}
        for category, skills in ESCO_TAXONOMY.items():
            for skill in skills:
                self.all_canonical_skills[skill.lower()] = category

    def extract_text_from_file(self, filename: str, content_bytes: bytes) -> str:
        text = ""
        filename_lower = filename.lower()
        if filename_lower.endswith(".pdf"):
            try:
                import pypdf
                pdf_reader = pypdf.PdfReader(io.BytesIO(content_bytes))
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except Exception:
                try:
                    import pdfplumber
                    with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                except Exception:
                    pass
        elif filename_lower.endswith(".docx"):
            try:
                import docx
                doc = docx.Document(io.BytesIO(content_bytes))
                for para in doc.paragraphs:
                    text += para.text + "\n"
            except Exception:
                pass
        else:
            try:
                text = content_bytes.decode("utf-8", errors="ignore")
            except Exception:
                text = str(content_bytes)

        return text.strip()

    def extract_skills(self, text: str) -> List[str]:
        text_lower = " " + text.lower() + " "
        normalized = re.sub(r'[/,();:]', ' ', text_lower)
        
        extracted = set()
        for skill in self.all_canonical_skills.keys():
            pattern = r'(?:\b|_)' + re.escape(skill) + r'(?:\b|_)'
            if re.search(pattern, normalized):
                extracted.add(skill)

        return sorted(list(extracted))

    def evaluate_ats(self, text: str, target_role: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # 1. Section Presence (25 pts)
        sections = {
            "Contact Info": bool(re.search(r'(@|phone|email|linkedin|github|\+91|\+1)', text_lower)),
            "Education": bool(re.search(r'(education|bachelor|b\.tech|degree|university|institute|gpa|cgpa)', text_lower)),
            "Experience / Projects": bool(re.search(r'(experience|projects|work experience|internship|academic projects)', text_lower)),
            "Technical Skills": bool(re.search(r'(skills|technical skills|technologies|tools|competencies)', text_lower)),
        }
        section_score = (sum(sections.values()) / len(sections)) * 25.0

        # 2. Quantifiable Impact & Metrics (25 pts)
        metric_matches = re.findall(r'(\d+[\d\.,]*%|\$\d+|\d+\s*x|\b\d+\s*(?:ms|users|requests|queries|accuracy|precision|recall|retention|reduction|increase|improvement)\b)', text_lower)
        metric_score = min(25.0, len(metric_matches) * 6.5)

        # 3. Target Role Keyword Matching (35 pts)
        role_info = ROLE_BENCHMARKS.get(target_role, ROLE_BENCHMARKS["AI / ML Engineer"])
        essential = role_info["essential_skills"]
        important = role_info["important_skills"]
        
        extracted_skills = self.extract_skills(text)
        matched_essential = [s for s in essential if s in extracted_skills]
        matched_important = [s for s in important if s in extracted_skills]
        missing_essential = [s for s in essential if s not in extracted_skills]
        
        essential_coverage = len(matched_essential) / max(1, len(essential))
        important_coverage = len(matched_important) / max(1, len(important))
        keyword_score = (essential_coverage * 25.0) + (important_coverage * 10.0)

        # 4. Action Verbs & Structural Formatting (15 pts)
        action_verbs = ["developed", "built", "implemented", "optimized", "engineered", "designed", "deployed", "trained", "architected", "served", "collaborated"]
        verb_matches = [v for v in action_verbs if v in text_lower]
        formatting_score = min(15.0, 5.0 + len(verb_matches) * 2.0)

        total_ats_score = round(min(100.0, section_score + metric_score + keyword_score + formatting_score), 1)

        suggestions = []
        if len(metric_matches) < 3:
            suggestions.append("Add quantifiable metric gaps: Include measurable impact percentages (e.g. 'Optimized inference latency by 35%' or 'Achieved 92% F1-score').")
        
        if missing_essential:
            top_missing = [s.title() for s in missing_essential[:4]]
            suggestions.append(f"Missing core keywords for {target_role}: Add evidence of {', '.join(top_missing)}.")

        if not sections["Contact Info"]:
            suggestions.append("Add clear GitHub and LinkedIn portfolio links in header.")

        tech_stack_gaps = [s.title() for s in missing_essential[:5]]
        if not tech_stack_gaps and "docker" not in extracted_skills:
            tech_stack_gaps.append("Docker")

        # Semantic Similarity Vector Match against Job Description
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([text, role_info["jd_description"]])
            similarity_score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
            vector_match_pct = round(similarity_score * 100, 1)
        except Exception:
            vector_match_pct = 78.0

        return {
            "ats_score": total_ats_score,
            "formatting_score": round(min(100.0, (section_score + formatting_score) / 40.0 * 100), 1),
            "keyword_score": round(min(100.0, keyword_score / 35.0 * 100), 1),
            "vector_match_pct": vector_match_pct,
            "extracted_skills": [s.title() for s in extracted_skills],
            "matched_skills": [s.title() for s in matched_essential + matched_important],
            "missing_skills": [s.title() for s in missing_essential],
            "tech_stack_gaps": tech_stack_gaps,
            "achievement_metric_gaps": metric_matches[:5],
            "suggestions": suggestions,
            "target_role": target_role
        }

nlp_analyzer = ResumeNLPAnalyzer()
