"""
Grader module.
Normalizes total reward into final score.
Ensures deterministic evaluation.
"""
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

    # cap score
    if score > 1.0:
        score = 1.0

    return round(score,2)