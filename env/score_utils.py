def clamp_score(raw_score):
    try:
        score = float(raw_score)
        return max(0.001, min(0.999, score))
    except (TypeError, ValueError):
        return 0.001


def format_clamped_score(raw_score):
    return f"{clamp_score(raw_score):.3f}"
