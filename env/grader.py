"""
Grader module for AgentWorkBench
Handles safe scoring and reward formatting
"""

def clamp_score(score: float) -> float:
    """
    Clamp score between 0.01 and 0.99
    Avoid exact 0 or 1 (evaluation rule)
    """

    try:
        score = float(score)

        if score <= 0:
            score = 0.01

        elif score >= 1:
            score = 0.99

        return round(score, 2)

    except Exception:
        return 0.01


def format_score(score: float) -> str:
    """
    Format score to 2 decimal string
    """
    score = clamp_score(score)

    return f"{score:.2f}"


def grade(raw_score: float) -> float:
    """
    Main grading function required by environment.py

    Steps:
    1 Get raw score
    2 Clamp safely
    3 Return safe score
    """

    safe_score = clamp_score(raw_score)

    return safe_score


def step_reward(raw_score: float) -> str:
    """
    STEP reward format
    """

    score = clamp_score(raw_score)

    return f"[STEP] reward={score:.2f}"


def end_reward(raw_score: float) -> str:
    """
    END reward format
    """

    score = clamp_score(raw_score)

    return f"[END] final_reward={score:.2f}"


# Testing block (safe to keep)
if __name__ == "__main__":

    test_scores = [-2,0,0.235,0.678,1,3]

    for s in test_scores:

        print("Raw:",s)
        print("Safe:",grade(s))
        print(step_reward(s))
        print(end_reward(s))
        print()
