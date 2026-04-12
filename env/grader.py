"""
Grader module.
Normalizes total reward into final score.
Ensures deterministic evaluation.
"""

from .score_utils import clamp_score


def safe_score(score):
    return clamp_score(score)


def grade(expected, output):

    try:
        output = str(output).lower()
    except Exception:
        output = ""

    score = 0.1

    if len(output) > 20:
        score += 0.25

    keywords = [
        "fix",
        "solution",
        "issue",
        "improve",
        "update",
        "implement",
        "resolve",
        "analyze",
    ]

    keyword_hits = 0

    for word in keywords:
        if word in output:
            keyword_hits += 1

    score += keyword_hits * 0.07

    if score > 0.95:
        score = 0.95

    score = safe_score(score)

    return clamp_score(score)


    
  