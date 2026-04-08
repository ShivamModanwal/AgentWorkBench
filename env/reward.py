"""
Reward logic for task evaluation
"""

from .models import TaskDifficulty


def normalize_reward(r):

    try:
<<<<<<< HEAD
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
=======
        r = float(r)

    except:
        return 0.5


    # hard clamp strictly inside (0,1)
    r = max(0.02, min(0.98, r))
>>>>>>> 1633981 (Initial commit)

    return r


<<<<<<< HEAD
=======

>>>>>>> 1633981 (Initial commit)
def compute_reward(task, action):

    # NEVER start from zero (important)
    r = 0.05

    try:

        # EASY → classification only
        if task.difficulty == TaskDifficulty.EASY:

            if action.predicted_category == task.true_category:

                r += 0.6

            else:

                r += 0.05


            if action.mark_complete:

                r += 0.25



        # MEDIUM → classification + priority
        elif task.difficulty == TaskDifficulty.MEDIUM:

            if action.predicted_category == task.true_category:

                r += 0.4

            else:

                r += 0.05


            if action.predicted_priority == task.true_priority:

                r += 0.3

            else:

                r += 0.05


            if action.mark_complete:

                r += 0.2



        # HARD → classification + priority + scheduling
        elif task.difficulty == TaskDifficulty.HARD:

            if action.predicted_category == task.true_category:

                r += 0.35

            else:

                r += 0.05


            if action.predicted_priority == task.true_priority:

                r += 0.25

            else:

                r += 0.05


            # scheduling safety
            if hasattr(action, "scheduled_position"):

                if action.scheduled_position == task.schedule_position:

                    r += 0.2


            if action.mark_complete:

                r += 0.2


<<<<<<< HEAD
        # prevent negative values
        if r < 0:

            r = 0.02


        # prevent upper bound
        if r >= 1:

            r = 0.98


        # FINAL CRITICAL FIX
=======
        # upper protection (important)
        if r >= 1:

            r = 0.98


        # lower protection
        if r <= 0:

            r = 0.02


        # final normalization
>>>>>>> 1633981 (Initial commit)
        r = normalize_reward(r)


    except Exception as e:

        print("Reward computation error:", e)

        r = 0.5


<<<<<<< HEAD
    return float(r)
=======
    return float(r)
>>>>>>> 1633981 (Initial commit)
