"""
Grader module.

Normalizes total reward into final score.
Ensures deterministic evaluation.
"""
def grade(total_reward, max_reward, mistakes=0):

    score = total_reward / max_reward

    # mistake penalty
    score -= mistakes * 0.02

    if score < 0:
        score = 0

    if score > 1:
        score = 1

    return round(score,3)