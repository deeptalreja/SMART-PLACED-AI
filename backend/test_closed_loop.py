import httpx
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("================================================================")
    print("TESTING END-TO-END CLOSED FEEDBACK LOOP (Slide 05, 07, 09)")
    print("================================================================")
    client = httpx.Client(base_url="http://127.0.0.1:8000")
    
    # 1. Login
    login_res = client.post("/api/v1/auth/login", data={"username": "alex.chen@university.edu", "password": "password123"})
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[1] Logged in as alex.chen@university.edu.")

    # 2. Initial Dashboard State
    d1 = client.get("/api/v1/dashboard/overview", headers=headers).json()
    initial_score = d1["overall_readiness"]
    print(f"[2] Current Dashboard Placement Readiness Score: {initial_score}/100")
    print(f"    Target Role: {d1['target_role']}")
    print(f"    P1 Action: {d1['priority_actions'][0]['title']} -> {d1['priority_actions'][0]['recommended_action']}")

    # 3. Action 1: Solve Coding Challenge (Coin Change DP - closes LeetCode DP gap)
    code = (
        "def coinChange(coins: list[int], amount: int) -> int:\n"
        "    dp = [float('inf')] * (amount + 1)\n"
        "    dp[0] = 0\n"
        "    for a in range(1, amount + 1):\n"
        "        for c in coins:\n"
        "            if a - c >= 0:\n"
        "                dp[a] = min(dp[a], 1 + dp[a - c])\n"
        "    return dp[amount] if dp[amount] != float('inf') else -1\n"
    )
    code_res = client.post("/api/v1/coding/submit", json={"problem_id": "coin_change", "code": code}, headers=headers).json()
    assert code_res["status"] == "Accepted"
    score_after_coding = code_res["updated_overall_readiness"]
    print(f"[3] Coding Challenge Completed: {code_res['status']} ({code_res['passed_tests']}/{code_res['total_tests']} tests passed)")
    print(f"    DSA Readiness rose to: {code_res['updated_dsa_readiness']}%")
    print(f"    Placement Readiness Score updated: {initial_score} -> {score_after_coding}/100")

    # 4. Action 2: Adaptive Technical Interview (Slide 12: Churn model & class imbalance)
    q_res = client.post("/api/v1/interview/generate-question", json={"interview_type": "technical"}, headers=headers).json()
    print(f"[4] Adaptive Question Generated: {q_res['question']}")
    
    student_ans = (
        "In our churn prediction project, the dataset exhibited an 88:12 class imbalance. "
        "Firstly, we addressed this in preprocessing by applying SMOTE combined with Tomek links to oversample minority instances without borderline noise. "
        "Secondly, during training with XGBoost, we tuned the scale_pos_weight parameter to heavily penalize false negatives. "
        "Finally, for evaluation metrics, we avoided raw accuracy and monitored the Precision-Recall AUC (PR-AUC) and F1-score with an optimized threshold of 0.42."
    )
    int_res = client.post("/api/v1/interview/evaluate", json={"session_id": q_res["session_id"], "student_response": student_ans}, headers=headers).json()
    assert int_res["score"] >= 6.0
    score_after_interview = int_res["updated_overall_readiness"]
    print(f"[5] AI Rubric Evaluation Completed: Score {int_res['score']}/10")
    print(f"    Interview Readiness rose to: {int_res['updated_interview_readiness']}%")
    print(f"    Placement Readiness Score updated: {score_after_coding} -> {score_after_interview}/100")

    # 5. Fetch Final Dashboard State
    d_final = client.get("/api/v1/dashboard/overview", headers=headers).json()
    print(f"\n[6] Final Dashboard State:")
    print(f"    Initial Score: {initial_score}/100  -->  Final Score: {d_final['overall_readiness']}/100")
    print(f"    Total Readiness History Logs: {len(d_final['readiness_history'])}")
    print(f"    New P1 Priority Action: {d_final['priority_actions'][0]['title']}")
    
    print("\n================================================================")
    print("SUCCESS: THE CONTINUOUS INTELLIGENCE LOOP IS VERIFIED WORKING! [PASS]")
    print("================================================================")

if __name__ == "__main__":
    main()
