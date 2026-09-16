from typing import Dict, List, Any

# 10 Questions for AI / ML Track mapped across 5 evaluation dimensions (SVG specification)
AIML_QUESTIONS = [
    {
        "id": 1,
        "topic": "Fundamentals & ML Concepts",
        "dimension": "Concept Understanding",
        "question": "What is the primary difference between L1 (Lasso) and L2 (Ridge) regularization?",
        "options": [
            "L1 produces sparse weights by driving irrelevant coefficients to zero, while L2 shrinks coefficients uniformly",
            "L1 only works on decision trees, while L2 is for linear regression",
            "L2 produces sparse weights while L1 handles multicollinearity without zeroing coefficients",
            "There is no mathematical difference, only naming conventions"
        ],
        "correct": 0,
        "explanation": "L1 regularization uses an absolute penalty leading to exact zero weights for sparsity; L2 uses squared penalties shrinking weights smoothly."
    },
    {
        "id": 2,
        "topic": "Overfitting & Evaluation Metrics",
        "dimension": "Problem Solving",
        "question": "When evaluating a model on an imbalanced dataset with 99% negative cases and 1% positive fraud cases, which metric is most deceptive?",
        "options": [
            "Precision-Recall AUC",
            "Raw Classification Accuracy",
            "F1-Score",
            "Macro-Averaged Recall"
        ],
        "correct": 1,
        "explanation": "A dummy classifier predicting all negatives achieves 99% raw accuracy while having 0% true positive fraud detection."
    },
    {
        "id": 3,
        "topic": "Algorithms & Optimization",
        "dimension": "Practical Knowledge",
        "question": "Why does Adam optimizer typically converge faster than standard Stochastic Gradient Descent (SGD)?",
        "options": [
            "It computes the exact Hessian matrix at every step",
            "It combines momentum with adaptive per-parameter learning rates using first and second moments",
            "It skips backpropagation entirely",
            "It only evaluates training loss on the test partition"
        ],
        "correct": 1,
        "explanation": "Adam maintains exponentially decaying averages of past gradients (momentum) and past squared gradients (adaptive learning rate)."
    },
    {
        "id": 4,
        "topic": "Embeddings & Vectors",
        "dimension": "Concept Understanding",
        "question": "In semantic search with Sentence-BERT, what similarity metric is most commonly computed between normalized embedding vectors?",
        "options": [
            "Cosine Similarity (Dot Product of normalized vectors)",
            "Manhattan Distance (L1)",
            "Hamming Distance",
            "Jaccard Index"
        ],
        "correct": 0,
        "explanation": "Cosine similarity measures the angular orientation between semantic vector representations in latent embedding space."
    },
    {
        "id": 5,
        "topic": "RAG & Hallucination Mitigation",
        "dimension": "System Design",
        "question": "In a Retrieval-Augmented Generation (RAG) system, which strategy best reduces factual hallucination when retrieved context is insufficient?",
        "options": [
            "Increasing temperature to 1.5",
            "Prompt grounding with strict negative rejection instructions ('If not in context, state: insufficient information')",
            "Removing the vector retrieval step",
            "Using smaller chunk overlap sizes"
        ],
        "correct": 1,
        "explanation": "Explicit system prompting instructing the model to constrain answers strictly to the provided context prevents out-of-context fabrication."
    },
    {
        "id": 6,
        "topic": "Deep Learning Architectures",
        "dimension": "Practical Knowledge",
        "question": "Why do Residual Networks (ResNets) successfully train networks with hundreds of layers without suffering gradient degradation?",
        "options": [
            "They eliminate all activation functions",
            "Skip connections allow identity gradients to flow unimpeded directly to earlier layers during backprop",
            "They use dropout on every layer",
            "They replace matrix multiplications with sorting operations"
        ],
        "correct": 1,
        "explanation": "Skip connections (residual links) formulate F(x) + x, preventing vanishing gradients in deep backpropagation."
    },
    {
        "id": 7,
        "topic": "Model Serialization & Serving",
        "dimension": "System Design",
        "question": "When serving high-throughput PyTorch model inference in FastAPI with Docker, which setup provides the lowest latency?",
        "options": [
            "Reloading model weights from disk on every incoming HTTP POST request",
            "Preloading model onto GPU/CPU in memory during FastAPI startup lifespan, disabling gradient tracking with torch.no_grad()",
            "Running training loops during API request processing",
            "Writing requests to a text file and polling every 10 seconds"
        ],
        "correct": 1,
        "explanation": "Lifespan preloading keeps weights warm in VRAM/RAM, while torch.no_grad() eliminates autograd graph overhead."
    },
    {
        "id": 8,
        "topic": "Data Preprocessing & Leaks",
        "dimension": "Problem Solving",
        "question": "To prevent data leakage when scaling features with StandardScaler in Scikit-learn, when should fit_transform be called?",
        "options": [
            "On the combined dataset before train/test splitting",
            "Only fit on training data, then transform both train and test data",
            "Fit on test data only",
            "Fit after calculating evaluation metrics"
        ],
        "correct": 1,
        "explanation": "Fitting on test data or the whole dataset leaks statistical distribution parameters (mean/variance) of unseen data into training."
    },
    {
        "id": 9,
        "topic": "Technical Communication",
        "dimension": "Technical Communication",
        "question": "When explaining a ROC-AUC score of 0.85 to business stakeholders, which explanation is most accurate and clear?",
        "options": [
            "Our model makes correct predictions exactly 85% of the time on all instances",
            "There is an 85% probability that the model ranks a randomly chosen positive case higher than a randomly chosen negative case",
            "The model has 85% less error than a linear equation",
            "The dataset has an 85% signal-to-noise ratio"
        ],
        "correct": 1,
        "explanation": "ROC-AUC represents the concordance probability of ranking a random positive higher than a random negative across all classification thresholds."
    },
    {
        "id": 10,
        "topic": "AI System Scalability",
        "dimension": "System Design",
        "question": "For real-time vector search over 10 million embeddings, which indexing structure provides sub-50ms approximate nearest neighbor queries?",
        "options": [
            "Linear brute-force cosine comparison across all 10 million rows in SQLite",
            "Hierarchical Navigable Small World (HNSW) graph or Inverted File with Product Quantization (IVF-PQ)",
            "B-Tree index on float array string representations",
            "Bubble sort by vector magnitude"
        ],
        "correct": 1,
        "explanation": "HNSW graphs and IVF-PQ are industry standard Approximate Nearest Neighbor (ANN) indexes used in FAISS, Milvus, and pgvector."
    }
]

class SkillAssessmentEngine:
    def get_assessment_questions(self, track: str = "AI / ML") -> List[Dict[str, Any]]:
        return AIML_QUESTIONS

    def evaluate_answers(self, track: str, answers: Dict[int, int]) -> Dict[str, Any]:
        """
        Evaluates assessment and scores across the 5 dimensions:
        1. Concept Understanding
        2. Problem Solving
        3. Practical Knowledge
        4. System Design
        5. Technical Communication
        """
        questions = self.get_assessment_questions(track)
        dim_scores: Dict[str, List[int]] = {
            "Concept Understanding": [],
            "Problem Solving": [],
            "Practical Knowledge": [],
            "System Design": [],
            "Technical Communication": []
        }
        
        weak_topics = []
        strong_topics = []
        total_correct = 0

        for q in questions:
            qid = q["id"]
            user_choice = answers.get(qid)
            is_correct = (user_choice == q["correct"])
            
            dim = q["dimension"]
            dim_scores[dim].append(1 if is_correct else 0)
            
            if is_correct:
                total_correct += 1
                strong_topics.append(q["topic"])
            else:
                weak_topics.append(q["topic"])

        # Calculate composite score (0-100)
        overall_score = round((total_correct / len(questions)) * 100.0, 1)

        # Calculate per-dimension percentages
        dimension_results = {}
        for dim, results in dim_scores.items():
            if results:
                dimension_results[dim] = round((sum(results) / len(results)) * 100.0, 1)
            else:
                dimension_results[dim] = 50.0

        # Map to proficiency band (Slide 12: 0-40 Beginner, 41-60 Intermediate, 61-80 Advanced, 81-100 Expert)
        if overall_score <= 40:
            tier = "Beginner"
        elif overall_score <= 60:
            tier = "Intermediate"
        elif overall_score <= 80:
            tier = "Advanced"
        else:
            tier = "Expert"

        return {
            "overall_score": overall_score,
            "dimension_scores": dimension_results,
            "proficiency_tier": tier,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "total_questions": len(questions),
            "correct_answers": total_correct
        }

skill_assessment_engine = SkillAssessmentEngine()
