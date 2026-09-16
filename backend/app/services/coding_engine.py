import sys
import io
import traceback
from typing import Dict, List, Any

CURATED_PROBLEMS: List[Dict[str, Any]] = [
    {
        "id": "coin_change",
        "title": "Coin Change - Minimum Coins",
        "difficulty": "Medium",
        "topic": "Dynamic Programming",
        "description": (
            "You are given an integer array coins representing coins of different denominations "
            "and an integer amount representing a total amount of money.\n"
            "Return the fewest number of coins that you need to make up that amount. "
            "If that amount of money cannot be made up by any combination of the coins, return -1.\n\n"
            "Example:\nInput: coins = [1, 2, 5], amount = 11\nOutput: 3 (5 + 5 + 1)"
        ),
        "starter_code": (
            "def coinChange(coins: list[int], amount: int) -> int:\n"
            "    # Implement dynamic programming solution\n"
            "    dp = [float('inf')] * (amount + 1)\n"
            "    dp[0] = 0\n"
            "    for a in range(1, amount + 1):\n"
            "        for c in coins:\n"
            "            if a - c >= 0:\n"
            "                dp[a] = min(dp[a], 1 + dp[a - c])\n"
            "    return dp[amount] if dp[amount] != float('inf') else -1\n"
        ),
        "test_cases": [
            {"coins": [1, 2, 5], "amount": 11, "expected": 3},
            {"coins": [2], "amount": 3, "expected": -1},
            {"coins": [1], "amount": 0, "expected": 0},
            {"coins": [1, 5, 10, 25], "amount": 30, "expected": 2}
        ],
        "function_name": "coinChange"
    },
    {
        "id": "max_subarray",
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "difficulty": "Medium",
        "topic": "Dynamic Programming",
        "description": (
            "Given an integer array nums, find the subarray with the largest sum, and return its sum.\n\n"
            "Example:\nInput: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6 (Subarray: [4,-1,2,1])"
        ),
        "starter_code": (
            "def maxSubArray(nums: list[int]) -> int:\n"
            "    max_sum = nums[0]\n"
            "    current_sum = 0\n"
            "    for x in nums:\n"
            "        current_sum = max(x, current_sum + x)\n"
            "        max_sum = max(max_sum, current_sum)\n"
            "    return max_sum\n"
        ),
        "test_cases": [
            {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4], "expected": 6},
            {"nums": [1], "expected": 1},
            {"nums": [5, 4, -1, 7, 8], "expected": 23}
        ],
        "function_name": "maxSubArray"
    },
    {
        "id": "two_sum",
        "title": "Two Sum (Sorted Array)",
        "difficulty": "Easy-Medium",
        "topic": "Two Pointers",
        "description": (
            "Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, "
            "find two numbers such that they add up to a specific target number.\n"
            "Return the indices of the two numbers, 1-indexed."
        ),
        "starter_code": (
            "def twoSum(numbers: list[int], target: int) -> list[int]:\n"
            "    left, right = 0, len(numbers) - 1\n"
            "    while left < right:\n"
            "        curr = numbers[left] + numbers[right]\n"
            "        if curr == target:\n"
            "            return [left + 1, right + 1]\n"
            "        elif curr < target:\n"
            "            left += 1\n"
            "        else:\n"
            "            right -= 1\n"
            "    return []\n"
        ),
        "test_cases": [
            {"numbers": [2, 7, 11, 15], "target": 9, "expected": [1, 2]},
            {"numbers": [2, 3, 4], "target": 6, "expected": [1, 3]},
            {"numbers": [-1, 0], "target": -1, "expected": [1, 2]}
        ],
        "function_name": "twoSum"
    }
]

class CodingEngine:
    def get_problems(self) -> List[Dict[str, Any]]:
        return CURATED_PROBLEMS

    def get_problem_by_id(self, problem_id: str) -> Dict[str, Any]:
        for p in CURATED_PROBLEMS:
            if p["id"] == problem_id:
                return p
        return CURATED_PROBLEMS[0]

    def evaluate_code(self, problem_id: str, code_str: str) -> Dict[str, Any]:
        problem = self.get_problem_by_id(problem_id)
        func_name = problem["function_name"]
        test_cases = problem["test_cases"]

        # Sandbox execution environment
        exec_globals = {}
        try:
            exec(code_str, exec_globals)
        except Exception as e:
            return {
                "status": "Compile Error",
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "score": 0.0,
                "feedback": f"Syntax / Execution Error: {str(e)}\n{traceback.format_exc()}"
            }

        if func_name not in exec_globals:
            return {
                "status": "Runtime Error",
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "score": 0.0,
                "feedback": f"Function '{func_name}' was not found in your submitted code."
            }

        func = exec_globals[func_name]
        passed = 0
        details = []

        for idx, tc in enumerate(test_cases):
            expected = tc["expected"]
            kwargs = {k: v for k, v in tc.items() if k != "expected"}
            try:
                actual = func(**kwargs)
                if actual == expected:
                    passed += 1
                    details.append(f"Test case #{idx + 1}: Passed")
                else:
                    details.append(f"Test case #{idx + 1}: Failed (Expected {expected}, Got {actual})")
            except Exception as e:
                details.append(f"Test case #{idx + 1}: Error ({str(e)})")

        score = round((passed / len(test_cases)) * 100.0, 1)
        status = "Accepted" if passed == len(test_cases) else ("Partially Accepted" if passed > 0 else "Wrong Answer")

        return {
            "status": status,
            "passed_tests": passed,
            "total_tests": len(test_cases),
            "score": score,
            "feedback": " | ".join(details)
        }

coding_engine = CodingEngine()
