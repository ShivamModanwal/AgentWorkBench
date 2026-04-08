"""
Grader module.
Normalizes total reward into final score.
Ensures deterministic evaluation.
"""

def safe_score(score):

    try:
        score=float(score)
    except:
        return 0.5

    # strict bounds (never allow edges)
    if score <= 0:
        return 0.05

    if score >= 1:
        return 0.95

    # push away from edges
    if score < 0.05:
        score = 0.05

    if score > 0.95:
        score = 0.95

    return score


def grade(expected, output):

    try:
        output=str(output).lower()
    except:
        output=""

    score = 0.1   # NEVER start at zero (CRITICAL FIX)

    if len(output) > 20:

        score += 0.3


    keywords = [

        "fix",
        "solution",
        "issue",
        "improve",
        "update",
        "implement",
        "resolve",
        "analyze"

    ]


    for word in keywords:

        if word in output:

            score += 0.08


    # normalize BEFORE rounding
    score = safe_score(score)


    # NEVER round to 2 decimals (CRITICAL FIX)
    return float(score)
