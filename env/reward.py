"""
Reward logic for task evaluation
"""

from .models import TaskDifficulty


def normalize_reward(r):

    try:
        r=float(r)
    except:
        return 0.5

    # strict validator safety
    if r <= 0:
        r = 0.02

    if r >= 1:
        r = 0.98

    # avoid edge values
    if r < 0.02:
        r = 0.02

    if r > 0.98:
        r = 0.98

    return r


def compute_reward(task, action):

    r = 0.0

    try:

        # EASY → classification only
        if task.difficulty == TaskDifficulty.EASY:

            if action.predicted_category == task.true_category:

                r += 0.8

            else:

                r -= 0.1

            if action.mark_complete:

                r += 0.2


        # MEDIUM → classification + priority
        elif task.difficulty == TaskDifficulty.MEDIUM:

            if action.predicted_category == task.true_category:

                r += 0.5

            else:

                r -= 0.1

            if action.predicted_priority == task.true_priority:

                r += 0.3

            else:

                r -= 0.05

            if action.mark_complete:

                r += 0.2


        # HARD → classification + priority + scheduling
        elif task.difficulty == TaskDifficulty.HARD:

            if action.predicted_category == task.true_category:

                r += 0.4

            else:

                r -= 0.1

            if action.predicted_priority == task.true_priority:

                r += 0.3

            else:

                r -= 0.05

            # safe scheduling check
            if hasattr(action, "scheduled_position"):

                if action.scheduled_position == task.schedule_position:

                    r += 0.2

            if action.mark_complete:

                r += 0.2


        # prevent negative values
        if r < 0:

            r = 0.02


        # prevent upper bound
        if r >= 1:

            r = 0.98


        # FINAL CRITICAL FIX
        r = normalize_reward(r)


    except Exception as e:

        print("Reward computation error:", e)

        r = 0.5


    return round(r,3)
