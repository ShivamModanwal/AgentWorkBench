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

    # strict validator protection
    if score <= 0:
        score = 0.02

    if score >= 1:
        score = 0.98

    # avoid edge rounding issues
    if score < 0.02:
        score = 0.02

    if score > 0.98:
        score = 0.98

    return score


def grade(expected, output):

    output = output.lower()

    score = 0.0

    # basic response exists
    if len(output) > 20:
        score += 0.3

    # reasoning keywords
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
            score += 0.1


    # cap score (before safety)
    if score > 1.0:
        score = 1.0


    # CRITICAL FIX — enforce (0,1)
    score = safe_score(score)


    return round(score,2)
