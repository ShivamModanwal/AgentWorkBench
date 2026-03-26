"""
Reward logic for task evaluation.

Handles:
classification scoring
priority scoring
scheduling scoring
efficiency penalties
"""
from .models import TaskDifficulty

def compute_reward(task,action):

    r = 0

    # EASY → classification only
    if task.difficulty == TaskDifficulty.EASY:

        if action.predicted_category == task.true_category:

            r += 0.8

        else:

            r -= 0.2

        if action.mark_complete:

            r += 0.1

    # MEDIUM → classification + priority
    elif task.difficulty == TaskDifficulty.MEDIUM:

        if action.predicted_category == task.true_category:

            r += 0.4

        else:

            r -= 0.1

        if action.predicted_priority == task.true_priority:

            r += 0.3

        else:

            r -= 0.05

        if action.mark_complete:

            r += 0.1

    # HARD → classification + priority + scheduling
    elif task.difficulty == TaskDifficulty.HARD:

        if action.predicted_category == task.true_category:

            r += 0.3

        else:

            r -= 0.1

        if action.predicted_priority == task.true_priority:

            r += 0.3

        else:

            r -= 0.05

        if action.scheduled_position == task.schedule_position:

            r += 0.2

        if action.mark_complete:

            r += 0.1

    return r